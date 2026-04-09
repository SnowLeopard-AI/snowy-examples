"use client";

import {DataQueryCard, DataReadCard} from "@/components/data-query";
import {Dashboard} from "@/components/Dashboard";
import {AgentState} from "@/lib/types";
import {DynamicChartsProvider} from "@/lib/dynamic-charts-context";
import {useCoAgent, useRenderToolCall} from "@copilotkit/react-core";
import {CopilotSidebar} from "@copilotkit/react-ui";

function CustomHeader() {
  return (
    <div className="p-4 border-b border-gray-200">
      <h2 className="text-lg font-semibold">Popup Assistant</h2>
      <p className="text-xs mt-1" style={{ color: '#8D8A8A' }}>
        Data powered by <a href="https://www.snowleopard.ai/" target="_blank" className="underline">snowleopard.ai</a> <a href="https://docs.snowleopard.ai/recipes/copilotkit-data-agent" target="_blank" className="underline">(view cookbook)</a>
      </p>
    </div>
  );
}

export default function CopilotKitPage() {
  return (
    <main>
      <DynamicChartsProvider>
      <CopilotSidebar
        defaultOpen={true}
        clickOutsideToClose={false}
        Header={CustomHeader}
        labels={{
          initial: "👋 Hi, there! You're chatting with a data-agent.",
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
      </DynamicChartsProvider>
    </main>
  );
}

function YourMainContent() {
  // Workaround: useCoAgent state doesn't trigger re-renders in React 19
  // https://github.com/CopilotKit/CopilotKit/issues/2931
  // Force a re-render when the tool call completes so useMemo re-evaluates
  // and picks up the updated agent state from the StateSnapshotEvent.
  useCoAgent<AgentState>({
    name: "data_agent",
    initialState: {},
  });

  useRenderToolCall({
    name: "get_data",
    description: "Retrieve data from Northwind dataset with natural language queries.",
    parameters: [{ name: "human_query", type: "string", required: true }],
    render: ({ result, args }) => {
      return (
        <DataQueryCard
          query={result?.sql_query}
          numRows={result?.num_rows}
          dataPreview={result?.data_top}
          allData={result?.data_top}
          humanQuery={args?.human_query}
          error={typeof result === "string" ? result : undefined}
        />
      );
    },
  });

  useRenderToolCall({
    name: "read_get_data_response",
    description: "Read additional rows from a previous data query.",
    parameters: [
      { name: "tool_call_id", type: "string", required: true },
      { name: "start_row", type: "number", required: false },
      { name: "end_row", type: "number", required: false },
    ],
    render: ({ result }) => {
      return (
        <DataReadCard
          rows={result?.data_window}
          window={result?.window}
          totalRows={result?.total_rows}
        />
      );
    },
  });

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Dashboard />
    </div>
  );
}
