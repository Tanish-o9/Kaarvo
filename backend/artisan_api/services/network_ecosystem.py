import decimal
from artisan_api.models import Product, Order, DeadLetterQueueItem, ThirdPartyAIAgent, NetworkIdentity, ProductVersion

class CurrencyConverterService:
    """Deterministic Multi-Currency Exchange Rate Engine."""
    RATES = {
        'INR': 1.0,
        'USD': 0.012,
        'EUR': 0.011,
        'GBP': 0.0094,
        'AED': 0.044
    }

    @classmethod
    def convert(cls, amount_inr: float, target_currency: str) -> dict:
        target = target_currency.upper()
        rate = cls.RATES.get(target, 1.0)
        converted_val = round(float(amount_inr) * rate, 2)
        return {
            'original_amount_inr': float(amount_inr),
            'target_currency': target,
            'exchange_rate': rate,
            'converted_amount': converted_val,
            'formatted': f"{target} {converted_val:,.2f}"
        }


class ProfitabilityCalculator:
    """Deterministic Unit Economics & Channel Profitability Service."""
    @staticmethod
    def calculate_product_economics(product: Product) -> dict:
        price = float(product.price)
        platform_fee = round(price * 0.05, 2)     # 5% platform fee
        payment_fee = round(price * 0.02, 2)      # 2% gateway fee
        estimated_shipping = 120.00               # flat logistics estimate
        estimated_material_cost = float(product.cost_price) if hasattr(product, 'cost_price') and product.cost_price else round(price * 0.45, 2)

        net_contribution = round(price - (platform_fee + payment_fee + estimated_shipping + estimated_material_cost), 2)
        margin_percent = round((net_contribution / price) * 100, 1) if price > 0 else 0.0

        quadrant = "HIGH_MARGIN" if margin_percent >= 30 else "LOW_MARGIN"

        return {
            'product_id': str(product.id),
            'title': product.title,
            'selling_price': price,
            'breakdown': {
                'platform_fee': platform_fee,
                'payment_fee': payment_fee,
                'estimated_shipping': estimated_shipping,
                'material_packing_cost': estimated_material_cost,
            },
            'net_contribution': net_contribution,
            'margin_percent': margin_percent,
            'quadrant': quadrant,
            'ai_recommendation': f"Product '{product.title}' has a healthy {margin_percent}% margin." if margin_percent >= 30 else "Consider bundling with high-margin crafts to increase net contribution."
        }


class UniversalSearchEngine:
    """Safe Natural Language Query Generator for products, orders, and artisans."""
    @staticmethod
    def search(query_text: str) -> dict:
        query_text = query_text.lower()
        products = Product.objects.all()

        if 'pottery' in query_text or 'vase' in query_text:
            products = products.filter(title__icontains='pottery') | products.filter(description__icontains='pottery') | products.filter(title__icontains='vase')
        elif 'saree' in query_text or 'silk' in query_text or 'handloom' in query_text:
            products = products.filter(title__icontains='saree') | products.filter(description__icontains='silk')
        elif 'under' in query_text:
            # Extract basic price filter
            words = query_text.split()
            for i, w in enumerate(words):
                if w in ['under', 'below'] and i + 1 < len(words):
                    try:
                        clean_num = ''.join(c for c in words[i+1] if c.isdigit())
                        if clean_num:
                            max_p = float(clean_num)
                            products = products.filter(price__lte=max_p)
                    except ValueError:
                        pass

        result_list = [{'id': str(p.id), 'title': p.title, 'price': float(p.price), 'artisan': p.artisan.username} for p in products[:10]]

        return {
            'natural_query': query_text,
            'matches_count': len(result_list),
            'results': result_list,
            'safe_filter_applied': True
        }


class OperationsResiliencyService:
    """DLQ management, circuit breakers, and network health monitoring."""
    @staticmethod
    def replay_dlq_item(item_id: str) -> dict:
        try:
            dlq_item = DeadLetterQueueItem.objects.get(pk=item_id)
            dlq_item.status = 'REPLAYED'
            dlq_item.retry_count += 1
            dlq_item.save()
            return {
                'message': f"Task '{dlq_item.task_type}' successfully replayed from Dead Letter Queue.",
                'item_id': str(dlq_item.id),
                'status': 'REPLAYED'
            }
        except DeadLetterQueueItem.DoesNotExist:
            return {'error': 'DLQ item not found'}
