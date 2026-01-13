"use client";

import {DataTable} from "@/components/data-table";
import {DataQueryCard} from "@/components/data-query";
import {AgentState} from "@/lib/types";
import {useCoAgent, useRenderToolCall} from "@copilotkit/react-core";
import {CopilotSidebar} from "@copilotkit/react-ui";

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
            title: "What are top performing territories?",
            message: "What are top performing territories?",
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
    name: "my_agent",
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

  return (
    <div className="h-screen flex justify-center items-center flex-col bg-indigo-500">
      <DataTable state={state} />
    </div>
  );
}
