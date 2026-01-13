"use client";

import {DataTable} from "@/components/data-table";
import {DataQueryCard} from "@/components/data-query";
import {AgentState} from "@/lib/types";
import {useCoAgent, useFrontendTool, useRenderToolCall,} from "@copilotkit/react-core";
import {CopilotKitCSSProperties, CopilotSidebar} from "@copilotkit/react-ui";
import {useState} from "react";

export default function CopilotKitPage() {
  const [themeColor, setThemeColor] = useState("#6366f1");

  // 🪁 Frontend Actions: https://docs.copilotkit.ai/pydantic-ai/frontend-actions
  useFrontendTool({
    name: "setThemeColor",
    parameters: [
      {
        name: "themeColor",
        description: "The theme color to set. Make sure to pick nice colors.",
        required: true,
      },
    ],
    handler({ themeColor }) {
      setThemeColor(themeColor);
    },
  });

  return (
    <main
      style={
        { "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties
      }
    >
      <CopilotSidebar
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
        <YourMainContent themeColor={themeColor} />
      </CopilotSidebar>
    </main>
  );
}

function YourMainContent({ themeColor }: { themeColor: string }) {
  // 🪁 Shared State: https://docs.copilotkit.ai/pydantic-ai/shared-state
  const { state } = useCoAgent<AgentState>({
    name: "my_agent",
    initialState: {},
  });

  useRenderToolCall(
    {
      name: "get_data",
      description: "Retrieve data from Northwind dataset with natural language queries.",
      parameters: [{ name: "human_query", type: "string", required: true }],
      render: ({ args, result }) => {
        return (
          <DataQueryCard
            query={result?.sql_query}
            numRows={result?.num_rows}
            dataPreview={result?.data_top}
            themeColor={themeColor}
          />
        );
      },
    },
    [themeColor],
  );

  return (
    <div
      style={{ backgroundColor: themeColor }}
      className="h-screen flex justify-center items-center flex-col transition-colors duration-300"
    >
      <DataTable state={state} />
    </div>
  );
}
