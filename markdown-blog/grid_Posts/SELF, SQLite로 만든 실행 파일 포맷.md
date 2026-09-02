---
date: 2026-08-26
ready: false
tags:
  - 정보
  - Headliner
  - 도구
  - 오픈소스
description: "ELF를 SQLite 테이블로 풀어 담고 헤더 68바이트 자리에 SELF를 박으면 리눅스가 그대로 실행합니다. 왕복은 무손실이고 디스크는 오히려 줄지만, 두 프로세스가 텍스트 페이지를 공유하지 못합니다."
image: "![[SELF, SQLite로 만든 실행 파일 포맷-thumb.png]]"
---

ELF는 이미 데이터베이스입니다. 문자열을 한곳에 모아 재사용하고(`.strtab`), 이름으로 찾을 인덱스를 따로 둡니다(`.hash`, `.gnu.hash`). 스키마를 기록하고, 섹션끼리 오프셋으로 외래 키를 겁니다. 다만 그 모든 것을 직접 만든 바이너리 직렬화로 구현합니다.

그러면 그냥 데이터베이스를 쓰면 어떻게 되느냐가 SELF(Structured Executable & Linkable Format)의 출발점입니다. 실행 파일을 SQLite 파일로 만들고, 리눅스가 그걸 그대로 실행하게 합니다. 포맷은 완성됐고 ELF와 무손실로 왕복하며, 구현은 `fzakaria/selfdb`에 공개돼 있습니다.

## application_id

SQLite 헤더는 68바이트 오프셋에 4바이트짜리 `application_id` 필드를 갖습니다. 파일 포맷 식별용으로 예약된 자리입니다. SELF는 여기에 `0x53454c46`을 박습니다. ASCII로 `SELF`입니다.

커널의 `binfmt_misc`에는 두 조건을 함께 보는 매직 패턴을 등록합니다. 오프셋 0의 SQLite 헤더와 오프셋 68의 SELF 식별자입니다. 둘 다 맞으면 커널이 이 파일을 일반 데이터베이스가 아니라 실행 대상으로 보고 지정된 인터프리터에 넘깁니다.

평범한 SQLite 파일과 실행 가능한 SQLite 파일을 가르는 게 4바이트뿐이라는 뜻입니다.

## 스키마

실행에 실제로 필요한 테이블은 두 개입니다. 프로그램 헤더가 들어가는 `segments`와 심볼 테이블이 들어가는 `symbols`입니다.

```sql
CREATE TABLE segments (
  id INTEGER PRIMARY KEY,
  type TEXT NOT NULL,           -- 'load', 'tls', 'stack', 'relro'
  offset INTEGER NOT NULL,
  vaddr INTEGER NOT NULL,
  filesz INTEGER NOT NULL,
  memsz INTEGER NOT NULL,
  r INTEGER, w INTEGER, x INTEGER,
  align INTEGER NOT NULL DEFAULT 4096,
  content BLOB
);
```

```sql
CREATE TABLE symbols (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  version TEXT,                 -- 'GLIBC_2.2.5' 같은 값
  value INTEGER,
  size INTEGER,
  type TEXT,                    -- 'func', 'object', 'tls'
  bind TEXT,                    -- 'global', 'weak', 'local'
  defined INTEGER NOT NULL,
  exported INTEGER NOT NULL
);
CREATE INDEX idx_symbols_name ON symbols(name, version);
```

이 두 테이블이 ELF의 `.strtab`, `.hash`, `.gnu.hash`, `.gnu.version_r`을 한꺼번에 대체합니다. 문자열 재사용은 SQLite가 알아서 하고, 이름 조회 인덱스는 `CREATE INDEX` 한 줄입니다. ELF가 손으로 만들던 데이터베이스 원시 기능을 진짜 데이터베이스에 맡긴 셈입니다.

`sections`, `notes`, `dynamic_entries` 같은 메타데이터 테이블은 도구용이고 실행에는 필요 없습니다. 그래서 `strip(1)`이 트랜잭션이 됩니다. 해당 테이블을 지우고 `VACUUM`하면 끝입니다.

바이너리 도구들도 뷰로 내려앉습니다.

```sql
CREATE VIEW exports AS SELECT name, version, type, size
  FROM symbols WHERE exported = 1;
CREATE VIEW imports AS SELECT name, version
  FROM symbols WHERE defined = 0;
CREATE VIEW ldd AS SELECT ord, soname FROM needed ORDER BY ord;
```

`ldd(1)` 대신 `sqlite3 hello 'SELECT soname FROM ldd'`를 칩니다. `nm -D --undefined` 대신 `SELECT name,version FROM imports`이고, `readelf -l` 대신 `SELECT type,vaddr,memsz,r,w,x FROM segments WHERE type="load"`입니다. 출력 파싱이 사라지고 질의가 남습니다.

## 로더

변환 도구 `elf2self`가 ELF를 읽어 프로그램 헤더와 심볼 테이블을 뽑아 SQLite에 씁니다. 저자는 이 단계가 결국 `gcc`나 `ld` 안으로 들어갈 수 있다고 봅니다.

