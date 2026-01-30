import type { Metadata } from "next";

import { CopilotKit } from "@copilotkit/react-core";
import "./globals.css";
import "@copilotkit/react-ui/styles.css";

const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";

export const metadata: Metadata = {
  title: "Data Agent",
  description: "Chat with your data using Snow Leopard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={"antialiased"}>
        <CopilotKit
          runtimeUrl={`${basePath}/api/copilotkit`}
          agent="data_agent"
          showDevConsole={false}
          enableInspector={false}
        >
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
