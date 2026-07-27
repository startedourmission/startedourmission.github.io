// Index page search — client-side filter over posts by title/description/tags,
// combined (AND) with tag chips. No external dependencies.
(function () {
    if (!window.searchData) return;

    const posts = window.searchData || [];
    const input = document.getElementById('search-input');
    const clearBtn = document.getElementById('search-clear');
    const resultsEl = document.getElementById('search-results');
    const activeTagsEl = document.getElementById('search-active-tags');
    if (!input || !resultsEl) return;

    // 활성 태그 필터 집합 (소문자 비교)
    const activeTags = new Set();

    // 미리 소문자 인덱스를 만들어 매 입력마다 재계산하지 않음
    const indexed = posts.map(p => ({
        post: p,
        title: (p.title || '').toLowerCase(),
        desc: (p.description || '').toLowerCase(),
        tagsLower: (p.tags || []).map(t => t.toLowerCase())
    }));

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function currentQuery() {
        return input.value.trim().toLowerCase();
    }

    function isActive() {
        return currentQuery().length > 0 || activeTags.size > 0;
    }

    function matches(item, q) {
        // 모든 활성 태그를 포함해야 함 (AND)
        for (const t of activeTags) {
            if (!item.tagsLower.includes(t)) return false;
        }
        if (!q) return activeTags.size > 0;
        return (
            item.title.indexOf(q) !== -1 ||
            item.desc.indexOf(q) !== -1 ||
            item.tagsLower.some(t => t.indexOf(q) !== -1)
        );
    }

    function renderActiveTags() {
        if (activeTags.size === 0) {
            activeTagsEl.innerHTML = '';
            return;
        }
        activeTagsEl.innerHTML = Array.from(activeTags)
            .map(t => `<button type="button" class="search-chip" data-tag="${escapeHtml(t)}">${escapeHtml(t)}</button>`)
            .join('');
    }

    function renderResults() {
        if (!isActive()) {
            resultsEl.hidden = true;
            resultsEl.innerHTML = '';
            return;
        }
        const q = currentQuery();
        const hits = indexed.filter(item => matches(item, q));
        resultsEl.hidden = false;

        if (hits.length === 0) {
            resultsEl.innerHTML = '<p class="search-no-results">검색 결과가 없습니다.</p>';
            return;
        }

        const meta = `<p class="search-results-meta">${hits.length}개 결과</p>`;
        const list = hits.map(item => {
            const p = item.post;
            const dateHtml = p.date ? `<span class="search-result-meta">${escapeHtml(p.date)}</span>` : '';
            const descHtml = p.description ? `<p class="search-result-desc">${escapeHtml(p.description)}</p>` : '';
            const tagsHtml = (p.tags && p.tags.length)
                ? `<div class="search-result-tags">${p.tags.map(escapeHtml).join(' · ')}</div>`
                : '';
            return `<div class="search-result-item">
                <a class="search-result-title" href="${escapeHtml(p.url)}">${escapeHtml(p.title)}</a>${dateHtml}
                ${descHtml}
                ${tagsHtml}
            </div>`;
        }).join('');

        resultsEl.innerHTML = meta + list;
    }

    function syncTagFilterHighlight() {
        document.querySelectorAll('.tag-filter').forEach(a => {
            const t = (a.getAttribute('data-tag') || '').toLowerCase();
            a.classList.toggle('is-active', activeTags.has(t));
        });
    }

    function update() {
        clearBtn.classList.toggle('is-visible', input.value.length > 0);
        renderActiveTags();
        renderResults();
        syncTagFilterHighlight();
    }

    function addTag(tag) {
        activeTags.add(tag.toLowerCase());
        update();
        input.focus();
    }

    function removeTag(tag) {
        activeTags.delete(tag.toLowerCase());
        update();
    }

    input.addEventListener('input', update);

    clearBtn.addEventListener('click', function () {
        input.value = '';
        update();
        input.focus();
    });

    // 활성 태그 칩 클릭 → 제거
    activeTagsEl.addEventListener('click', function (e) {
        const chip = e.target.closest('.search-chip');
        if (chip) removeTag(chip.getAttribute('data-tag'));
    });

    // 기존 Tags 섹션의 링크를 필터로 가로채기 (JS 없으면 태그 페이지로 폴백)
    document.querySelectorAll('.tag-filter').forEach(a => {
        a.addEventListener('click', function (e) {
            const tag = a.getAttribute('data-tag');
            if (!tag) return;
            e.preventDefault();
            if (activeTags.has(tag.toLowerCase())) {
                removeTag(tag);
            } else {
                addTag(tag);
                resultsEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
    });

    update();
})();