실행은 `self-exec`가 맡습니다. `libsqlite3`에 링크된 작은 C 프로그램이고 `binfmt_misc`에 인터프리터로 등록됩니다. 하는 일은 ELF 로더와 같습니다. 프로그램 헤더와 심볼 테이블을 데이터베이스에서 읽고, load 세그먼트를 메모리에 매핑하고, 재배치를 수행하고, 진입점으로 점프합니다.

여기서 제약이 하나 생깁니다. **`self-exec` 자신은 ELF여야 합니다.** SELF로 만들면 `binfmt_misc`가 그걸 다시 자기에게 넘겨 무한 재귀에 빠집니다.

동적 링킹은 두 갈래로 시도했습니다. 하나는 glibc의 `rtld-audit` 훅을 쓰는 방식입니다. 감사 라이브러리가 "이 심볼은 어느 라이브러리가 채우나"만 SQL로 답하고, 매핑과 재배치는 기존 `ld.so`가 그대로 합니다. 지연 PLT 바인딩, IFUNC, TLS, 심볼 버저닝이 전부 살아남습니다.

다른 하나는 동적 링커 자체를 C와 SQL로 다시 쓴 `self-ld`입니다. 모든 오브젝트의 세그먼트를 매핑하고, export를 등록하고, GOT 엔트리를 질의로 채웁니다.

```sql
SELECT s.value + o.load_bias
FROM relocations r
JOIN symbols s ON r.symbol = s.id
JOIN objects o ON s.object = o.id
WHERE r.id = ?
ORDER BY o.load_order
LIMIT 1;
```

심볼 해석 순서라는 링커의 오래된 규칙이 `ORDER BY ... LIMIT 1`로 적힙니다. 다만 이쪽은 개념 증명 단계입니다. 실제로 쓸 만한 건 첫 번째 갈래입니다.

## 클로저

SELF 데이터베이스는 실행 파일 하나에 머물 이유가 없습니다. 프로그램과 그 전이 의존성 전부를 한 파일에 담을 수 있고, 저자는 이것을 클로저라고 부릅니다.

```sql
CREATE TABLE objects (
  id INTEGER PRIMARY KEY,
  path TEXT UNIQUE,
  soname TEXT,
  kind TEXT,
  is_root INTEGER
);
CREATE TABLE needs (
  object_id INTEGER REFERENCES objects(id),
  ord INTEGER NOT NULL,
  soname TEXT NOT NULL,
  resolved_path TEXT REFERENCES objects(path)
);
```

`resolved_path`가 핵심입니다. ELF의 의존성은 soname이라는 이름으로만 적혀 있고, 그 이름이 실제로 어느 파일을 가리키는지는 실행 시점의 검색 경로가 정합니다. 여기서는 모든 의존성 간선이 특정 경로로 미리 해소돼 외래 키로 박힙니다. Nix가 `RUNPATH`로 하던 명시적 의존성 해소가 스키마의 외래 키로 그대로 옮겨옵니다.

규모 시험도 했습니다. 실행 파일 723개와 서로 다른 공유 라이브러리 400개, 합쳐서 오브젝트 1,123개와 심볼 346,386개를 데이터베이스 하나에 담았습니다. 결과가 611.9 MiB입니다.

같은 내용을 개별 ELF 파일로 두면 644.4 MiB입니다. **데이터베이스 쪽이 더 작습니다.** b-tree 오버헤드가 많은 오브젝트에 걸쳐 분산되고, 여러 프로그램이 함께 쓰는 라이브러리가 `objects` 테이블에 여러 번 등장하되 같은 콘텐츠 블롭을 참조하기 때문입니다. 정규화가 중복 제거를 대신합니다.

프로그램마다 클로저를 따로 만드는 AppImage 방식으로 같은 내용을 담으면 5.53 GiB입니다. 9배 차이입니다.

## mmap

여기서 대가가 나옵니다.

같은 ELF 바이너리를 두 프로세스가 실행하면 커널이 텍스트 세그먼트 페이지를 공유합니다. 파일이 그대로 메모리에 매핑되기 때문에 한 벌만 올라가고 페이지 캐시가 그것을 관리합니다. SELF는 바이트를 b-tree에서 꺼내 복사합니다. 그래서 **두 프로세스가 텍스트 페이지를 공유하지 못합니다.** 프로세스마다 사본이 생기고, 커널의 페이지 관리 최적화가 그만큼 무력해집니다.

저자도 이 사실을 적어두었습니다. 다만 성능 항목에 넣고 다른 수치와 나란히 다룹니다. SQLite를 열고 인터프리터를 초기화하는 데 약 5밀리초의 고정 비용이 들고, 거기에 이미지 바이트를 복사하는 시간이 비례해서 붙는다는 식입니다. 15 KiB짜리 `hello`는 차이가 미미하고, 42 MiB에 라이브러리 47개를 매다는 `gdb`는 측정 가능하지만 크지 않은 증가를 보입니다. 크기 쪽은 더 나아서, strip한 `coreutils`가 1,794,048바이트로 ELF의 1,768,632바이트와 1% 안쪽입니다.

