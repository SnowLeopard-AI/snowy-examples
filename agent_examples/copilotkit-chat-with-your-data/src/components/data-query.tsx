import { useState } from "react";
import Image from "next/image";

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
}: {
  query?: string;
  numRows?: number;
  dataPreview?: object[];
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div
      className="rounded-xl shadow-sm mt-6 mb-4 mr-3 bg-white"
      style={{ border: '1px solid #E3E3E3' }}
    >
      <div className="p-4 w-full">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center justify-between w-full text-left hover:bg-gray-50 -m-2 p-2 rounded transition-colors cursor-pointer"
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
                {numRows !== undefined ? `${numRows} rows returned` : 'Loading...'}
              </p>
            </div>
          </div>
          <ChevronIcon isExpanded={isExpanded} />
        </button>

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

            {dataPreview && dataPreview.length > 0 && (
              <div className="mt-4">
                <p className="text-xs font-medium mb-2">Preview (Top {dataPreview.length} Rows)</p>
                <div
                  className="rounded overflow-x-auto max-h-64 overflow-y-auto"
                  style={{ border: '1px solid #E3E3E3' }}
                >
                  <table className="w-full text-xs">
                    <thead className="sticky top-0" style={{ backgroundColor: '#F5F5F5' }}>
                      <tr>
                        {Object.keys(dataPreview[0] || {}).map((col) => (
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
                      {dataPreview.map((row, idx) => (
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

                <div className="mt-4 flex flex-col items-center gap-3">
                  <button
                    className="px-4 py-2 rounded-full text-sm font-medium transition-colors hover:opacity-90 cursor-pointer"
                    style={{ backgroundColor: '#9DEDEB' }}
                    onClick={() => {
                      document.getElementById('query-results')?.scrollIntoView({ behavior: 'smooth' });
                    }}
                  >
                    See full results
                  </button>
                  <p className="text-sm" style={{ color: '#8D8A8A' }}>
                    Data powered by <a href="https://www.snowleopard.ai/" target="_blank" className="underline">snowleopard.ai</a>
                  </p>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
