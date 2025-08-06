import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

interface Node {
  id: string;
  name: string;
  type: "badge" | "course";
  level: "basic" | "intermediate" | "expert";
}

interface Link {
  source: string;
  target: string;
  type: "prerequisite" | "contributes";
}

interface SkillTreeProps {
  nodes: Node[];
  links: Link[];
  width?: number;
  height?: number;
}

const SkillTree: React.FC<SkillTreeProps> = ({
  nodes,
  links,
  width = 1200,
  height = 800,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !nodes.length) return;

    // Clear previous content
    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current);
    const g = svg.append("g");

    // Create zoom behavior
    const zoom = d3
      .zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    svg.call(zoom as any);

    // Create force simulation
    const simulation = d3
      .forceSimulation()
      .force(
        "link",
        d3
          .forceLink()
          .id((d: any) => d.id)
          .distance(100)
      )
      .force("charge", d3.forceManyBody().strength(-1000))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(50));

    // Create links
    const link = g
      .append("g")
      .selectAll("line")
      .data(links)
      .enter()
      .append("line")
      .attr("stroke", (d) => (d.type === "prerequisite" ? "#999" : "#666"))
      .attr("stroke-width", (d) => (d.type === "prerequisite" ? 1 : 2))
      .attr("stroke-dasharray", (d) =>
        d.type === "prerequisite" ? "5,5" : "none"
      );

    // Create nodes
    const node = g
      .append("g")
      .selectAll("g")
      .data(nodes)
      .enter()
      .append("g")
      .call(
        d3
          .drag()
          .on("start", dragStarted)
          .on("drag", dragged)
          .on("end", dragEnded) as any
      );

    // Add circles for nodes
    node
      .append("circle")
      .attr("r", 30)
      .attr("fill", (d) => getNodeColor(d.type, d.level));

    // Add text labels
    node
      .append("text")
      .text((d) => d.name)
      .attr("text-anchor", "middle")
      .attr("dy", ".3em")
      .attr("fill", "#fff")
      .style("font-size", "12px");

    // Update simulation
    simulation.nodes(nodes as any).on("tick", ticked);

    (simulation.force("link") as any).links(links);

    function ticked() {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      node.attr("transform", (d: any) => `translate(${d.x},${d.y})`);
    }

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
  }, [nodes, links, width, height]);

  return (
    <svg
      ref={svgRef}
      width={width}
      height={height}
      style={{ border: "1px solid #ccc" }}
    />
  );
};

function getNodeColor(type: string, level: string): string {
  if (type === "badge") {
    switch (level) {
      case "basic":
        return "#4CAF50";
      case "intermediate":
        return "#2196F3";
      case "expert":
        return "#9C27B0";
      default:
        return "#666";
    }
  }
  return "#FF9800"; // course color
}

export default SkillTree;
