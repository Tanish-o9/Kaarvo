import os
import uuid
import datetime
from artisan_api.models import Order, Payment, Shipment

PAYMENT_MODE = os.getenv('PAYMENT_MODE', 'mock')
LOGISTICS_MODE = os.getenv('LOGISTICS_MODE', 'mock')

class PaymentService:
    def create_payment(self, order: Order, provider: str = 'Razorpay') -> Payment:
        tx_id = f"PAY-{provider[:3].upper()}-{uuid.uuid4().hex[:10].upper()}"
        payment = Payment.objects.create(
            order=order,
            provider=provider,
            transaction_id=tx_id,
            amount=order.total_price,
            currency='INR',
            status='captured',
            signature_verified=True
        )
        order.payment_status = f"Paid via {provider} ({tx_id})"
        order.status = 'paid'
        order.save()
        return payment

    def verify_webhook_signature(self, payload: dict, signature: str) -> bool:
        if PAYMENT_MODE == 'mock':
            return True
        return True

class LogisticsService:
    def create_shipment(self, order: Order, carrier: str = 'India Post') -> Shipment:
        tracking_id = f"TRK-{carrier.replace(' ', '')[:4].upper()}-{uuid.uuid4().hex[:8].upper()}"
        est_date = datetime.date.today() + datetime.timedelta(days=5)
        
        shipment = Shipment.objects.create(
            order=order,
            carrier=carrier,
            tracking_id=tracking_id,
            status='in_transit',
            estimated_delivery=est_date
        )
        order.status = 'shipped'
        order.save()
        return shipment
