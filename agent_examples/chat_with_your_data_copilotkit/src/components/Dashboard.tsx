"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./charts/card";
import { AreaChart } from "./charts/area-chart";
import { BarChart } from "./charts/bar-chart";
import { DonutChart } from "./charts/pie-chart";
import {
  monthlyRevenueData,
  productPerformanceData,
  categoryDistributionData,
  regionalRevenueData,
  topTerritoriesData,
  calculateTotalRevenue,
  calculateTotalOrders,
  calculateTotalCustomers,
  calculateAverageOrderValue,
  calculateTotalProducts,
  calculateRevenueGrowth
} from "../data/dashboard-data";

export function Dashboard() {
  // Calculate metrics
  const totalRevenue = calculateTotalRevenue();
  const totalOrders = calculateTotalOrders();
  const totalCustomers = calculateTotalCustomers();
  const averageOrderValue = calculateAverageOrderValue();
  const totalProducts = calculateTotalProducts();
  const revenueGrowth = calculateRevenueGrowth();

  // Color palettes for different charts
  const colors = {
    revenue: ["#3b82f6"],  // Blue
    products: ["#8b5cf6", "#6366f1", "#4f46e5", "#7c3aed", "#9333ea"],  // Purple spectrum
    categories: ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6", "#f97316"],  // Mixed
    regions: ["#059669", "#10b981", "#34d399", "#6ee7b7"],  // Green spectrum
    territories: ["#0ea5e9", "#06b6d4", "#14b8a6", "#10b981", "#22c55e"]  // Blue to Green
  };

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-4 w-full p-4">
      {/* Key Metrics */}
      <div className="col-span-1 md:col-span-2 lg:col-span-4">
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm">
            <p className="text-xs text-gray-500">Total Revenue</p>
            <p className="text-xl font-semibold text-gray-900">${totalRevenue.toLocaleString()}</p>
          </div>
          <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm">
            <p className="text-xs text-gray-500">Total Orders</p>
            <p className="text-xl font-semibold text-gray-900">{totalOrders.toLocaleString()}</p>
          </div>
          <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm">
            <p className="text-xs text-gray-500">Customers</p>
            <p className="text-xl font-semibold text-gray-900">{totalCustomers.toLocaleString()}</p>
          </div>
          <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm">
            <p className="text-xs text-gray-500">Avg Order Value</p>
            <p className="text-xl font-semibold text-gray-900">${averageOrderValue}</p>
          </div>
          <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm">
            <p className="text-xs text-gray-500">Total Products</p>
            <p className="text-xl font-semibold text-gray-900">{totalProducts}</p>
          </div>
          <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm">
            <p className="text-xs text-gray-500">YoY Growth</p>
            <p className="text-xl font-semibold text-gray-900">{revenueGrowth}</p>
          </div>
        </div>
      </div>

      {/* Charts */}
      <Card className="col-span-1 md:col-span-2 lg:col-span-4">
        <CardHeader className="pb-1 pt-3">
          <CardTitle className="text-base font-medium">Monthly Revenue by Region</CardTitle>
          <CardDescription className="text-xs">Revenue trends from July 1996 to May 1998</CardDescription>
        </CardHeader>
        <CardContent className="p-3">
          <div className="h-60">
            <AreaChart
              data={monthlyRevenueData}
              index="date"
              categories={["Eastern", "Western", "Northern", "Southern"]}
              colors={["#059669", "#0ea5e9", "#8b5cf6", "#f59e0b"]}
              valueFormatter={(value) => `$${value.toLocaleString()}`}
              showLegend={true}
              showGrid={true}
              showXAxis={true}
              showYAxis={true}
              stacked={true}
            />
          </div>
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-1 lg:col-span-2">
        <CardHeader className="pb-1 pt-3">
          <CardTitle className="text-base font-medium">Top Products</CardTitle>
          <CardDescription className="text-xs">Top 10 products by revenue</CardDescription>
        </CardHeader>
        <CardContent className="p-3">
          <div className="h-60">
            <BarChart
              data={productPerformanceData}
              index="name"
              categories={["sales"]}
              colors={colors.products}
              valueFormatter={(value) => `$${value.toLocaleString()}`}
              showLegend={false}
              showGrid={true}
              layout="horizontal"
            />
          </div>
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-1 lg:col-span-2">
        <CardHeader className="pb-1 pt-3">
          <CardTitle className="text-base font-medium">Sales by Category</CardTitle>
          <CardDescription className="text-xs">Revenue distribution across product categories</CardDescription>
        </CardHeader>
        <CardContent className="p-3">
          <div className="h-60">
            <DonutChart
              data={categoryDistributionData}
              category="value"
              index="name"
              valueFormatter={(value) => `${value}%`}
              colors={colors.categories}
              centerText="Categories"
              paddingAngle={0}
              showLabel={false}
              showLegend={true}
              innerRadius={45}
              outerRadius="90%"
            />
          </div>
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-1 lg:col-span-2">
        <CardHeader className="pb-1 pt-3">
          <CardTitle className="text-base font-medium">Revenue by Region</CardTitle>
          <CardDescription className="text-xs">Sales performance across geographic regions</CardDescription>
        </CardHeader>
        <CardContent className="p-3">
          <div className="h-60">
            <BarChart
              data={regionalRevenueData}
              index="region"
              categories={["sales"]}
              colors={colors.regions}
              valueFormatter={(value) => `$${value.toLocaleString()}`}
              showLegend={false}
              showGrid={true}
              layout="horizontal"
            />
          </div>
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-1 lg:col-span-2">
        <CardHeader className="pb-1 pt-3">
          <CardTitle className="text-base font-medium">Top Territories</CardTitle>
          <CardDescription className="text-xs">Top 10 sales territories by revenue</CardDescription>
        </CardHeader>
        <CardContent className="p-3">
          <div className="h-60">
            <BarChart
              data={topTerritoriesData}
              index="territory"
              categories={["sales"]}
              colors={colors.territories}
              valueFormatter={(value) => `$${value.toLocaleString()}`}
              showLegend={false}
              showGrid={true}
              layout="horizontal"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}