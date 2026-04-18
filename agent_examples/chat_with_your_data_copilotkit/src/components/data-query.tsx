import { useRef, useState } from "react";
import Image from "next/image";
import { useDynamicCharts } from "@/lib/dynamic-charts-context";
import { ChartRecommendation } from "@/lib/types";

const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";

// Chevron icon for expand/collapse
function ChevronIcon({ isExpanded }: { isExpanded: boolean }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
      style={{ color: '#8D8A8A' }}
    >
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
    </svg>
  );
}

// Data read card component that displays additional rows from a previous query
export function DataReadCard({
  rows,
  window,
  totalRows,
}: {
  rows?: object[];
  window?: [number, number];
  totalRows?: number;
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  const startRow = window?.[0] ?? 0;
  const endRow = window?.[1] ?? (rows?.length ?? 0);
  const total = totalRows ?? rows?.length ?? 0;

  return (
    <div
      className="rounded-xl shadow-sm mt-2 mb-4 mr-3 bg-white"
      style={{ border: '1px solid #E3E3E3' }}
    >
      <div className="p-4 w-full">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center justify-between w-full text-left hover:bg-gray-50 -m-2 p-2 rounded transition-colors cursor-pointer"
        >
          <p className="text-sm" style={{ color: '#8D8A8A' }}>
            Reading rows {startRow} - {endRow} of {total}
          </p>
          <ChevronIcon isExpanded={isExpanded} />
        </button>

        {isExpanded && rows && rows.length > 0 && (
          <div className="mt-4">
            <div
              className="rounded overflow-x-auto max-h-64 overflow-y-auto"
              style={{ border: '1px solid #E3E3E3' }}
            >
              <table className="w-full text-xs">
                <thead className="sticky top-0" style={{ backgroundColor: '#F5F5F5' }}>
                  <tr>
                    {Object.keys(rows[0] || {}).map((col) => (
                      <th
                        key={col}
                        className="text-left p-2 font-medium"
                        style={{ borderBottom: '1px solid #E3E3E3' }}
                      >
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      {Object.values(row).map((val: unknown, colIdx) => (
                        <td key={colIdx} className="p-2">
                          {val !== null && val !== undefined ? String(val) : '—'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Data query card component that displays query results
export function DataQueryCard({
  query,
  numRows,
  dataPreview,
  allData,
  humanQuery,
  error,
}: {
  query?: string;
  numRows?: number;
  dataPreview?: object[];
  allData?: Record<string, unknown>[];
  humanQuery?: string;
  error?: string;
}) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const { charts, addChart } = useDynamicCharts();
  const cardRef = useRef<HTMLDivElement>(null);

  const chartData = allData ?? (dataPreview as Record<string, unknown>[] | undefined);
  const sourceKey = query;
  const isAdded = !!sourceKey && charts.some((c) => c.sourceKey === sourceKey);
  const chartStatus: "idle" | "loading" | "added" = isAdded ? "added" : isLoading ? "loading" : "idle";

  function findScrollParent(el: HTMLElement | null): HTMLElement | null {
    let node = el?.parentElement ?? null;
    while (node) {
      const style = getComputedStyle(node);
      if (/(auto|scroll|overlay)/.test(style.overflowY) && node.scrollHeight > node.clientHeight) {
        return node;
      }
      node = node.parentElement;
    }
    return null;
  }

  function toggleExpanded() {
    if (!query) return;
    const el = cardRef.current;
    const scrollParent = findScrollParent(el);
    const topBefore = el?.getBoundingClientRect().top ?? 0;

    // Nudge the chat container's scrollTop by -1px so CopilotKit's scroll
    // handler flips its "user scrolled up" flag. This prevents its
    // MutationObserver from auto-scrolling to bottom when the card expands.
    // The flag is reset on the next user message, preserving the "jump to
    // bottom on new response" behavior.
    if (scrollParent && scrollParent.scrollTop > 0) {
      scrollParent.scrollTop -= 1;
    }

    setIsExpanded((prev) => !prev);

    requestAnimationFrame(() => {
      if (!el || !scrollParent) return;
      const topAfter = el.getBoundingClientRect().top;
      const diff = topAfter - topBefore;
      if (diff !== 0) scrollParent.scrollTop += diff;
    });
  }

  async function handleAddChart() {
    if (!chartData || chartData.length === 0) return;
    setIsLoading(true);
    try {
      const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";
      const columns = Object.keys(chartData[0]);
      const sampleRows = chartData.slice(0, 10);
      const res = await fetch(`${basePath}/api/chart-recommendation`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ columns, sample_rows: sampleRows, sql_query: query, user_question: humanQuery }),
      });
      const recommendation: ChartRecommendation = await res.json();
      addChart({
        id: crypto.randomUUID(),
        recommendation,
        data: chartData,
        sourceKey,
      });
    } catch (err) {
      console.error("Failed to get chart recommendation", err);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div
      ref={cardRef}
      className="rounded-xl shadow-sm mt-6 mb-4 mr-3 bg-white"
      style={{ border: '1px solid #E3E3E3' }}
    >
      <div className="p-4 w-full">
        <div
          onClick={toggleExpanded}
          role={query ? 'button' : undefined}
          tabIndex={query ? 0 : undefined}
          className={`flex items-center justify-between w-full text-left -m-2 p-2 rounded transition-colors ${query ? 'hover:bg-gray-50 cursor-pointer' : ''}`}
        >
          <div className="flex items-center gap-3 flex-1">
            <Image
              src={`${basePath}/snow-leopard-icon.png`}
              alt="Snow Leopard"
              width={40}
              height={40}
              priority
              style={{ width: 'auto', height: 'auto' }}
            />
            <div>
              <h3 className="text-base font-semibold" style={{ color: '#1a1a1a' }}>Data Query Result</h3>
              <p className="text-sm" style={{ color: '#8D8A8A' }}>
                {numRows !== undefined ? `${numRows} rows returned` : error ? 'Error retrieving data' : 'Loading...'}
              </p>
            </div>
          </div>
          {query && <ChevronIcon isExpanded={isExpanded} />}
        </div>

        {isExpanded && (
          <>
            {query && (
              <div className="mt-4 mb-3">
                <p className="text-xs font-medium mb-2">SQL Query</p>
                <div
                  className="p-3 rounded text-xs font-mono overflow-x-auto"
                  style={{ backgroundColor: '#F5F5F5' }}
                >
                  {query}
                </div>
              </div>
            )}

            {chartData && chartData.length > 0 && (
              <div className="mt-4">
                <p className="text-xs font-medium mb-2">Data ({chartData.length} Rows)</p>
                <div
                  className="rounded overflow-x-auto max-h-64 overflow-y-auto"
                  style={{ border: '1px solid #E3E3E3' }}
                >
                  <table className="w-full text-xs">
                    <thead className="sticky top-0" style={{ backgroundColor: '#F5F5F5' }}>
                      <tr>
                        {Object.keys(chartData[0] || {}).map((col) => (
                          <th
                            key={col}
                            className="text-left p-2 font-medium"
                            style={{borderBottom: '1px solid #E3E3E3' }}
                          >
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {chartData.map((row, idx) => (
                        <tr
                          key={idx}
                          className="hover:bg-gray-50"
                        >
                          {Object.values(row).map((val: unknown, colIdx) => (
                            <td
                              key={colIdx}
                              className="p-2"
                            >
                              {val !== null && val !== undefined ? String(val) : '—'}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="mt-4 flex justify-center">
                  <p className="text-sm" style={{ color: '#8D8A8A' }}>
                    Data powered by <a href="https://www.snowleopard.ai/" target="_blank" className="underline">snowleopard.ai</a>
                  </p>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {chartData && chartData.length > 0 && !error && (
        <div className="px-4 pb-3">
          <button
            onClick={handleAddChart}
            disabled={chartStatus !== "idle"}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            className={`w-full py-2 text-sm font-medium rounded-lg border transition-colors ${
              chartStatus === "added"
                ? "bg-green-50 text-green-700 border-green-200"
                : chartStatus === "loading"
                  ? "bg-gray-50 text-gray-400 border-gray-200"
                  : "cursor-pointer"
            }`}
            style={
              chartStatus === "idle"
                ? {
                    backgroundColor: isHovered ? "#7dd9d7" : "#9dedeb",
                    color: "#1a1a1a",
                    borderColor: "#7dd9d7",
                  }
                : undefined
            }
          >
            {chartStatus === "added"
              ? "Added to Dashboard"
              : chartStatus === "loading"
                ? "Analyzing..."
                : "Add as Chart"}
          </button>
        </div>
      )}
    </div>
  );
}