HN 스레드는 같은 사실을 다르게 읽었습니다. 537포인트를 받은 이 글의 최상위 우려가 정확히 mmap이었고, 거기서는 이것이 지연 항목이 아니라 실격 사유로 다뤄집니다. 실행 파일이 메모리에 공유 가능한 이미지여야 한다는 것은 성능 튜닝이 아니라 유닉스가 40년간 유지해온 전제이기 때문입니다. `fork` 이후의 메모리 회계, 컨테이너 밀도, 같은 바이너리를 수백 개 띄우는 서버의 상주 메모리가 전부 이 전제 위에 서 있습니다.

한쪽은 5밀리초라고 쓰고 한쪽은 계약 위반이라고 읽습니다. 사실 자체는 양쪽이 같습니다.

## 중복 제거가 옮겨간 자리

두 숫자를 나란히 놓으면 이 포맷이 실제로 무엇을 한 것인지 보입니다. 디스크에서는 644.4 MiB가 611.9 MiB로 줄었고, 메모리에서는 공유되던 것이 프로세스 수만큼 복제됩니다.

**SELF는 중복 제거를 페이지 캐시에서 b-tree로 옮깁니다.** 디스크에서 이득을 보고 RAM에서 손해를 봅니다. 어느 출처도 이 교환을 한 문장으로 적어두지 않았지만, 클로저 실험의 611.9 MiB와 mmap 각주는 같은 설계 결정의 앞뒷면입니다. 그리고 이 교환은 실행 파일이 많고 동시 실행 프로세스가 적은 환경, 예를 들면 컨테이너 이미지나 배포 아티팩트 쪽에서는 유리하고, 같은 바이너리를 대량으로 띄우는 서버에서는 불리합니다. 범용 포맷의 교체가 아니라 배포 계층의 교체로 읽는 쪽이 맞습니다.

바이너리를 질의 가능한 데이터로 보는 관점 자체는 계보가 깁니다. osquery와 Steampipe가 시스템 상태에 SQL을 얹었고, 더 거슬러 올라가면 Smalltalk와 Lisp의 영속 이미지, PICK과 AS/400, 마이크로소프트가 접은 WinFS가 있습니다. 매번 같은 자리에서 멈췄다는 게 이 계보의 특징입니다. 질의 가능성을 얻는 대가로 운영체제가 이미 최적화해둔 무언가를 포기해야 했습니다. 이번에 포기 대상은 mmap입니다.

그럼에도 이 글에서 가장 설득력 있는 대목은 성능이 아닙니다. `LD_PRELOAD`가 트랜잭션이 되는 부분입니다.

```sql
$ sqlite3 system.db "BEGIN;
    CREATE TABLE preload(ord INTEGER PRIMARY KEY, path TEXT);
    INSERT INTO preload VALUES (0, 'libmul.so.1.self');
  COMMIT;"
```

재링크도 환경 변수도 없이 모든 바이너리에 라이브러리를 원자적으로 끼워 넣습니다. 되돌리는 것은 `DELETE`와 `COMMIT`입니다. 추적용 `malloc`을 시스템 전체에 심어보고 `ROLLBACK`하는 일이 트랜잭션 하나가 됩니다. 시스템 구성이 파일 조작이 아니라 스키마 변경이 되면 원자성과 롤백이 공짜로 따라옵니다. 이건 mmap과 교환할 만한 성질인지 따로 저울에 올려볼 값어치가 있습니다.

한 가지 더 있습니다. 요즘 바이너리를 조사하는 주체가 사람에서 도구로, 다시 에이전트로 넘어가고 있습니다. 의존성 추적, SBOM 생성, 취약점 대조가 전부 그렇습니다. 이 작업들은 `readelf` 출력을 파싱하는 일이었고, 파싱은 깨지기 쉽습니다. `ldd`가 `JOIN`이 되면 그 층이 통째로 사라집니다. 실행 성능이 아니라 도구 표면을 기준으로 포맷을 고르는 게 언제 합리적이 되는지는 아직 열린 질문이고, 이 프로젝트가 그 질문의 가장 극단적인 형태입니다.

---

참고: [Your executable is a SQLite database (Farid Zakaria)](https://fzakaria.com/2026/08/23/your-executable-is-a-sqlite-database) · [fzakaria/selfdb](https://github.com/fzakaria/selfdb) · [Simon Willison의 정리](https://simonwillison.net/2026/Aug/24/your-executable-is-a-sqlite-database/) · [Hacker News 토론 (537pt/105댓글)](https://news.ycombinator.com/item?id=49415271) · [Three ways to smuggle SQLite into Nix](https://fzakaria.com/2026/08/19/three-ways-to-smuggle-sqlite-into-nix)
