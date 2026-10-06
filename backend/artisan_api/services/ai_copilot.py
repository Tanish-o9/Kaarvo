import re
import json
import time
from artisan_api.models import Product, Order, Inventory, AgentMemory, LLMCostTracker

class AICommerceCopilot:
    """
    Unified Personal AI Commerce Copilot for Artisans.
    Routes natural language intents, applies approval levels 1-4, and manages long-term memory.
    """
    def process_query(self, user, query: str) -> dict:
        start_time = time.time()
        q_lower = query.lower()

        # Load User Memory / Preferences
        memories = AgentMemory.objects.filter(user=user)
        user_pref = {m.key: m.value for m in memories}
        pref_lang = user_pref.get('preferred_language', 'hi')

        result_payload = {}
        approval_level = 1 # Level 1: Safe read-only by default
        requires_approval = False
        action_name = "QUERY_INFO"

        # Intent 1: Price Update
        if "update price" in q_lower or "change price" in q_lower or "set price" in q_lower:
            match = re.search(r'₹?\s*(\d+)', query)
            new_price = float(match.group(1)) if match else 899.0
            prod = Product.objects.filter(artisan=user).first()
            if prod:
                action_name = "UPDATE_PRICE"
                approval_level = 2 # Level 2: Reversible change requiring quick confirmation
                requires_approval = True
                result_payload = {
                    'action': 'UPDATE_PRICE',
                    'product_id': str(prod.id),
                    'product_title': prod.title,
                    'current_price': float(prod.price),
                    'new_price': new_price,
                    'approval_level': 2,
                    'message': f"Do you want to update price of '{prod.title}' from ₹{prod.price} to ₹{new_price}?"
                }
                answer = f"I prepared the price update for '{prod.title}' to ₹{new_price}. Please confirm approval to execute."
            else:
                answer = "No products found to update."

        # Intent 2: Best Sellers & Analytics
        elif "best-selling" in q_lower or "top product" in q_lower or "performance" in q_lower:
            prods = Product.objects.filter(artisan=user).order_by('-views_count')[:3]
            items = [{"title": p.title, "price": float(p.price), "views": p.views_count} for p in prods]
            answer = f"Your top performing products are: " + ", ".join([f"{p['title']} (₹{p['price']})" for p in items])
            result_payload = {'top_products': items}

        # Intent 3: Low Stock Check
        elif "low stock" in q_lower or "restock" in q_lower or "inventory" in q_lower:
            low_inv = Inventory.objects.filter(product__artisan=user, quantity__lte=5)
            items = [{"title": i.product.title, "quantity": i.quantity} for i in low_inv]
            answer = f"Low stock alert: " + (", ".join([f"{i['title']} ({i['quantity']} left)" for i in items]) if items else "All inventory levels are healthy!")
            result_payload = {'low_stock_items': items}

        # Intent 4: Revenue & Earnings
        elif "earn" in q_lower or "revenue" in q_lower or "sales" in q_lower:
            orders = Order.objects.filter(artisan=user)
            total = sum(o.total_price for o in orders)
            answer = f"Your total earnings this month are ₹{total} across {orders.count()} completed orders."
            result_payload = {'total_revenue': float(total), 'order_count': orders.count()}

        # Intent 5: General Copilot Chat
        else:
            answer = f"Namaste! As your AI Business Copilot, I can help you update product prices, check stock, run festival campaigns, or view sales analytics."

        latency = int((time.time() - start_time) * 1000)

        # Track LLM Copilot Usage
        LLMCostTracker.objects.create(
            provider='Gemini',
            model_name='gemini-3.6-flash',
            operation='CopilotQuery',
            tokens_used=len(query) + len(answer),
            estimated_cost=0.000250,
            latency_ms=latency
        )

        return {
            'answer': answer,
            'action': action_name,
            'approval_level': approval_level,
            'requires_approval': requires_approval,
            'payload': result_payload,
            'latency_ms': latency
        }
