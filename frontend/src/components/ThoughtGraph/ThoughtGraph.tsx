import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { ThoughtNode, ReasoningEdge } from '../../types/reasoning';
import './ThoughtGraph.css';

interface ThoughtGraphProps {
  nodes: ThoughtNode[];
  edges: ReasoningEdge[];
  onNodeClick?: (node: ThoughtNode) => void;
}

export const ThoughtGraph: React.FC<ThoughtGraphProps> = ({ nodes, edges, onNodeClick }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [dimensions] = useState({ width: 900, height: 600 });

  useEffect(() => {
    if (!svgRef.current || nodes.length === 0) return;

    // Clear previous visualization
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current);
    const { width, height } = dimensions;

    // Create container group for zoom/pan
    const g = svg.append('g');

    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.3, 3])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom as any);

    // Color mapping based on thought type
    const colorMap: Record<string, string> = {
      question: '#3b82f6',     // Blue
      retrieval: '#10b981',    // Green
      reasoning: '#f59e0b',    // Orange
      conclusion: '#ef4444'    // Red
    };

    // Create copies of data for D3
    const nodeData = nodes.map(n => ({ ...n }));
    const edgeData = edges.map(e => ({
      ...e,
      source: e.source_id,
      target: e.target_id
    }));

    // Create force simulation
    const simulation = d3.forceSimulation(nodeData as any)
      .force('link', d3.forceLink(edgeData as any)
        .id((d: any) => d.id)
        .distance(150)
      )
      .force('charge', d3.forceManyBody().strength(-400))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(50));

    // Create arrow markers for edges
    svg.append('defs').selectAll('marker')
      .data(['arrow'])
      .join('marker')
      .attr('id', 'arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 25)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#999');

    // Draw edges
    const links = g.append('g')
      .selectAll('line')
      .data(edgeData)
      .join('line')
      .attr('stroke', '#999')
      .attr('stroke-width', 2)
      .attr('marker-end', 'url(#arrow)');

    // Draw edge labels
    const linkLabels = g.append('g')
      .selectAll('text')
      .data(edgeData)
      .join('text')
      .text(d => d.label)
      .attr('font-size', '10px')
      .attr('fill', '#666')
      .attr('text-anchor', 'middle');

    // Draw nodes
    const nodeGroups = g.append('g')
      .selectAll('g')
      .data(nodeData)
      .join('g')
      .attr('cursor', 'pointer')
      .call(d3.drag<any, any>()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded) as any
      );

    // Node circles
    nodeGroups.append('circle')
      .attr('r', (d: any) => 15 + (d.confidence * 20))
      .attr('fill', (d: any) => colorMap[d.type] || '#gray')
      .attr('stroke', '#fff')
      .attr('stroke-width', 3)
      .on('click', (event, d) => {
        event.stopPropagation();
        if (onNodeClick) onNodeClick(d as ThoughtNode);
      });

    // Node labels (type)
    nodeGroups.append('text')
      .text((d: any) => d.type)
      .attr('text-anchor', 'middle')
      .attr('dy', -40)
      .attr('font-size', '12px')
      .attr('font-weight', 'bold')
      .attr('fill', (d: any) => colorMap[d.type] || '#gray');

    // Confidence labels
    nodeGroups.append('text')
      .text((d: any) => `${Math.round(d.confidence * 100)}%`)
      .attr('text-anchor', 'middle')
      .attr('dy', 45)
      .attr('font-size', '10px')
      .attr('fill', '#666');

    // Update positions on simulation tick
    simulation.on('tick', () => {
      links
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      linkLabels
        .attr('x', (d: any) => (d.source.x + d.target.x) / 2)
        .attr('y', (d: any) => (d.source.y + d.target.y) / 2);

      nodeGroups.attr('transform', (d: any) => `translate(${d.x},${d.y})`);
    });

    // Drag functions
    function dragStarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: any, d: any) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragEnded(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Cleanup
    return () => {
      simulation.stop();
    };

  }, [nodes, edges, dimensions, onNodeClick]);

  return (
    <div className="thought-graph-container">
      <div className="graph-legend">
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#3b82f6' }}></div>
          <span>Question</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#10b981' }}></div>
          <span>Retrieval</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#f59e0b' }}></div>
          <span>Reasoning</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#ef4444' }}></div>
          <span>Conclusion</span>
        </div>
      </div>
      <svg
        ref={svgRef}
        width={dimensions.width}
        height={dimensions.height}
        style={{ border: '1px solid #ddd', borderRadius: '8px', background: '#fafafa' }}
      />
      <div className="graph-controls">
        <p>🖱️ Drag nodes • 🔍 Scroll to zoom • 👆 Click node for details</p>
      </div>
    </div>
  );
};
