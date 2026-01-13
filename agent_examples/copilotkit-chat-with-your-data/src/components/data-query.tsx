import { useState } from "react";

// Database icon for the data query card
function DatabaseIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-12 h-12 text-white/80">
      <ellipse cx="12" cy="5" rx="9" ry="3" strokeWidth="2" />
      <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" strokeWidth="2" />
      <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3" strokeWidth="2" />
    </svg>
  );
}

// Chevron icon for expand/collapse
function ChevronIcon({ isExpanded }: { isExpanded: boolean }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      className={`w-5 h-5 text-white transition-transform ${isExpanded ? 'rotate-180' : ''}`}
    >
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
    </svg>
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
  dataPreview?: any[];
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="rounded-xl shadow-xl mt-6 mb-4 max-w-2xl w-full bg-indigo-500">

      <div className="bg-white/20 p-4 w-full">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center justify-between mb-4 w-full text-left hover:bg-white/10 -m-2 p-2 rounded transition-colors"
        >
          <div className="flex items-center gap-3 flex-1">
            <DatabaseIcon />
            <div>
              <h3 className="text-lg font-bold text-white">Data Query Result</h3>
              <p className="text-white/90 text-sm">
                {numRows !== undefined ? `${numRows} rows returned` : 'Loading...'}
              </p>
            </div>
          </div>
          <ChevronIcon isExpanded={isExpanded} />
        </button>

        {isExpanded && (
          <>
            {query && (
              <div className="mt-3 mb-3">
                <p className="text-white/80 text-xs font-semibold mb-1">SQL Query:</p>
                <div className="bg-black/30 p-2 rounded text-white/90 text-xs font-mono overflow-x-auto">
                  {query}
                </div>
              </div>
            )}

            {dataPreview && dataPreview.length > 0 && (
              <div className="mt-3">
                <p className="text-white/80 text-xs font-semibold mb-2">Preview (Top {dataPreview.length} rows):</p>
                <div className="bg-white/10 rounded overflow-x-auto max-h-64 overflow-y-auto">
                  <table className="w-full text-xs">
                    <thead className="bg-black/20 sticky top-0">
                      <tr>
                        {Object.keys(dataPreview[0] || {}).map((col) => (
                          <th key={col} className="text-left p-2 text-white font-semibold border-b border-white/20">
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {dataPreview.map((row, idx) => (
                        <tr key={idx} className="border-b border-white/10 hover:bg-white/5">
                          {Object.values(row).map((val: any, colIdx) => (
                            <td key={colIdx} className="p-2 text-white/90">
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
          </>
        )}
      </div>
    </div>
  );
}
