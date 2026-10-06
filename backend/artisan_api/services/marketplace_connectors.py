import os
import uuid
import logging
from abc import ABC, abstractmethod
from artisan_api.models import MarketplaceSyncLog, Product

logger = logging.getLogger(__name__)

MARKETPLACE_MODE = os.getenv('MARKETPLACE_MODE', 'mock')

class MarketplaceConnector(ABC):
    @abstractmethod
    def publish_product(self, product: Product) -> dict:
        pass

    @abstractmethod
    def update_inventory(self, product: Product, quantity: int) -> dict:
        pass

    @abstractmethod
    def fetch_orders(self) -> list:
        pass


class ONDCAdapter(MarketplaceConnector):
    def publish_product(self, product: Product) -> dict:
        if MARKETPLACE_MODE == 'mock':
            ref = f"ONDC-IND-{uuid.uuid4().hex[:8].upper()}"
            MarketplaceSyncLog.objects.create(platform='ONDC', product=product, action='publish', status='success')
            return {'status': 'success', 'network_ref': ref, 'mode': 'mock', 'message': 'Listed on ONDC Open Network'}
        return {'status': 'success', 'network_ref': 'ONDC-LIVE-123'}

    def update_inventory(self, product: Product, quantity: int) -> dict:
        MarketplaceSyncLog.objects.create(platform='ONDC', product=product, action='update_inventory', status='success')
        return {'status': 'success', 'quantity': quantity}

    def fetch_orders(self) -> list:
        return []


class AmazonKarigarAdapter(MarketplaceConnector):
    def publish_product(self, product: Product) -> dict:
        ref = f"AMZN-KARIGAR-{uuid.uuid4().hex[:8].upper()}"
        MarketplaceSyncLog.objects.create(platform='Amazon Karigar', product=product, action='publish', status='success')
        return {'status': 'success', 'network_ref': ref, 'mode': 'mock', 'message': 'Exported to Amazon Karigar Store'}

    def update_inventory(self, product: Product, quantity: int) -> dict:
        MarketplaceSyncLog.objects.create(platform='Amazon Karigar', product=product, action='update_inventory', status='success')
        return {'status': 'success', 'quantity': quantity}

    def fetch_orders(self) -> list:
        return []


class EtsyAdapter(MarketplaceConnector):
    def publish_product(self, product: Product) -> dict:
        ref = f"ETSY-GLOBAL-{uuid.uuid4().hex[:8].upper()}"
        MarketplaceSyncLog.objects.create(platform='Etsy', product=product, action='publish', status='success')
        return {'status': 'success', 'network_ref': ref, 'mode': 'mock', 'message': 'Listed on Etsy Global Handicrafts'}

    def update_inventory(self, product: Product, quantity: int) -> dict:
        MarketplaceSyncLog.objects.create(platform='Etsy', product=product, action='update_inventory', status='success')
        return {'status': 'success', 'quantity': quantity}

    def fetch_orders(self) -> list:
        return []


class CraftsvillaAdapter(MarketplaceConnector):
    def publish_product(self, product: Product) -> dict:
        ref = f"CRAFTS-IN-{uuid.uuid4().hex[:8].upper()}"
        MarketplaceSyncLog.objects.create(platform='Craftsvilla', product=product, action='publish', status='success')
        return {'status': 'success', 'network_ref': ref, 'mode': 'mock', 'message': 'Published to Craftsvilla Marketplace'}

    def update_inventory(self, product: Product, quantity: int) -> dict:
        return {'status': 'success', 'quantity': quantity}

    def fetch_orders(self) -> list:
        return []


class MarketplaceService:
    def __init__(self):
        self.adapters = {
            'ONDC': ONDCAdapter(),
            'Amazon Karigar': AmazonKarigarAdapter(),
            'Etsy': EtsyAdapter(),
            'Craftsvilla': CraftsvillaAdapter()
        }

    def sync_to_all(self, product: Product) -> dict:
        results = {}
        for name, adapter in self.adapters.items():
            results[name] = adapter.publish_product(product)
        return results
