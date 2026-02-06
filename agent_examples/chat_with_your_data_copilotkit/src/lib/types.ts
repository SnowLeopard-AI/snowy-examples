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