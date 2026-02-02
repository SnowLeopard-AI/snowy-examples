// Monthly revenue data from Northwind database by region (July 1996 - May 1998)
export const monthlyRevenueData = [
  { date: "Jul 96", Eastern: 58514.85, Western: 12795.13, Northern: 37290.9, Southern: 11852.88 },
  { date: "Aug 96", Eastern: 33949.73, Western: 17494.6, Northern: 33055.2, Southern: 13808.32 },
  { date: "Sep 96", Eastern: 54622.9, Western: 31984.0, Northern: 19329.2, Southern: 7048.0 },
  { date: "Oct 96", Eastern: 94923.67, Western: 39770.8, Northern: 39090.3, Southern: 14319.52 },
  { date: "Nov 96", Eastern: 112669.17, Western: 106833.1, Northern: 2819.2, Southern: 14831.92 },
  { date: "Dec 96", Eastern: 147670.92, Western: 26657.0, Northern: 26637.28, Southern: 11035.2 },
  { date: "Jan 97", Eastern: 107291.76, Western: 119073.4, Northern: 33107.48, Southern: 27924.06 },
  { date: "Feb 97", Eastern: 51346.78, Western: 45531.2, Northern: 29613.44, Southern: 40850.56 },
  { date: "Mar 97", Eastern: 63495.49, Western: 44296.0, Northern: 29320.2, Southern: 46397.6 },
  { date: "Apr 97", Eastern: 132738.52, Western: 97837.12, Northern: 7155.6, Southern: 41010.2 },
  { date: "May 97", Eastern: 101092.91, Western: 59108.1, Northern: 18588.2, Southern: 72198.4 },
  { date: "Jun 97", Eastern: 92622.43, Western: 38144.05, Northern: 33429.15, Southern: 22399.14 },
  { date: "Jul 97", Eastern: 156737.36, Western: 62144.8, Northern: 14358.12, Southern: 4327.87 },
  { date: "Aug 97", Eastern: 85167.54, Western: 84948.11, Northern: 28096.9, Southern: 23326.4 },
  { date: "Sep 97", Eastern: 117857.32, Western: 135519.67, Northern: 72468.25, Southern: 14223.6 },
  { date: "Oct 97", Eastern: 180370.7, Western: 37347.0, Northern: 47913.01, Southern: 30507.82 },
  { date: "Nov 97", Eastern: 56411.39, Western: 50517.25, Northern: 65181.54, Southern: 38392.34 },
  { date: "Dec 97", Eastern: 135717.57, Western: 45877.08, Northern: 29071.32, Southern: 70546.64 },
  { date: "Jan 98", Eastern: 186346.0, Western: 75474.15, Northern: 82528.08, Southern: 102820.03 },
  { date: "Feb 98", Eastern: 253756.46, Western: 72938.32, Northern: 134847.38, Southern: 86160.96 },
  { date: "Mar 98", Eastern: 188927.98, Western: 87208.37, Northern: 132227.52, Southern: 65440.5 },
  { date: "Apr 98", Eastern: 273389.54, Western: 312140.37, Northern: 121618.9, Southern: 51829.42 },
  { date: "May 98", Eastern: 44577.02, Western: 11608.35, Northern: 10858.4, Southern: 0 },
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
