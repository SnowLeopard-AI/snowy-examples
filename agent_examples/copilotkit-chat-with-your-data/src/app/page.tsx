"use client";

import dynamic from "next/dynamic";
import {DataTable} from "@/components/data-table";
import {DataQueryCard} from "@/components/data-query";
import {Dashboard} from "@/components/Dashboard";
import {AgentState} from "@/lib/types";
import {useCoAgent, useRenderToolCall} from "@copilotkit/react-core";

const CopilotSidebar = dynamic(
  () => import("@copilotkit/react-ui").then((mod) => mod.CopilotSidebar),
  { ssr: false }
);

export default function CopilotKitPage() {
  return (
    <main>
      <CopilotSidebar
        defaultOpen={true}
        disableSystemMessage={true}
        clickOutsideToClose={false}
        labels={{
          title: "Popup Assistant",
          initial: "👋 Hi, there! You're chatting with an agent.",
        }}
        suggestions={[
          {
            title: "Which customers have placed the highest number of orders?",
            message: "Which customers have placed the highest number of orders?",
          },
          {
            title: "What are the top 20 performing territories by revenue?",
            message: "What are top 20 performing territories by revenue?",
          },
        ]}
      >
        <YourMainContent />
      </CopilotSidebar>
    </main>
  );
}

function YourMainContent() {
  // 🪁 Shared State: https://docs.copilotkit.ai/pydantic-ai/shared-state
  const { state } = useCoAgent<AgentState>({
    name: "data_agent",
    initialState: {},
  });

  useRenderToolCall({
    name: "get_data",
    description: "Retrieve data from Northwind dataset with natural language queries.",
    parameters: [{ name: "human_query", type: "string", required: true }],
    render: ({ result }) => {
      return (
        <DataQueryCard
          query={result?.sql_query}
          numRows={result?.num_rows}
          dataPreview={result?.data_top}
        />
      );
    },
  });

  // Get the last query from data_responses
  const dataResponses = state.data_responses || {};
  const toolCallIds = Object.keys(dataResponses);
  const lastToolCallId = toolCallIds[toolCallIds.length - 1];
  const lastQuery = lastToolCallId ? dataResponses[lastToolCallId] : null;

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Dashboard />
      {lastQuery && (
        <div className="p-4">
          <DataTable rows={lastQuery.rows} query={lastQuery.query} />
        </div>
      )}
    </div>
  );
}
