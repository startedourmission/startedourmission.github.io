// Canvas Static Visualization
// 블로그 스타일 정적 마인드맵

class CanvasVisualization {
    constructor() {
        this.container = d3.select('#canvas-visualization');
        this.width = 0;
        this.height = 0;
        this.svg = null;
        this.g = null;
        this.nodes = [];
        this.links = [];
        this.zoom = null;
        
        this.init();
    }
    
    init() {
        this.setupDimensions();
        this.setupSVG();
        this.setupData();
        this.setupControls();
        this.render();
        
        // 윈도우 리사이즈 이벤트
        window.addEventListener('resize', () => this.handleResize());
    }
    
    setupDimensions() {
        const containerRect = document.getElementById('canvas-container').getBoundingClientRect();
        this.width = Math.max(containerRect.width, 800);
        this.height = Math.max(600, window.innerHeight - 200);
    }
    
    setupSVG() {
        // 기존 SVG 제거
        this.container.selectAll('*').remove();
        
        // SVG 생성
        this.svg = this.container
            .append('svg')
            .attr('width', this.width)
            .attr('height', this.height);
            
        // 줌/팬 기능 설정
        this.zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on('zoom', (event) => {
                this.g.attr('transform', event.transform);
            });
            
        this.svg.call(this.zoom);
        
        // 메인 그룹
        this.g = this.svg.append('g');
        
        // 배경 클릭으로 노드 선택 해제
        this.svg.append('rect')
            .attr('width', this.width)
            .attr('height', this.height)
            .style('fill', 'transparent')
            .on('click', () => this.hideNodeDetails());
    }
    
    setupData() {
        if (!window.canvasData) {
            console.error('Canvas data not found');
            return;
        }
        
        // 노드 데이터 준비 (원본 위치 사용)
        this.nodes = window.canvasData.nodes.map(node => ({
            id: node.id,
            type: node.type,
            text: node.text || '',
            file: node.file || null,
            x: node.x,
            y: node.y,
            width: node.width,
            height: node.height
        }));
        
        // 링크 데이터 준비
        this.links = window.canvasData.edges.map(edge => ({
            id: edge.id,
            sourceId: edge.fromNode,
            targetId: edge.toNode,
            fromSide: edge.fromSide || null,
            toSide: edge.toSide || null
        }));
    }
    
    render() {
        // Canvas 크기 계산 (모든 노드가 들어가도록)
        const bounds = this.calculateBounds();
        const scale = this.calculateInitialScale(bounds);
        
        // 줌 초기 설정
        const transform = d3.zoomIdentity
            .translate(this.width / 2, this.height / 2)
            .scale(scale)
            .translate(-bounds.centerX, -bounds.centerY);
            
        this.svg.call(this.zoom.transform, transform);
        
        // 링크 렌더링 (노드 연결선)
        const links = this.g.selectAll('.link')
            .data(this.links)
            .join('line')
            .attr('class', 'link')
            .attr('x1', d => this.getNodeById(d.sourceId).x)
            .attr('y1', d => this.getNodeById(d.sourceId).y)
            .attr('x2', d => this.getNodeById(d.targetId).x)
            .attr('y2', d => this.getNodeById(d.targetId).y)
            .style('stroke', '#ccc')
            .style('stroke-width', 1)
            .style('stroke-opacity', 0.7);
            
        // 노드 그룹 생성
        const nodeGroups = this.g.selectAll('.node-group')
            .data(this.nodes)
            .join('g')
            .attr('class', 'node-group')
            .attr('transform', d => `translate(${d.x}, ${d.y})`)
            .style('cursor', 'pointer');
            
        // 노드 배경 (블로그 스타일 카드)
        nodeGroups.append('rect')
            .attr('class', 'node-bg')
            .attr('width', d => d.width)
            .attr('height', d => d.height)
            .attr('x', d => -d.width / 2)
            .attr('y', d => -d.height / 2)
            .attr('rx', 5)
            .style('fill', '#fff')
            .style('stroke', '#ddd')
            .style('stroke-width', 1)
            .on('click', (event, d) => {
                event.stopPropagation();
                this.showNodeDetails(d);
            });
            
        // 노드 텍스트 (블로그 스타일)
        nodeGroups.append('foreignObject')
            .attr('width', d => d.width - 16)
            .attr('height', d => d.height - 16)
            .attr('x', d => -d.width / 2 + 8)
            .attr('y', d => -d.height / 2 + 8)
            .append('xhtml:div')
            .style('width', '100%')
            .style('height', '100%')
            .style('display', 'flex')
            .style('align-items', 'center')
            .style('justify-content', 'center')
            .style('text-align', 'center')
            .style('font-size', '11px')
            .style('line-height', '1.3')
            .style('color', '#333')
            .style('font-family', 'var(--font-family)')
            .style('overflow', 'hidden')
            .style('padding', '4px')
            .html(d => this.formatNodeText(d.text));
    }
    
    getNodeById(id) {
        return this.nodes.find(node => node.id === id);
    }
    
