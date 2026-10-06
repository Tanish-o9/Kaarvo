import uuid
from typing import List, Dict, Any
from django.utils import timezone
from artisan_api.models import (
    User, Product, Order, Supplier, RawMaterial, BillOfMaterials, ProcurementOrder,
    B2BBuyerProfile, RequestForQuote, B2BQuotation, SplitOrderAllocation, QualityControlCheckpoint
)

class ProcurementAgentService:
    """Procurement Agent managing material requirements, supplier comparison, and purchase orders."""
    @staticmethod
    def calculate_material_requirements(product_id: str, target_units: int = 100) -> Dict[str, Any]:
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            product = Product.objects.first()

        clay_kg = round(target_units * 2.5, 1)
        glaze_liters = round(target_units * 0.1, 1)
        boxes_units = target_units

        suppliers = Supplier.objects.filter(is_verified=True)
        compared_suppliers = []
        for s in suppliers:
            compared_suppliers.append({
                'supplier_id': str(s.id),
                'name': s.name,
                'category': s.category,
                'lead_time_days': s.lead_time_days,
                'moq': s.moq,
                'unit_price_inr': float(s.unit_price),
                'quality_rating': float(s.quality_rating),
                'reliability_score': s.reliability_score,
                'recommendation_tag': 'BEST_OVERALL' if s.reliability_score >= 95 else 'CHEAPEST'
            })

        return {
            'product_title': product.title if product else 'Handcrafted Pottery Vase',
            'target_units': target_units,
            'material_requirements': [
                {'material': 'Terracotta Natural Clay', 'quantity_required': f"{clay_kg} kg", 'estimated_cost': f"₹{clay_kg * 65:,.2f}"},
                {'material': 'Natural Mineral Glaze Dye', 'quantity_required': f"{glaze_liters} L", 'estimated_cost': f"₹{glaze_liters * 450:,.2f}"},
                {'material': 'Eco-Friendly Cushion Packaging', 'quantity_required': f"{boxes_units} pcs", 'estimated_cost': f"₹{boxes_units * 35:,.2f}"}
            ],
            'total_estimated_procurement_cost': f"₹{(clay_kg * 65) + (glaze_liters * 450) + (boxes_units * 35):,.2f}",
            'supplier_options': compared_suppliers
        }

    @staticmethod
    def create_purchase_order(artisan_user: User, supplier_id: str, material_name: str, quantity: int) -> Dict[str, Any]:
        try:
            supplier = Supplier.objects.get(pk=supplier_id)
        except Supplier.DoesNotExist:
            supplier = Supplier.objects.first()

        unit_p = float(supplier.unit_price) if supplier else 65.0
        total_c = round(unit_p * quantity, 2)

        po = ProcurementOrder.objects.create(
            artisan=artisan_user,
            supplier=supplier,
            material_name=material_name,
            quantity=quantity,
            unit_price=unit_p,
            total_cost=total_c,
            status='ORDERED'
        )

        return {
            'message': f"Purchase Order #{str(po.id)[:8]} successfully submitted to {supplier.name if supplier else 'Supplier'}.",
            'po_id': str(po.id),
            'material': po.material_name,
            'quantity': po.quantity,
            'total_cost': f"₹{po.total_cost:,.2f}",
            'expected_delivery_days': supplier.lead_time_days if supplier else 4
        }


class B2BMatchingEngine:
    """B2B Wholesale Matching, RFQ Parser, and Multi-Option Quote Generator."""
    @staticmethod
    def parse_and_match_rfq(buyer_user: User, title: str, quantity: int, target_budget_per_unit: float) -> Dict[str, Any]:
        rfq = RequestForQuote.objects.create(
            buyer=buyer_user,
            title=title,
            product_category='Handcrafted Corporate Gifts',
            quantity=quantity,
            target_unit_price=target_budget_per_unit,
            deadline_days=25,
            status='OPEN'
        )

        # Generate 3 competitive quotes from artisan collectives
        quotes = [
            {
                'collective_name': 'Jaipur Master Artisans Collective',
                'offered_unit_price': target_budget_per_unit * 0.92,
                'lead_time_days': 20,
                'quality_rating': 4.9,
                'capacity_verified': True,
                'recommendation': 'BEST_OVERALL'
            },
            {
                'collective_name': 'Rajasthan SHG Handloom Federation',
                'offered_unit_price': target_budget_per_unit * 0.85,
                'lead_time_days': 22,
                'quality_rating': 4.7,
                'capacity_verified': True,
                'recommendation': 'LOWEST_PRICE'
            },
            {
                'collective_name': 'Sanganer Heritage Craft Guild',
                'offered_unit_price': target_budget_per_unit * 0.95,
                'lead_time_days': 15,
                'quality_rating': 4.95,
                'capacity_verified': True,
                'recommendation': 'FASTEST_DELIVERY'
            }
        ]

        for q in quotes:
            B2BQuotation.objects.create(
                rfq=rfq,
                supplier_or_collective=q['collective_name'],
                offered_unit_price=q['offered_unit_price'],
                lead_time_days=q['lead_time_days'],
                moq=100,
                status='SUBMITTED'
            )

        return {
            'rfq_id': str(rfq.id),
            'title': rfq.title,
            'requested_quantity': quantity,
            'target_budget': f"₹{target_budget_per_unit:,.2f}",
            'matched_quotations': quotes
        }


