"""
Financial Coaching Intelligence Module
Transforms raw financial data into coaching insights, recommendations, and engagement.
"""

import logging
from typing import Dict, List, Any, Optional
from statistics import mean

logger = logging.getLogger(__name__)


class CoachingAnalyzer:
    """Analyzes financial data and generates coaching insights"""
    
    def __init__(self):
        self.logger = logger
    
    def analyze(self, rows: List[Dict], query: str, analysis_context: Optional[Dict] = None) -> Dict:
        if not rows or not isinstance(rows, list):
            return self._empty_coaching()
        
        query_lower = query.lower()
        
        # Determine query type
        if any(word in query_lower for word in ['merchant', 'where', 'most at', 'spent the most']):
            return self.analyze_spending_by_merchant(rows)
        
        elif any(word in query_lower for word in ['category', 'categories', 'spending by']):
            return self.analyze_spending_by_category(rows)
        
        elif any(word in query_lower for word in ['trend', 'over time', 'month', 'week']):
            return self.analyze_trends(rows)
        
        else:
            return self.generate_general_insights(rows)


    def analyze_spending_by_category(self, rows: List[Dict]) -> Dict:
        """
        Analyze spending by category and provide coaching
        Returns Red/Yellow/Green zones with recommendations
        """
        if not rows or not isinstance(rows, list):
            return self._empty_coaching()
        
        # Extract category data
        categories = []
        total_spending = 0
        
        for row in rows:
            if not isinstance(row, dict):
                continue
            
            # Get category name and amount
            category_name = row.get('category_name', '')
            amount = row.get('total_spending', 0)
            
            if not category_name or not isinstance(amount, (int, float)):
                continue
            
            categories.append({
                'name': category_name,
                'amount': float(amount)
            })
            total_spending += float(amount)
        
        if not categories or total_spending == 0:
            return self._empty_coaching()
        
        # Calculate percentages
        categories_with_pct = []
        for cat in categories:
            pct = (cat['amount'] / total_spending * 100) if total_spending > 0 else 0
            categories_with_pct.append({
                'name': cat['name'],
                'amount': cat['amount'],
                'percentage': pct
            })
        
        # Sort by amount descending
        categories_with_pct.sort(key=lambda x: x['amount'], reverse=True)
        
        # Identify zones: Red (>10%), Yellow (3-10%), Green (<3%)
        red_zones = [c for c in categories_with_pct if c['percentage'] > 10]
        yellow_zones = [c for c in categories_with_pct if 3 <= c['percentage'] <= 10]
        green_zones = [c for c in categories_with_pct if c['percentage'] < 3]
        
        # Filter out transfers for "real spending"
        transfers = ['paycheck', 'credit card', 'payment', 'transfer', 'deposit']
        real_categories = [c for c in categories_with_pct
                        if not any(t in c['name'].lower() for t in transfers)]
        real_spending = sum(c['amount'] for c in real_categories)
        
        # Generate opportunities
        opportunities = []
        
        for cat in red_zones:
            cat_lower = cat['name'].lower()
            
            if 'mortgage' in cat_lower or 'rent' in cat_lower:
                savings = cat['amount'] * 0.05  # 5% with refinancing
                opportunities.append({
                    'category': cat['name'],
                    'amount': cat['amount'],
                    'percentage': cat['percentage'],
                    'opportunity': 'Refinancing or renegotiating lease',
                    'potential_savings': savings,
                    'action': f"Could save ${savings:,.0f}/month with refinancing"
                })
            elif 'home improvement' in cat_lower or 'renovation' in cat_lower:
                savings = cat['amount'] * 0.50  # 50% if deferred
                opportunities.append({
                    'category': cat['name'],
                    'amount': cat['amount'],
                    'percentage': cat['percentage'],
                    'opportunity': 'Defer non-essential projects',
                    'potential_savings': savings,
                    'action': f"Deferring 50% could save ${savings:,.0f}/month"
                })
        
        for cat in yellow_zones:
            cat_lower = cat['name'].lower()
            
            if any(word in cat_lower for word in ['restaurant', 'dining', 'food & dining', 'fast food']):
                savings = cat['amount'] * 0.30  # 30% with meal prep
                opportunities.append({
                    'category': cat['name'],
                    'amount': cat['amount'],
                    'percentage': cat['percentage'],
                    'opportunity': 'Meal prep and home cooking',
                    'potential_savings': savings,
                    'action': f"Meal prep 2x/week could save ${savings:,.0f}/month"
                })
            elif any(word in cat_lower for word in ['gas', 'fuel', 'auto']):
                savings = cat['amount'] * 0.20  # 20% with optimization
                opportunities.append({
                    'category': cat['name'],
                    'amount': cat['amount'],
                    'percentage': cat['percentage'],
                    'opportunity': 'Carpooling, EV, or route optimization',
                    'potential_savings': savings,
                    'action': f"Optimization could save ${savings:,.0f}/month"
                })
            elif 'shopping' in cat_lower:
                savings = cat['amount'] * 0.15
                opportunities.append({
                    'category': cat['name'],
                    'amount': cat['amount'],
                    'percentage': cat['percentage'],
                    'opportunity': 'Budget discipline or list-based shopping',
                    'potential_savings': savings,
                    'action': f"Impulse control could save ${savings:,.0f}/month"
                })
        
        # Sort opportunities by potential savings
        opportunities.sort(key=lambda x: x['potential_savings'], reverse=True)
        
        # Generate insights
        insights = []
        
        if real_categories:
            insights.append(f"💰 Real Monthly Spending: ${real_spending:,.0f} (excluding transfers)")
        
        if red_zones:
            top_red = red_zones[0]
            insights.append(f"🔴 Highest Expense: {top_red['name']} @ ${top_red['amount']:,.0f} ({top_red['percentage']:.1f}% of total)")

        if opportunities:
            total_opportunity = sum(o['potential_savings'] for o in opportunities)
            insights.append(f"💡 Found {len(opportunities)} optimization opportunities totaling ${total_opportunity:,.0f}/month savings")

        if yellow_zones:
            top_yellow = yellow_zones[0]
            insights.append(f"🟡 Monitor: {top_yellow['name']} at {top_yellow['percentage']:.1f}% - watch for growth")
        
        # Generate recommendations
        recommendations = []

        if red_zones:
            top_red = red_zones[0]
            recommendations.append(f"Your {top_red['name']} is your largest expense ({top_red['percentage']:.1f}%). This should be priority #1 for optimization.")

        if opportunities:
            top_opp = opportunities[0]
            recommendations.append(f"{top_opp['action']} (Highest impact: ${top_opp['potential_savings']:,.0f}/month)")

        if len(opportunities) > 1:
            second_opp = opportunities[1]
            recommendations.append(f"{second_opp['action']}")
        
        # Generate follow-up questions
        follow_ups = []

        if red_zones:
            top_red = red_zones[0]
            follow_ups.append(f"Is your {top_red['name']} spending one-time or recurring?")

        if opportunities:
            follow_ups.append(f"Which of these {len(opportunities)} opportunities interests you most?")

        follow_ups.append("Should we create a monthly savings goal based on these opportunities?")
        
        return {
            'type': 'spending_by_category',
            'total_spending': total_spending,
            'real_spending': real_spending,
            'red_zones': red_zones,
            'yellow_zones': yellow_zones,
            'green_zones': green_zones,
            'opportunities': opportunities,
            'insights': insights,
            'recommendations': recommendations,
            'follow_up_questions': follow_ups,
            'total_opportunity': sum(o['potential_savings'] for o in opportunities) if opportunities else 0
        }

    
    def analyze_spending_by_merchant(self, rows: List[Dict]) -> Dict:
        """
        Analyze spending by merchant and provide coaching
        """
        
        # Extract merchant data
        merchants = []
        total_spending = 0
        
        for row in rows:
            if not isinstance(row, dict):
                continue
            
            if 'merchant_name' not in row:
                continue
            
            amount = row.get('total_spent', 0)
            if isinstance(amount, (int, float)):
                merchants.append({
                    'name': row['merchant_name'],
                    'amount': amount
                })
                total_spending += amount
        
        if not merchants or total_spending == 0:
            return self._empty_coaching()
        
        # Filter out transfers
        transfers = ['paycheck', 'credit card', 'mortgage payment', 'payment']
        real_merchants = [m for m in merchants 
                         if not any(t in m['name'].lower() for t in transfers)]
        real_spending = sum(m['amount'] for m in real_merchants)
        
        # Categorize merchants
        restaurants = [m for m in real_merchants if any(
            x in m['name'].lower() for x in ['restaurant', 'dining', 'bar', 'cafe', 'coffee', 'pizza', 'burger', 'tacos', 'sushi']
        )]
        
        fuel = [m for m in real_merchants if any(
            x in m['name'].lower() for x in ['gas', 'shell', 'bp', 'exxon', 'chevron', 'valero', 'conoco', 'quiktrip']
        )]
        
        groceries = [m for m in real_merchants if any(
            x in m['name'].lower() for x in ['grocery', 'trader', 'whole foods', 'safeway', 'walmart', 'kroger', 'instacart']
        )]
        
        entertainment = [m for m in real_merchants if any(
            x in m['name'].lower() for x in ['netflix', 'spotify', 'movie', 'theater', 'hulu', 'disney']
        )]
        
        # Generate insights
        insights = []
        
        restaurant_total = sum(m['amount'] for m in restaurants)
        grocery_total = sum(m['amount'] for m in groceries)
        
        insights.append(f"💰 Real Spending (excluding transfers): ${real_spending:,.0f}")
        
        if restaurants:
            insights.append(f"🍽️  Dining Out: ${restaurant_total:,.0f} at {len(restaurants)} different places")
            if grocery_total > 0:
                ratio = restaurant_total / grocery_total
                insights.append(f"   Ratio to groceries: {ratio:.1f}:1 (eating out {ratio:.1f}x more than buying groceries)")
        
        if fuel:
            fuel_total = sum(m['amount'] for m in fuel)
            insights.append(f"⛽ Fuel: ${fuel_total:,.0f} across {len(fuel)} stations")
        
        if groceries:
            insights.append(f"🛒 Groceries: ${grocery_total:,.0f} (good control)")
        
        if entertainment:
            ent_total = sum(m['amount'] for m in entertainment)
            insights.append(f"🎬 Entertainment: ${ent_total:,.0f}/month (subscriptions)")
        
        # Generate opportunities
        opportunities = []
        
        if restaurants and grocery_total > 0:
            savings = restaurant_total * 0.30  # 30% savings with meal prep
            opportunities.append({
                'category': 'Dining Out',
                'amount': restaurant_total,
                'opportunity': 'Meal prep and home cooking',
                'potential_savings': savings,
                'action': f"Reduce dining out by 30%: save ${savings:,.0f}/month"
            })
        
        if fuel:
            fuel_total = sum(m['amount'] for m in fuel)
            savings = fuel_total * 0.20
            opportunities.append({
                'category': 'Fuel',
                'amount': fuel_total,
                'opportunity': 'Consolidate gas stations or optimize routes',
                'potential_savings': savings,
                'action': f"Route optimization: save ${savings:,.0f}/month"
            })
        
        if entertainment:
            ent_total = sum(m['amount'] for m in entertainment)
            savings = ent_total * 0.30  # Cancel unused subscriptions
            opportunities.append({
                'category': 'Entertainment',
                'amount': ent_total,
                'opportunity': 'Cancel unused subscriptions',
                'potential_savings': savings,
                'action': f"Review subscriptions: save ${savings:,.0f}/month"
            })
        
        # Generate recommendations
        recommendations = []

        if restaurants:
            top_restaurant = max(restaurants, key=lambda x: x['amount'])
            recommendations.append(f"Your top restaurant is {top_restaurant['name']} (${top_restaurant['amount']:,.0f}). Consider cooking that cuisine at home.")

        if opportunities:
            recommendations.append(opportunities[0]['action'])
        
        # Generate follow-ups
        follow_ups = []
        if restaurants:
            follow_ups.append("Want to identify your favorite restaurants and optimize around them?")
        
        follow_ups.append("Should we track your dining spending weekly?")
        follow_ups.append("What's a realistic monthly dining budget for you?")
        
        return {
            'type': 'spending_by_merchant',
            'total_spending': total_spending,
            'real_spending': real_spending,
            'restaurants': restaurants,
            'fuel': fuel,
            'groceries': groceries,
            'entertainment': entertainment,
            'opportunities': opportunities,
            'insights': insights,
            'recommendations': recommendations,
            'follow_up_questions': follow_ups,
            'total_opportunity': sum(o['potential_savings'] for o in opportunities) if opportunities else 0
        }
    
    def analyze_trends(self, rows: List[Dict]) -> Dict:
        """Analyze spending trends over time"""
        
        insights = [
            "📊 Trend analysis available with date-based queries",
            "Try: 'Show my spending trend over last 3 months' or 'How much did I spend last month?'"
        ]
        
        return {
            'type': 'trends',
            'insights': insights,
            'recommendations': ["Provide date range for trend analysis"],
            'follow_up_questions': ["Which time period would you like to analyze?"]
        }
    
    def generate_general_insights(self, rows: List[Dict]) -> Dict:
        """Generate general insights when query type is unclear"""
        
        return self._empty_coaching()
    
    def _empty_coaching(self) -> Dict:
        """Return empty coaching structure"""
        return {
            'type': 'general',
            'insights': [],
            'recommendations': [],
            'follow_up_questions': [],
            'opportunities': []
        }


# Global instance
coaching_analyzer = CoachingAnalyzer()
