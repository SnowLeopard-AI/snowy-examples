// State of the agent, make sure this aligns with your agent's state.

type SchemaData = {
  query: string;
  rows: Record<string, unknown>[];
  columns?: string[];
};

export type AgentState = {
  data_responses?: Record<string, SchemaData>;
  last_tool_call_id?: string;
}

// Dynamic chart types

export type ChartType = "bar" | "area" | "line" | "donut";

export interface ChartRecommendation {
  chart_type: ChartType;
  index: string;
  categories: string[];
  title: string;
  description: string;
  layout?: "horizontal" | "vertical";
  pivot_column?: string;
}

export interface DynamicChart {
  id: string;
  colorIndex: number;
  recommendation: ChartRecommendation;
  data: Record<string, unknown>[];
}