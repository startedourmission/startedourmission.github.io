// Index page graph view - Obsidian-style force-directed graph of wiki-links between posts.
(function () {
    if (!window.graphData) return;

    const container = document.getElementById('graph-view');
    if (!container) return;

    const rawNodes = (window.graphData.nodes || []).map(n => Object.assign({}, n));
    const rawEdges = window.graphData.edges || [];
    const nodeById = new Map(rawNodes.map(n => [n.id, n]));
    const links = rawEdges
        .filter(e => nodeById.has(e.source) && nodeById.has(e.target))
        .map(e => ({ source: e.source, target: e.target }));

    // Degree for sizing
    const degree = new Map();
    rawNodes.forEach(n => degree.set(n.id, 0));
    links.forEach(l => {
        degree.set(l.source, (degree.get(l.source) || 0) + 1);
        degree.set(l.target, (degree.get(l.target) || 0) + 1);
    });

    // Category palette (deterministic hash → hue)
    const colorFor = (() => {
        const cache = new Map();
        return (cat) => {
            if (cache.has(cat)) return cache.get(cat);
            let h = 0;
            for (let i = 0; i < cat.length; i++) h = (h * 31 + cat.charCodeAt(i)) >>> 0;
            const hue = h % 360;
            const color = `hsl(${hue}, 55%, 55%)`;
            cache.set(cat, color);
            return color;
        };
    })();

    let width = container.clientWidth || 800;
    let height = container.clientHeight || 520;

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const rootGroup = svg.append('g');
    const linkLayer = rootGroup.append('g').attr('class', 'graph-links');
    const nodeLayer = rootGroup.append('g').attr('class', 'graph-nodes');

    const zoom = d3.zoom()
        .scaleExtent([0.15, 4])
        .on('zoom', (event) => rootGroup.attr('transform', event.transform));
    svg.call(zoom);

    const linkSel = linkLayer
        .selectAll('line')
        .data(links)
        .join('line')
        .attr('stroke', 'var(--graph-link, #b0b0b0)')
        .attr('stroke-opacity', 0.55)
        .attr('stroke-width', 1);

    const nodeSel = nodeLayer
        .selectAll('g.graph-node')
        .data(rawNodes, d => d.id)
        .join('g')
        .attr('class', 'graph-node')
        .style('cursor', 'pointer')
        .on('click', (_e, d) => { window.location.href = d.url; })
        .call(d3.drag()
            .on('start', (event, d) => {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x; d.fy = d.y;
            })
            .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y; })
            .on('end', (event, d) => {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null; d.fy = null;
            }));

    nodeSel.append('circle')
        .attr('r', d => 4 + Math.min(10, Math.sqrt(degree.get(d.id) || 0) * 2))
        .attr('fill', d => colorFor(d.category || ''))
        .attr('stroke', 'var(--graph-node-stroke, #fff)')
        .attr('stroke-width', 1.2);

    nodeSel.append('title').text(d => `${d.title}${d.category ? ' · ' + d.category : ''}`);

    nodeSel.append('text')
        .attr('dx', 8)
        .attr('dy', '0.35em')
        .attr('font-size', 10)
        .attr('fill', 'var(--graph-label, #555)')
        .attr('pointer-events', 'none')
        .text(d => d.title.length > 24 ? d.title.slice(0, 23) + '…' : d.title);

    const simulation = d3.forceSimulation(rawNodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(60).strength(0.4))
        .force('charge', d3.forceManyBody().strength(-120))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collide', d3.forceCollide().radius(d => 10 + Math.sqrt(degree.get(d.id) || 0) * 2))
        .on('tick', () => {
            linkSel
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            nodeSel.attr('transform', d => `translate(${d.x},${d.y})`);
        });

    const resetBtn = document.getElementById('graph-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);
            simulation.alpha(0.6).restart();
        });
    }

    let resizeFrame = null;
    window.addEventListener('resize', () => {
        if (resizeFrame) cancelAnimationFrame(resizeFrame);
        resizeFrame = requestAnimationFrame(() => {
            width = container.clientWidth || width;
            height = container.clientHeight || height;
            svg.attr('width', width).attr('height', height);
            simulation.force('center', d3.forceCenter(width / 2, height / 2));
            simulation.alpha(0.3).restart();
        });
    });
})();