    calculateBounds() {
        if (this.nodes.length === 0) return { centerX: 0, centerY: 0, width: 800, height: 600 };
        
        const bounds = this.nodes.reduce((acc, node) => {
            const x = node.x;
            const y = node.y;
            return {
                minX: Math.min(acc.minX, x - node.width / 2),
                maxX: Math.max(acc.maxX, x + node.width / 2),
                minY: Math.min(acc.minY, y - node.height / 2),
                maxY: Math.max(acc.maxY, y + node.height / 2)
            };
        }, {
            minX: Infinity,
            maxX: -Infinity,
            minY: Infinity,
            maxY: -Infinity
        });
        
        const centerX = (bounds.minX + bounds.maxX) / 2;
        const centerY = (bounds.minY + bounds.maxY) / 2;
        const width = bounds.maxX - bounds.minX;
        const height = bounds.maxY - bounds.minY;
        
        return { centerX, centerY, width, height };
    }
    
    calculateInitialScale(bounds) {
        const padding = 50;
        const scaleX = (this.width - padding * 2) / Math.max(bounds.width, 1);
        const scaleY = (this.height - padding * 2) / Math.max(bounds.height, 1);
        return Math.min(scaleX, scaleY, 1); // 최대 1배율
    }
    
    formatNodeText(text) {
        if (!text) return '';
        
        // 노드에서는 wikilink를 단순 텍스트로 변환 (표시용)
        let processedText = this.convertWikiLinksToText(text);
        
        // 긴 텍스트는 줄임표 처리
        if (processedText.length > 100) {
            processedText = processedText.substring(0, 97) + '...';
        }
        
        // HTML 이스케이프
        return this.escapeHtml(processedText);
    }
    
    convertWikiLinksToText(text) {
        // Obsidian wikilink를 단순 텍스트로 변환 (노드 표시용)
        const wikiLinkPattern = /\[\[([^\]]+)\]\]/g;
        
        return text.replace(wikiLinkPattern, (match, linkContent) => {
            // 파이프(|)로 분리된 경우 display text만 사용
            if (linkContent.includes('|')) {
                const parts = linkContent.split('|');
                return parts[1].trim();
            } else {
                // 파이프가 없으면 전체 내용 사용
                return linkContent.trim();
            }
        });
    }
    
    convertWikiLinks(text) {
        // Obsidian wikilink 패턴: [[target|display]] 또는 [[target]]
        const wikiLinkPattern = /\[\[([^\]]+)\]\]/g;
        
        return text.replace(wikiLinkPattern, (match, linkContent) => {
            let target, displayText;
            
            // 파이프(|)로 분리된 경우
            if (linkContent.includes('|')) {
                const parts = linkContent.split('|');
                target = parts[0].trim();
                displayText = parts[1].trim();
            } else {
                // 파이프가 없으면 target이 display text
                target = linkContent.trim();
                displayText = target;
            }
            
            // URL 친화적으로 변환
            const urlFriendlyTarget = this.toUrlFriendly(target);
            
            // HTML 링크 생성 (새 탭에서 열기)
            return `<a href="${urlFriendlyTarget}.html" target="_blank" style="color: var(--color-link); text-decoration: underline;">${this.escapeHtml(displayText)}</a>`;
        });
    }
    
    toUrlFriendly(input) {
        return input.toLowerCase()
            .replace(/[^\w\s]/g, '') // 영숫자가 아닌 문자 제거
            .replace(/\s+/g, '-');   // 공백을 하이픈으로
    }
    
    escapeHtml(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
    
    showNodeDetails(node) {
        const panel = document.getElementById('node-details');
        const title = document.getElementById('node-title');
        const content = document.getElementById('node-content');
        
        title.textContent = node.type.charAt(0).toUpperCase() + node.type.slice(1) + ' Node';
        
        let details = `<strong>ID:</strong> ${node.id}<br>`;
        if (node.text) {
            const processedText = this.convertWikiLinks(node.text).replace(/\n/g, '<br>');
            details += `<strong>Content:</strong><br>${processedText}<br>`;
        }
        if (node.file) {
            details += `<strong>File:</strong> ${node.file}<br>`;
        }
        details += `<strong>Position:</strong> (${Math.round(node.x)}, ${Math.round(node.y)})<br>`;
        details += `<strong>Size:</strong> ${node.width} × ${node.height}`;
        
        content.innerHTML = details;
        panel.style.display = 'block';
    }
    
    hideNodeDetails() {
        document.getElementById('node-details').style.display = 'none';
    }
    
    setupControls() {
        // Reset Zoom 버튼
        document.getElementById('reset-zoom').addEventListener('click', () => {
            this.svg.transition()
                .duration(750)
                .call(this.zoom.transform, d3.zoomIdentity);
        });
        
        // Center View 버튼
        document.getElementById('center-view').addEventListener('click', () => {
            this.centerView();
        });
        
        // 노드 디테일 패널 닫기 버튼
        document.getElementById('close-details').addEventListener('click', () => {
            this.hideNodeDetails();
        });
    }
    
    centerView() {
        if (this.nodes.length === 0) return;
        
        const bounds = this.calculateBounds();
        const scale = this.calculateInitialScale(bounds);
        
        const transform = d3.zoomIdentity
            .translate(this.width / 2, this.height / 2)
            .scale(scale)
            .translate(-bounds.centerX, -bounds.centerY);
            
        this.svg.transition()
            .duration(750)
            .call(this.zoom.transform, transform);
    }
    
    handleResize() {
        this.setupDimensions();
        
        this.svg
            .attr('width', this.width)
            .attr('height', this.height);
    }
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    if (window.canvasData) {
        new CanvasVisualization();
    } else {
        console.error('Canvas data not available');
        document.getElementById('canvas-visualization').innerHTML = 
            '<p style="text-align: center; color: #666; padding: 50px;">Canvas data could not be loaded.</p>';
    }
});