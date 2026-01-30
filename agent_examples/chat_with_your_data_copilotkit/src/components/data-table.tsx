import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./charts/card";

// Component to display a data table from rows
export function DataTable({rows, query}: {
  rows: Array<Record<string, unknown>>;
  query: string;
}) {
  if (!rows || rows.length === 0) {
    return (
      <Card className="w-full">
        <CardContent className="py-6">
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
            <CardTitle className="text-base font-medium mb-2">No Data Yet</CardTitle>
            <CardDescription className="text-xs">Ask a question about your sales data to get started!</CardDescription>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader className="pb-1 pt-3">
        <CardTitle className="text-base font-medium">Query Results</CardTitle>
        <CardDescription className="text-xs">{rows.length} rows returned</CardDescription>
      </CardHeader>
      <CardContent className="p-3">
        <div className="mb-3">
          <p className="text-xs font-medium text-gray-500 mb-1">SQL Query:</p>
          <div className="bg-gray-100 p-2 rounded text-xs font-mono overflow-x-auto text-gray-800 border border-gray-200">
            {query}
          </div>
        </div>

        <div className="overflow-auto max-h-[600px] border border-gray-200 rounded-lg">
          <table className="w-full text-sm">
            <thead className="bg-gray-100 sticky top-0">
              <tr>
                {Object.keys(rows[0] || {}).map((col) => (
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
              {rows.map((row, idx) => (
                <tr
                  key={idx}
                  className={`border-b border-gray-200 hover:bg-gray-50 ${
                    idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'
                  }`}
                >
                  {Object.values(row).map((val: unknown, colIdx) => (
                    <td key={colIdx} className="p-3 text-gray-800">
                      {val !== null && val !== undefined ? String(val) : '—'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}