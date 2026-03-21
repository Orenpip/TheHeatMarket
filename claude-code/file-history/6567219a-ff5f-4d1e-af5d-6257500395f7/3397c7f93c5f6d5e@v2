export type MapNodeType =
  | "CAREER"
  | "MAJOR"
  | "INDUSTRY"
  | "PROGRAM"
  | "SKILL"
  | "VALUE";

export type EdgeType = "REQUIRES" | "LEADS_TO" | "RELATED" | "ALTERNATIVE";

export interface MapNodeMetadata {
  medianSalary?: string;
  growthRate?: string;
  educationRequired?: string;
  skills?: string[];
  entryPaths?: string[];
  dayInTheLife?: string;
  university?: string;
  location?: string;
  deadline?: string;
  // extensible
  [key: string]: unknown;
}

export interface MapNode {
  id: string;
  type: MapNodeType;
  label: string;
  description?: string;
  metadata: MapNodeMetadata;
  parentId?: string;
  createdAt: Date;
  updatedAt: Date;
  // injected by personalized query
  similarity?: number;
  isPersonalized?: boolean;
  isNew?: boolean;
}

export interface MapEdge {
  id: string;
  sourceId: string;
  targetId: string;
  weight: number;
  edgeType: EdgeType;
}

export interface MapNodeWithEdges extends MapNode {
  outEdges: MapEdge[];
  inEdges: MapEdge[];
  children?: MapNode[];
}

export interface PersonalizedMapData {
  nodes: MapNode[];
  edges: MapEdge[];
  personalizedNodeIds: string[];
  studentBreadthScore?: number;
}

export interface D3Node extends MapNode {
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
  vx?: number;
  vy?: number;
}

export interface D3Edge {
  source: string | D3Node;
  target: string | D3Node;
  weight: number;
  edgeType: EdgeType;
}
