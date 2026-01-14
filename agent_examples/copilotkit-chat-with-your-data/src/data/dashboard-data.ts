// Monthly revenue data from Northwind database (July 1996 - May 1998)
export const monthlyRevenueData = [
  { date: "Jul 96", revenue: 27861.9 },
  { date: "Aug 96", revenue: 25485.28 },
  { date: "Sep 96", revenue: 26381.4 },
  { date: "Oct 96", revenue: 37515.72 },
  { date: "Nov 96", revenue: 45600.05 },
  { date: "Dec 96", revenue: 45239.63 },
  { date: "Jan 97", revenue: 61258.07 },
  { date: "Feb 97", revenue: 38483.63 },
  { date: "Mar 97", revenue: 38547.22 },
  { date: "Apr 97", revenue: 53032.95 },
  { date: "May 97", revenue: 53781.29 },
  { date: "Jun 97", revenue: 36362.8 },
  { date: "Jul 97", revenue: 51020.86 },
  { date: "Aug 97", revenue: 47287.67 },
  { date: "Sep 97", revenue: 55629.24 },
  { date: "Oct 97", revenue: 66749.23 },
  { date: "Nov 97", revenue: 43533.81 },
  { date: "Dec 97", revenue: 71398.43 },
  { date: "Jan 98", revenue: 94222.11 },
  { date: "Feb 98", revenue: 99415.29 },
  { date: "Mar 98", revenue: 104854.15 },
  { date: "Apr 98", revenue: 123798.68 },
  { date: "May 98", revenue: 18333.63 },
];

// Top selling products by revenue
export const productPerformanceData = [
  { name: "Côte de Blaye", sales: 141396.74, units: 623 },
  { name: "Thüringer Rostbratwurst", sales: 80368.67, units: 746 },
  { name: "Raclette Courdavault", sales: 71155.7, units: 1496 },
  { name: "Tarte au sucre", sales: 47234.97, units: 1083 },
  { name: "Camembert Pierrot", sales: 46825.48, units: 1577 },
  { name: "Gnocchi di nonna Alice", sales: 42593.06, units: 1263 },
  { name: "Manjimup Dried Apples", sales: 41819.65, units: 886 },
  { name: "Alice Mutton", sales: 32698.38, units: 978 },
  { name: "Carnarvon Tigers", sales: 29171.87, units: 539 },
  { name: "Rössle Sauerkraut", sales: 25696.64, units: 640 },
];

// Revenue by category
export const categoryRevenueData = [
  { name: "Beverages", value: 267868.18 },
  { name: "Dairy Products", value: 234507.28 },
  { name: "Confections", value: 167357.23 },
  { name: "Meat/Poultry", value: 163022.36 },
  { name: "Seafood", value: 131261.74 },
  { name: "Condiments", value: 106047.08 },
  { name: "Produce", value: 99984.58 },
  { name: "Grains/Cereals", value: 95744.59 },
];

// Calculate total category revenue for percentages
const totalCategoryRevenue = categoryRevenueData.reduce((sum, cat) => sum + cat.value, 0);

// Category distribution as percentages (for donut chart)
export const categoryDistributionData = categoryRevenueData.map(cat => ({
  name: cat.name,
  value: Number(((cat.value / totalCategoryRevenue) * 100).toFixed(1)),
  revenue: cat.value
}));

// Revenue by region
export const regionalRevenueData = [
  { region: "Eastern", sales: 722066.00 },
  { region: "Western", sales: 538416.00 },
  { region: "Northern", sales: 349535.19 },
  { region: "Southern", sales: 270417.12 },
];

// Top territories by revenue
export const topTerritoriesData = [
  { territory: "Rockville", sales: 232890.85 },
  { territory: "Greensboro", sales: 232890.85 },
  { territory: "Cary", sales: 232890.85 },
  { territory: "Atlanta", sales: 202812.84 },
  { territory: "Savannah", sales: 202812.84 },
  { territory: "Orlando", sales: 202812.84 },
  { territory: "Tampa", sales: 202812.84 },
  { territory: "Wilton", sales: 192107.6 },
  { territory: "Neward", sales: 192107.6 },
  { territory: "Westboro", sales: 166537.76 },
];

// Metrics calculations
export const calculateTotalRevenue = () => {
  return 1265793.04; // Total from database
};

export const calculateTotalOrders = () => {
  return 830; // Total orders from database
};

export const calculateTotalCustomers = () => {
  return 91; // Total customers from database
};

export const calculateAverageOrderValue = () => {
  return 1525.05; // From database
};

export const calculateTotalProducts = () => {
  return 77; // Total products in catalog
};

export const calculateRevenueGrowth = () => {
  // Calculate year-over-year growth from Jan 97 to Jan 98
  const jan97 = 61258.07;
  const jan98 = 94222.11;
  const growth = ((jan98 - jan97) / jan97) * 100;
  return growth.toFixed(1) + "%";
};
