# Well-Known Ports

## 포트 번호 범위
- Well-Known Ports: 0 ~ 1023 (시스템 포트)
- Registered Ports: 1024 ~ 49151 (사용자 포트)
- Dynamic Ports: 49152 ~ 65535 (동적 포트)

## 주요 시스템 포트 (0-1023)

### 파일 전송 관련
- **20**: FTP (데이터)
- **21**: FTP (제어)
- **22**: SSH/SFTP (보안 파일 전송)
- **69**: TFTP (Trivial File Transfer Protocol)

### 메일 관련
- **25**: SMTP (이메일 전송)
- **110**: POP3 (이메일 수신)
- **143**: IMAP (이메일 수신)
- **465**: SMTPS (보안 이메일 전송)
- **587**: SMTP Submission
- **993**: IMAPS (보안 IMAP)
- **995**: POP3S (보안 POP3)

### 웹 관련
- **80**: HTTP
- **443**: HTTPS
- **8080**: HTTP Alternate (프록시)

### 원격 접속
- **22**: SSH
- **23**: Telnet
- **3389**: RDP (Remote Desktop Protocol)

### 네임 서비스
- **53**: DNS (Domain Name System)
- **67**: DHCP Server
- **68**: DHCP Client
- **88**: Kerberos
- **123**: NTP (Network Time Protocol)

### 데이터베이스
- **1433**: MS SQL Server
- **1521**: Oracle
- **3306**: MySQL
- **5432**: PostgreSQL
- **27017**: MongoDB

### 기타 중요 포트
- **161**: SNMP
- **162**: SNMP Trap
- **389**: LDAP
- **636**: LDAPS (보안 LDAP)
- **989**: FTPS (데이터)
- **990**: FTPS (제어)

## 자주 사용되는 등록 포트 (1024-49151)

### 개발 관련
- **3000**: Node.js 기본 포트
- **4200**: Angular 개발 서버
- **8080**: Apache Tomcat
- **8088**: Apache HTTP
- **8443**: Apache Tomcat SSL
- **9000**: Jenkins

### 데이터베이스 관리
- **5984**: CouchDB
- **6379**: Redis
- **9042**: Cassandra

### 메시징 & 큐
- **5672**: RabbitMQ
- **61616**: Apache ActiveMQ

### 모니터링
- **9090**: Prometheus
- **9100**: Node Exporter
- **9200**: Elasticsearch

## 보안 고려사항

### 포트 보안 지침
1. Well-Known 포트는 관리자 권한 필요
2. 사용하지 않는 포트는 방화벽에서 차단
3. 중요 서비스는 기본 포트 변경 권장
4. 정기적인 포트 스캔 모니터링 실시

### 일반적인 보안 설정
```bash
# 방화벽 설정 예시 (Linux)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -P INPUT DROP
```

## 포트 충돌 방지
1. 서비스 시작 전 포트 사용 여부 확인
2. 포트 중복 사용 시 다음 방법 고려:
   - 포트 번호 변경
   - 프록시 서버 사용
   - 컨테이너화 (Docker)

## 포트 검사 명령어
```bash
# Linux/Mac
netstat -tulpn
lsof -i :포트번호

# Windows
netstat -ano
```