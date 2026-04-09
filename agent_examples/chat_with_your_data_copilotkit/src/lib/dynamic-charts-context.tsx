"use client";

import { createContext, useContext, useState, useCallback, useRef, ReactNode } from "react";
import { DynamicChart } from "./types";

interface DynamicChartsContextValue {
  charts: DynamicChart[];
  addChart: (chart: Omit<DynamicChart, "colorIndex">) => void;
  removeChart: (id: string) => void;
}

const DynamicChartsContext = createContext<DynamicChartsContextValue | null>(null);

export function DynamicChartsProvider({ children }: { children: ReactNode }) {
  const [charts, setCharts] = useState<DynamicChart[]>([]);
  const colorCounter = useRef(0);

  const addChart = useCallback((chart: Omit<DynamicChart, "colorIndex">) => {
    const colorIndex = colorCounter.current++;
    setCharts((prev) => [{ ...chart, colorIndex }, ...prev]);
  }, []);

  const removeChart = useCallback((id: string) => {
    setCharts((prev) => prev.filter((c) => c.id !== id));
  }, []);

  return (
    <DynamicChartsContext.Provider value={{ charts, addChart, removeChart }}>
      {children}
    </DynamicChartsContext.Provider>
  );
}

export function useDynamicCharts() {
  const ctx = useContext(DynamicChartsContext);
  if (!ctx) throw new Error("useDynamicCharts must be used within DynamicChartsProvider");
  return ctx;
}
