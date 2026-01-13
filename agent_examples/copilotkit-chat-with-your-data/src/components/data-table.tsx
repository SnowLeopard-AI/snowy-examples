import { AgentState } from "@/lib/types";

// Component to display the full data table from the last query
export function DataTable({ state }: { state: AgentState }) {
  // Get the last query from data_responses
  const dataResponses = state.data_responses || {};
  const toolCallIds = Object.keys(dataResponses);

  if (toolCallIds.length === 0) {
    return (
      <div className="bg-white/90 rounded-xl shadow-2xl p-8 max-w-6xl w-full mx-4">
        <div className="text-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            className="w-16 h-16 mx-auto mb-4 text-gray-400"
          >
            <ellipse cx="12" cy="5" rx="9" ry="3" strokeWidth="2" />
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" strokeWidth="2" />
            <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3" strokeWidth="2" />
          </svg>
          <h2 className="text-2xl font-bold text-gray-700 mb-2">No Data Yet</h2>
          <p className="text-gray-500">Ask a question about your sales data to get started!</p>
        </div>
      </div>
    );
  }

  // Get the last query (most recent tool call)
  const lastToolCallId = toolCallIds[toolCallIds.length - 1];
  const lastQuery = dataResponses[lastToolCallId];

  if (!lastQuery || !lastQuery.rows || lastQuery.rows.length === 0) {
    return (
      <div className="bg-white/90 rounded-xl shadow-2xl p-8 max-w-6xl w-full mx-4">
        <div className="text-center">
          <p className="text-gray-500">No data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white/90 rounded-xl shadow-2xl p-6 max-w-6xl w-full mx-4">
      <div className="mb-4">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Query Results</h2>
        <p className="text-sm text-gray-600 mb-3">
          {lastQuery.rows.length} rows returned
        </p>

        {lastQuery.query && (
          <div className="mb-4">
            <p className="text-xs font-semibold text-gray-700 mb-1">SQL Query:</p>
            <div className="bg-gray-100 p-3 rounded text-xs font-mono overflow-x-auto text-gray-800 border border-gray-200">
              {lastQuery.query}
            </div>
          </div>
        )}
      </div>

      <div className="overflow-auto max-h-[600px] border border-gray-200 rounded-lg">
        <table className="w-full text-sm">
          <thead className="bg-gray-100 sticky top-0">
            <tr>
              {Object.keys(lastQuery.rows[0] || {}).map((col) => (
                <th
                  key={col}
                  className="text-left p-3 text-gray-700 font-semibold border-b-2 border-gray-300"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {lastQuery.rows.map((row, idx) => (
              <tr
                key={idx}
                className={`border-b border-gray-200 hover:bg-gray-50 ${
                  idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'
                }`}
              >
                {Object.values(row).map((val: any, colIdx) => (
                  <td key={colIdx} className="p-3 text-gray-800">
                    {val !== null && val !== undefined ? String(val) : '—'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}