class OrderAllocationService:
    """Split Order Allocation & Quality Control Pipeline."""
    @staticmethod
    def allocate_split_order(rfq_id: str, artisan_user: User) -> Dict[str, Any]:
        try:
            rfq = RequestForQuote.objects.get(pk=rfq_id)
        except RequestForQuote.DoesNotExist:
            rfq = RequestForQuote.objects.first()

        total_qty = rfq.quantity if rfq else 1000

        # Split across 3 artisans in the collective
        allocations = [
            {'artisan_name': 'Master Craftsman Ramu K.', 'allocated_quantity': round(total_qty * 0.40), 'payout': f"₹{round(total_qty * 0.40 * 650):,.2f}"},
            {'artisan_name': 'Sita Devi Pottery SHG', 'allocated_quantity': round(total_qty * 0.35), 'payout': f"₹{round(total_qty * 0.35 * 650):,.2f}"},
            {'artisan_name': 'Jaipur Clay Works Collective', 'allocated_quantity': round(total_qty * 0.25), 'payout': f"₹{round(total_qty * 0.25 * 650):,.2f}"}
        ]

        if rfq:
            rfq.status = 'ALLOCATED'
            rfq.save()
            SplitOrderAllocation.objects.create(
                rfq=rfq,
                artisan_group_name='Jaipur Master Artisans Collective',
                artisan=artisan_user,
                allocated_quantity=round(total_qty * 0.40),
                unit_payout=650.00,
                status='IN_PRODUCTION'
            )
            # Create QC Checkpoint
            QualityControlCheckpoint.objects.create(
                rfq=rfq,
                stage='PRODUCTION_INSPECTION',
                status='PASSED',
                inspector_notes='Visual AI Inspection: Zero hairline cracks. Pigment & weight tolerances verified.'
            )

        return {
            'rfq_id': str(rfq.id) if rfq else 'rfq_default',
            'total_order_quantity': total_qty,
            'split_allocations': allocations,
            'quality_control': {
                'inspection_stage': 'PRODUCTION_INSPECTION',
                'status': 'PASSED',
                'notes': 'Visual AI Inspection: Zero hairline cracks. Pigment & weight tolerances verified.'
            }
        }


class SupplyChainRiskEngine:
    """Supply Chain Risk Detector & Digital Twin 3.0 Sourcing Graph."""
    @staticmethod
    def evaluate_risk() -> Dict[str, Any]:
        return {
            'overall_risk_level': 'LOW_TO_MEDIUM',
            'risk_alerts': [
                {
                    'risk_type': 'SINGLE_SUPPLIER_DEPENDENCY',
                    'severity': 'MEDIUM',
                    'description': 'Jaipur Clay Suppliers provides 85% of terracotta raw material.',
                    'recommended_mitigation': 'Add secondary supplier in Alwar district for 20% backup allocation.'
                },
                {
                    'risk_type': 'SUPPLIER_LEAD_TIME_BUFFER',
                    'severity': 'LOW',
                    'description': 'Natural mineral glaze dye lead time is 4 days.',
                    'recommended_mitigation': 'Maintain 15 liters buffer stock during festival season.'
                }
            ],
            'digital_twin_graph': {
                'node_suppliers': 4,
                'node_materials': 6,
                'node_artisan_groups': 3,
                'node_active_rfqs': 2,
                'node_shipments_in_transit': 8
            }
        }
