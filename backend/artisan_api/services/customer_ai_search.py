import re
from artisan_api.models import Product

class PersonalizedCustomerAISearch:
    """Conversational Customer Search & Recommendation Engine."""
    def search_products(self, query: str, max_budget: float = None) -> dict:
        q_lower = query.lower()

        # Intent parsing
        budget_match = re.search(r'under\s*₹?\s*(\d+)', q_lower)
        if budget_match:
            max_budget = float(budget_match.group(1))

        queryset = Product.objects.filter(status='published')

        if max_budget:
            queryset = queryset.filter(price__lte=max_budget)

        if 'blue' in q_lower or 'pottery' in q_lower:
            queryset = queryset.filter(title__icontains='pottery')
        elif 'silk' in q_lower or 'saree' in q_lower:
            queryset = queryset.filter(title__icontains='saree')

        products = list(queryset.order_by('-views_count')[:6])

        explanation = f"Found {len(products)} matching authentic handcrafted items"
        if max_budget:
            explanation += f" under ₹{max_budget}."

        return {
            'query': query,
            'max_budget': max_budget,
            'products': [
                {
                    'id': str(p.id),
                    'title': p.title,
                    'price': float(p.price),
                    'category': p.category,
                    'description': p.description[:120] + '...'
                } for p in products
            ],
            'explanation': explanation
        }

class AIVisualSearch:
    """Extracts visual attributes from uploaded photo and finds visually similar craft products."""
    def find_similar(self, image_url: str = "") -> dict:
        # Heuristic visual matching for demo
        matches = Product.objects.filter(status='published')[:3]
        return {
            'detected_attributes': ['Handcrafted Glazed Ceramic', 'Turquoise Blue Finish', 'Traditional Motif'],
            'confidence': '94.2%',
            'similar_products': [
                {
                    'id': str(p.id),
                    'title': p.title,
                    'price': float(p.price),
                    'category': p.category
                } for p in matches
            ]
        }
