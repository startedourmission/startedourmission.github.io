// Canvas Visualization using D3.js
// 인터랙티브 마인드맵 시각화

class CanvasVisualization {
    constructor() {
        this.container = d3.select('#canvas-visualization');
        this.width = 0;
        this.height = 0;
        this.svg = null;
        this.g = null;
        this.simulation = null;
        this.nodes = [];
        this.links = [];
        this.zoom = null;
        
        this.init();
    }
    
    init() {
        this.setupDimensions();
        this.setupSVG();
        this.setupData();
        this.setupSimulation();
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
        
        // 노드 데이터 준비
        this.nodes = window.canvasData.nodes.map(node => ({
            id: node.id,
            type: node.type,
            text: node.text || '',
            file: node.file || null,
            originalX: node.x,
            originalY: node.y,
            width: node.width,
            height: node.height,
            // D3 simulation을 위한 속성들
            x: node.x,
            y: node.y,
            fx: null, // 고정 위치 (드래그 시 사용)
            fy: null
        }));
        
        // 링크 데이터 준비
        this.links = window.canvasData.edges.map(edge => ({
            id: edge.id,
            source: edge.fromNode,
            target: edge.toNode,
            fromSide: edge.fromSide || null,
            toSide: edge.toSide || null
        }));
    }
    
    setupSimulation() {
        this.simulation = d3.forceSimulation(this.nodes)
            .force('link', d3.forceLink(this.links)
                .id(d => d.id)
                .distance(120)
                .strength(0.5))
            .force('charge', d3.forceManyBody()
                .strength(-300)
                .distanceMax(400))
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))
            .force('collision', d3.forceCollide()
                .radius(d => Math.max(d.width, d.height) / 2 + 10))
            .alphaTarget(0.1)
            .on('tick', () => this.ticked());
    }
    
    render() {
        // 링크 렌더링
        const links = this.g.selectAll('.link')
            .data(this.links)
            .join('line')
            .attr('class', 'link')
            .style('stroke', '#999')
            .style('stroke-width', 2)
            .style('stroke-opacity', 0.6);
            
        // 노드 그룹 생성
        const nodeGroups = this.g.selectAll('.node-group')
            .data(this.nodes)
            .join('g')
            .attr('class', 'node-group')
            .style('cursor', 'pointer')
            .call(this.setupDrag());
            
        // 노드 배경 (카드 스타일)
        nodeGroups.append('rect')
            .attr('class', 'node-bg')
            .attr('width', d => d.width)
            .attr('height', d => d.height)
            .attr('x', d => -d.width / 2)
            .attr('y', d => -d.height / 2)
            .attr('rx', 8)
            .style('fill', d => this.getNodeColor(d.type))
            .style('stroke', '#ddd')
            .style('stroke-width', 2)
            .style('filter', 'drop-shadow(2px 2px 4px rgba(0,0,0,0.1))')
            .on('click', (event, d) => {
                event.stopPropagation();
                this.showNodeDetails(d);
            });
            
        // 노드 텍스트
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
            .style('font-size', '12px')
            .style('line-height', '1.3')
            .style('color', '#333')
            .style('overflow', 'hidden')
            .style('word-wrap', 'break-word')
            .html(d => this.formatNodeText(d.text));
    }
    
    setupDrag() {
        return d3.drag()
            .on('start', (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            })
            .on('drag', (event, d) => {
                d.fx = event.x;
                d.fy = event.y;
            })
            .on('end', (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0.1);
                // 드래그 종료 후에도 위치 고정 유지 (더블클릭으로 해제 가능)
            });
    }
    
    ticked() {
        // 링크 위치 업데이트
        this.g.selectAll('.link')
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
            
        // 노드 위치 업데이트
        this.g.selectAll('.node-group')
            .attr('transform', d => `translate(${d.x}, ${d.y})`);
    }
    
    getNodeColor(type) {
        const colors = {
            'text': '#f0f8ff',
            'file': '#f0fff0',
            'link': '#fff8dc',
            'group': '#fdf5e6'
        };
        return colors[type] || '#ffffff';
    }
    
    formatNodeText(text) {
        if (!text) return '';
        
        // 긴 텍스트는 줄임표 처리
        if (text.length > 100) {
            return text.substring(0, 97) + '...';
        }
        
        // HTML 이스케이프
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
            details += `<strong>Content:</strong><br>${node.text.replace(/\n/g, '<br>')}<br>`;
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
        
        // 모든 노드의 경계 계산
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
        
        const scale = Math.min(
            (this.width * 0.8) / width,
            (this.height * 0.8) / height,
            1
        );
        
        const transform = d3.zoomIdentity
            .translate(this.width / 2, this.height / 2)
            .scale(scale)
            .translate(-centerX, -centerY);
            
        this.svg.transition()
            .duration(750)
            .call(this.zoom.transform, transform);
    }
    
    handleResize() {
        this.setupDimensions();
        
        this.svg
            .attr('width', this.width)
            .attr('height', this.height);
            
        this.simulation
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))
            .alpha(0.3)
            .restart();
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