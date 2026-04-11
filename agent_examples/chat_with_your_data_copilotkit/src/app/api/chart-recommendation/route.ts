import { NextRequest, NextResponse } from "next/server";

const agentUrl = process.env.AGENT_URL || "http://localhost:8000/";

export async function POST(req: NextRequest) {
  const body = await req.json();
  const res = await fetch(new URL("/chart-recommendation", agentUrl), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
