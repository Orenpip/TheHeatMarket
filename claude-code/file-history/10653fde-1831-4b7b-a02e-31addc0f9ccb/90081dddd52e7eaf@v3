"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import * as d3 from "d3";
import MapNodeDetail from "./MapNodeDetail";
import MapSearchBar from "./MapSearchBar";
import MapLegend from "./MapLegend";

interface MapNode {
  id: string;
  type: string;
  label: string;
  description: string | null;
  metadata: Record<string, unknown>;
  similarity?: number;
  isPersonalized?: boolean;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
  vx?: number;
  vy?: number;
}

interface MapEdge {
  source: string | MapNode;
  target: string | MapNode;
  weight: number;
  edgeType: string;
  id?: string;
}

const NODE_COLORS: Record<string, string> = {
  CAREER: "#3B82F6",
  MAJOR: "#8B5CF6",
  INDUSTRY: "#10B981",
  PROGRAM: "#F59E0B",
  SKILL: "#EF4444",
  VALUE: "#EC4899",
};

const NODE_SIZES: Record<string, number> = {
  INDUSTRY: 18,
  CAREER: 12,
  MAJOR: 12,
  PROGRAM: 10,
  SKILL: 8,
  VALUE: 8,
};

export default function MapCanvas() {
  const svgRef = useRef<SVGSVGElement>(null);
  const [nodes, setNodes] = useState<MapNode[]>([]);
  const [edges, setEdges] = useState<MapEdge[]>([]);
  const [selectedNode, setSelectedNode] = useState<MapNode | null>(null);
  const [personalized, setPersonalized] = useState(true);
  const [loading, setLoading] = useState(true);
  const simulationRef = useRef<d3.Simulation<MapNode, MapEdge> | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const endpoint = personalized ? "/api/map/personalized" : "/api/map/nodes";
      const res = await fetch(endpoint);
      if (!res.ok) return;

      const data = await res.json() as { nodes?: MapNode[]; edges?: MapEdge[] } | MapNode[];

      if (Array.isArray(data)) {
        setNodes(data);
        // Fetch edges separately
        const edgesRes = await fetch(
          "/api/map/personalized"
        );
        if (edgesRes.ok) {
          const edgeData = await edgesRes.json() as { edges: MapEdge[] };
          setEdges(edgeData.edges ?? []);
        }
      } else {
        setNodes(data.nodes ?? []);
        setEdges(data.edges ?? []);
      }
    } finally {
      setLoading(false);
    }
  }, [personalized]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    if (!svgRef.current || nodes.length === 0) return;

    const container = svgRef.current.parentElement!;
    const width = container.clientWidth;
    const height = container.clientHeight;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    svg
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height]);

    // Zoom/pan
    const g = svg.append("g");

    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.2, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform.toString());
      });

    svg.call(zoom);

    // D3 Force Simulation
    const simulation = d3
      .forceSimulation<MapNode>(nodes)
      .force(
        "link",
        d3
          .forceLink<MapNode, MapEdge>(edges as MapEdge[])
          .id((d) => d.id)
          .distance((d) => 80 + (1 - (d.weight ?? 0.5)) * 60)
          .strength(0.3)
      )
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force(
        "collision",
        d3.forceCollide<MapNode>().radius((d) => (NODE_SIZES[d.type] ?? 10) + 15)
      );

    simulationRef.current = simulation;

    // Draw edges
    const link = g
      .append("g")
      .selectAll("line")
      .data(edges)
      .join("line")
      .attr("stroke", "rgba(0,0,0,0.08)")
      .attr("stroke-width", (d) => Math.max(0.5, (d.weight ?? 0.5) * 2))
      .attr("class", "map-edge");

    // Draw nodes
    const nodeGroup = g
      .append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("class", "map-node")
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .call(
        d3
          .drag<SVGGElement, MapNode>()
          .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          }) as any
      )
      .on("click", (_event, d) => {
        setSelectedNode(d);
      });

    // Node circles
    nodeGroup
      .append("circle")
      .attr("r", (d) => {
        const base = NODE_SIZES[d.type] ?? 10;
        const boost = d.similarity ? d.similarity * 8 : 0;
        return base + boost;
      })
      .attr("fill", (d) => NODE_COLORS[d.type] ?? "#6B7280")
      .attr("fill-opacity", (d) => (d.isPersonalized ? 0.9 : 0.6))
      .attr("stroke", (d) => (d.isPersonalized ? "white" : "none"))
      .attr("stroke-width", 2)
      .style("cursor", "pointer")
      .style("filter", (d) =>
        d.isPersonalized
          ? `drop-shadow(0 0 6px ${NODE_COLORS[d.type] ?? "#3B82F6"}66)`
          : "none"
      );

    // Node labels
    nodeGroup
      .append("text")
      .attr("y", (d) => (NODE_SIZES[d.type] ?? 10) + 12)
      .attr("text-anchor", "middle")
      .attr("font-size", "10px")
      .attr("font-family", "Inter, system-ui, sans-serif")
      .attr("fill", "#1A1A2E")
      .attr("pointer-events", "none")
      .text((d) =>
        d.label.length > 20 ? d.label.slice(0, 18) + "..." : d.label
      );

    // Simulation tick
    simulation.on("tick", () => {
      link
        .attr("x1", (d) => (typeof d.source === "object" ? d.source.x ?? 0 : 0))
        .attr("y1", (d) => (typeof d.source === "object" ? d.source.y ?? 0 : 0))
        .attr("x2", (d) => (typeof d.target === "object" ? d.target.x ?? 0 : 0))
        .attr("y2", (d) => (typeof d.target === "object" ? d.target.y ?? 0 : 0));

      nodeGroup.attr("transform", (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
    });

    return () => {
      simulation.stop();
    };
  }, [nodes, edges]);

  async function handleSearch(query: string) {
    if (!query.trim()) {
      fetchData();
      return;
    }

    const res = await fetch(
      `/api/map/search?q=${encodeURIComponent(query)}`
    );
    if (res.ok) {
      const results = await res.json() as MapNode[];
      setNodes(results);
      setEdges([]);
    }
  }

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-3 animate-spin">🧭</div>
          <p className="text-[#6B7280] text-sm">Loading your map...</p>
        </div>
      </div>
    );
  }

  if (nodes.length === 0) {
    return (
      <div className="h-screen flex items-center justify-center bg-gradient-to-br from-[#F2F4F7] to-[#E8EBF0]">
        <div className="text-center max-w-sm px-6">
          <div className="text-5xl mb-4">🗺️</div>
          <h2 className="text-xl font-bold text-[#1A1A2E] mb-2">
            Map is being built
          </h2>
          <p className="text-sm text-[#6B7280] mb-4">
            The career and education map will populate as you complete
            reflections and build your signal profile. Check back after your
            first reflection!
          </p>
          <a
            href="/reflect"
            className="inline-block px-5 py-2.5 bg-[#3B82F6] text-white rounded-xl text-sm font-medium hover:bg-[#2563EB] transition-colors"
          >
            Start a Reflection
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-screen overflow-hidden bg-gradient-to-br from-[#F2F4F7] to-[#E8EBF0]">
      {/* Controls */}
      <div className="absolute top-4 left-4 right-4 z-20 flex items-start gap-3">
        <MapSearchBar onSearch={handleSearch} />

        <button
          onClick={() => setPersonalized(!personalized)}
          className={`flex-shrink-0 px-4 py-2.5 rounded-xl text-sm font-medium glass-card transition-all ${
            personalized
              ? "text-[#3B82F6] border-blue-200/60"
              : "text-[#6B7280]"
          }`}
        >
          {personalized ? "✨ Personalized" : "All Nodes"}
        </button>
      </div>

      {/* D3 Canvas */}
      <svg ref={svgRef} className="w-full h-full" />

      {/* Legend */}
      <div className="absolute bottom-24 left-4 z-20">
        <MapLegend />
      </div>

      {/* Node Detail Panel */}
      {selectedNode && (
        <MapNodeDetail
          node={selectedNode}
          onClose={() => setSelectedNode(null)}
        />
      )}
    </div>
  );
}
