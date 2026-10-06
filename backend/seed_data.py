import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artisan_backend.settings')
django.setup()

from django.contrib.auth.models import User
from artisan_api.models import (
    ArtisanProfile, Product, ProductMedia, ProductFact, Variant, Inventory, Order, ProductStatus,
    Organization, OrganizationMember, Role, Campaign, Shipment, Payment,
    AgentMemory, BusinessKnowledge, ProductPassport, LLMCostTracker,
    AgentIdentity, AgentAuditTrail, BusinessGoalPlan, FeatureFlag
)

def seed():
    print("Seeding Prompt #3 Agentic Infrastructure Data...")
    user = User.objects.get(username='artisan_demo')
    product = Product.objects.filter(artisan=user).first()

    # 1. Agent Identity
    AgentIdentity.objects.get_or_create(
        agent_id='agent_google_shopping_01',
        defaults={
            'client_name': 'Google Shopping AI Assistant',
            'scopes': ['products:read', 'inventory:read', 'checkout:create'],
            'is_active': True
        }
    )

    # 2. Agent Audit Trail
    AgentAuditTrail.objects.get_or_create(
        agent_id='agent_google_shopping_01',
        action='SEARCH_PRODUCTS',
        defaults={
            'risk_level': 'READ',
            'input_summary': {'query': 'handmade blue pottery', 'max_budget': 1500},
            'result_summary': {'count': 3, 'status': 'success'}
        }
    )

    # 3. Autopilot Business Goal Plan
    BusinessGoalPlan.objects.get_or_create(
        artisan=user,
        goal='Increase Diwali Festival Sales by 30%',
        defaults={
            'plan_steps': [
                {'step': 1, 'action': 'Select Top Crafts', 'status': 'completed'},
                {'step': 2, 'action': 'Create 15% Discount Bundle', 'status': 'pending_approval'},
                {'step': 3, 'action': 'WhatsApp Broadcast Campaign', 'status': 'pending_approval'}
            ],
            'status': 'proposed'
        }
    )

    # 4. Feature Flags
    FeatureFlags = [
        ('AGENTIC_CHECKOUT', True, 'Enable server-side verified AI Agent checkout'),
        ('AI_AUTOPILOT', True, 'Enable goal-driven business autopilot planning'),
        ('EXTERNAL_AGENT_API', True, 'Expose machine-readable product catalog feed for external agents')
    ]
    for key, is_enabled, desc in FeatureFlags:
        FeatureFlag.objects.get_or_create(key=key, defaults={'is_enabled': is_enabled, 'description': desc})

    # 5. Mega Prompt #4 Seed Data: AI Tasks, Approval Inbox, Support Tickets, Event Mode
    from artisan_api.models import AITask, ApprovalInboxItem, SmartSupportTicket, EventExhibitionMode

    t1, _ = AITask.objects.get_or_create(
        title="Dynamic Price Adjustment: Jaipur Ceramic Vase",
        defaults={
            'assigned_team': 'BUSINESS_TEAM',
            'assigned_agent': 'Pricing Agent',
            'priority': 'HIGH',
            'status': 'WAITING_APPROVAL',
            'payload': {'current_price': 1499, 'proposed_price': 1299, 'margin_check': 'PASSED (+42%)'},
            'requires_approval': True
        }
    )

    ApprovalInboxItem.objects.get_or_create(
        task=t1,
        defaults={
            'action_type': 'PRICE_UPDATE',
            'summary': 'Pricing Agent proposes festive price adjustment from ₹1,499 to ₹1,299',
            'reason': 'Competitor price drop detected & festival demand surge starting in 3 days.',
            'expected_impact': 'Expected +35% unit sales surge, maintaining high profit margin.',
            'preview_data': {'sku': 'JV-001', 'old_price': 1499, 'new_price': 1299}
        }
    )

    t2, _ = AITask.objects.get_or_create(
        title="Multi-channel Social Campaign Broadcast: Diwali Handloom",
        defaults={
            'assigned_team': 'BUSINESS_TEAM',
            'assigned_agent': 'Marketing Agent',
            'priority': 'HIGH',
            'status': 'WAITING_APPROVAL',
            'payload': {'channels': ['Instagram', 'WhatsApp Business'], 'budget': 500},
            'requires_approval': True
        }
    )

    ApprovalInboxItem.objects.get_or_create(
        task=t2,
        defaults={
            'action_type': 'CAMPAIGN_BROADCAST',
            'summary': 'Marketing Agent generated Diwali Handloom Saree Reel & Broadcast Post',
            'reason': 'Peak social engagement window detected (7:30 PM IST).',
            'expected_impact': 'Estimated reach ~4,500 buyers, ~45 conversions.',
            'preview_data': {'caption': 'Celebrate Diwali with authentic handmade Pashmina Sarees! 🪔✨'}
        }
    )

    SmartSupportTicket.objects.get_or_create(
        issue="Logistics Delay Notification: Order #ORD-8821",
        defaults={
            'customer_context': {'customer': 'Rohan Sharma', 'city': 'Bangalore', 'order_value': 2499},
            'ai_summary': 'Transit delay due to regional weather. Package held at courier hub.',
            'suggested_resolution': 'Send automated WhatsApp apology voucher + 5% refund credit.',
            'priority': 'HIGH',
            'status': 'OPEN'
        }
    )

    event, _ = EventExhibitionMode.objects.get_or_create(
        event_name="Surajkund International Crafts Mela 2026",
        defaults={
            'location': 'Faridabad, Haryana (Stall #B-42)',
            'qr_code_slug': 'surajkund-2026',
            'is_active': True
        }
    )
    if product:
        event.event_products.add(product)

    # 6. Mega Prompt #5 Seed Data: Network Identity, Product Version, Market Experiment, AI Agents, DLQ
    from artisan_api.models import NetworkIdentity, ProductVersion, MarketExpansionExperiment, ThirdPartyAIAgent, DeadLetterQueueItem, ParticipantType, TrustLevel

    NetworkIdentity.objects.get_or_create(
        user=user,
        defaults={
            'participant_type': ParticipantType.ARTISAN,
            'trust_level': TrustLevel.PLATFORM_VERIFIED,
            'trust_signals': {
                'identity_verified': True,
                'organization_verified': True,
                'fulfillment_rate': '98.5%',
                'listing_completeness': '95%'
            }
        }
    )

    if product:
        ProductVersion.objects.get_or_create(
            product=product,
            version_number=1,
            defaults={
                'title': product.title,
                'price': product.price,
                'description': product.description,
                'provenance_sources': {
                    'material': 'ARTISAN_DECLARED',
                    'price': 'MERCHANT_CONFIGURED',
                    'description': 'AI_GENERATED'
                }
            }
        )

        exp, _ = MarketExpansionExperiment.objects.get_or_create(
            target_market='UAE',
            defaults={
                'artisan': user,
                'currency': 'AED',
                'status': 'ACTIVE',
                'metrics': {'views': 420, 'orders': 14, 'conversion': '3.3%', 'revenue_aed': 1850}
            }
        )
        exp.products.add(product)

    ThirdPartyAIAgent.objects.get_or_create(
        name="Global Craft Translator & Cultural Localizer Agent",
        defaults={
            'developer_name': 'LangCraft AI Labs',
            'version': 'v2.1',
            'pricing_model': 'USAGE_BASED',
            'required_scopes': ['products:read', 'products:write'],
            'rating': 4.92,
            'is_verified': True
        }
    )

    ThirdPartyAIAgent.objects.get_or_create(
        name="ONDC Smart Logistics & Rate Optimizer",
        defaults={
            'developer_name': 'LogiTech India',
            'version': 'v1.4',
            'pricing_model': 'FREE',
            'required_scopes': ['orders:read', 'shipments:create'],
            'rating': 4.88,
            'is_verified': True
        }
    )

    DeadLetterQueueItem.objects.get_or_create(
        task_type="MARKETPLACE_SYNC_ETSY",
        defaults={
            'payload': {'product_id': str(product.id) if product else 'sample_id', 'target_channel': 'Etsy Global'},
            'error_log': 'HTTP 504 Gateway Timeout during image media upload.',
            'retry_count': 2,
            'status': 'FAILED'
        }
    )

    # 7. Mega Prompt #6 Seed Data: Self-Improving AI, Prompt Experiments, Search Gaps
    from artisan_api.models import AILearningStore, PromptVersion, AIPromptExperiment, ProductSearchGap, LearningSource

    AILearningStore.objects.get_or_create(
        recommendation_title="High-Resolution Heritage Studio Lighting for Blue Pottery",
        defaults={
            'context': {'category': 'Pottery', 'original_ctr': '2.1%'},
            'action_taken': 'Applied AI Studio Enhancement & Cultural Background',
            'expected_outcome': 'Increase CTR by +15%',
            'actual_outcome': 'CTR increased from 2.1% to 3.4% (+61.9% relative lift)',
            'source': LearningSource.EXPERIMENT,
            'is_successful': True,
            'impact_delta': '+61.9% CTR'
        }
    )

    pv1, _ = PromptVersion.objects.get_or_create(
        prompt_key="catalog-extraction-agent",
        version="v1.0",
        defaults={
            'template_text': 'Extract craft attributes, materials, and pricing from artisan audio transcript.',
            'status': 'PRODUCTION',
            'evaluation_score': 92.40
        }
    )

    pv2, _ = PromptVersion.objects.get_or_create(
        prompt_key="catalog-extraction-agent",
        version="v2.0-canary",
        defaults={
            'template_text': 'Extract structured craft facts, material provenance (FACT/DECLARED), and pricing elasticity.',
            'status': 'CANARY',
            'evaluation_score': 96.80
        }
    )

    AIPromptExperiment.objects.get_or_create(
        experiment_name="Catalog Extraction v1 vs v2-canary A/B Test",
        defaults={
            'variant_a': pv1,
            'variant_b': pv2,
            'metrics_a': {'accuracy': '92.4%', 'latency_ms': 450, 'approval_rate': '88%'},
            'metrics_b': {'accuracy': '96.8%', 'latency_ms': 380, 'approval_rate': '95%'},
            'winning_variant': 'VARIANT_B'
        }
    )

    ProductSearchGap.objects.get_or_create(
        search_query="handmade terracotta tea cups",
        defaults={
            'query_count': 38,
            'category_hint': 'Terracotta & Pottery',
            'suggested_artisan_action': 'High unfulfilled customer search volume. Recommend Jaipur artisans create a 6-piece Terracotta Tea Cup set.',
            'status': 'OPEN'
        }
    )

    # 8. Mega Prompt #7 Seed Data: Signals, Opportunities, Goals, Daily Brief
    from artisan_api.models import BusinessSignal, Opportunity, BusinessGoal, AIPlan, DailyAIBrief

    BusinessSignal.objects.get_or_create(
        signal_type="LOW_CONVERSION",
        entity_id=str(product.id) if product else "sample_prod",
        defaults={
            'artisan': user,
            'entity_type': 'product',
            'severity': 'medium',
            'confidence': 0.88,
            'evidence': [{'source': 'views_count', 'value': 45}, {'source': 'orders_count', 'value': 1}]
        }
    )

    opp, _ = Opportunity.objects.get_or_create(
        title="Optimize Listing & Hero Image for Jaipur Ceramic Vase",
        defaults={
            'artisan': user,
            'opportunity_type': 'IMPROVE_PRODUCT_LISTING',
            'description': 'Product has high views (45) but low conversion (1 order). Studio lighting enhancement can boost orders.',
            'entity_type': 'product',
            'entity_id': str(product.id) if product else "sample_prod",
            'confidence': 0.91,
            'expected_impact': '+18-24% Conversion Lift',
            'urgency': 'HIGH',
            'possible_actions': [
                {'id': 'act_1', 'label': 'AI Studio Lighting & Cultural Background', 'risk': 'LOW'},
                {'id': 'act_2', 'label': 'Apply ₹100 First-Order Discount Coupon', 'risk': 'MEDIUM'}
            ],
            'status': 'discovered'
        }
    )

    bg, _ = BusinessGoal.objects.get_or_create(
        title="Increase Diwali Festive Revenue to ₹50,000",
        defaults={
            'artisan': user,
            'target_metric': 'REVENUE',
            'target_value': 50000.00,
            'current_value': 18450.00,
            'constraints': {'max_spend': 5000, 'max_discount_pct': 12},
            'autonomy_level': 2,
            'status': 'active'
        }
    )

    AIPlan.objects.get_or_create(
        goal=bg,
        title="Diwali Festive Demand & Inventory Clearance Plan",
        defaults={
            'steps': [
                {'step': 1, 'name': 'Audit Low-Turnover Inventory', 'status': 'completed'},
                {'step': 2, 'name': 'Create Festive Product Bundles', 'status': 'pending'},
                {'step': 3, 'name': 'WhatsApp Campaign Broadcast', 'status': 'pending'}
            ],
            'estimated_cost': 1200.00,
            'risk_level': 'MEDIUM',
            'status': 'in_progress'
        }
    )

    DailyAIBrief.objects.get_or_create(
        artisan=user,
        defaults={
            'orders_count': 12,
            'revenue_amount': 18450.00,
            'needs_attention': ['Jaipur Ceramic Vase (Low conversion)', 'Blue Pottery (Stock: 3 left)'],
            'opportunity_text': 'Your Terracotta Planter collection received 32% more views yesterday.',
            'suggested_action': 'Prepare a Diwali restock plan and offer a 10% bundle discount for repeat buyers.',
            'pending_approvals_count': 2
        }
    )

    # 9. Mega Prompt #8 Seed Data: Suppliers, Raw Materials, B2B RFQs, Split Allocations
    from artisan_api.models import (
        Supplier, RawMaterial, RequestForQuote, B2BQuotation, SplitOrderAllocation, QualityControlCheckpoint
    )

    sup1, _ = Supplier.objects.get_or_create(
        name="Jaipur High-Grade Raw Clay Suppliers",
        defaults={
            'category': 'Terracotta & Raw Clay',
            'materials_provided': ['Natural Terracotta Clay', 'Red Clay Powder', 'Glaze Mineral Dyes'],
            'location': 'Jaipur, Rajasthan',
            'lead_time_days': 4,
            'moq': 50,
            'unit_price': 65.00,
            'quality_rating': 4.90,
            'reliability_score': 98,
            'payment_terms': 'Net 30 Days'
        }
    )

    RawMaterial.objects.get_or_create(
        name="Natural Terracotta Clay",
        defaults={
            'supplier': sup1,
            'category': 'Clay',
            'price_per_unit': 65.00,
            'unit': 'kg',
            'moq': 50,
            'stock_available': 1200,
            'lead_time_days': 4
        }
    )

    rfq1, _ = RequestForQuote.objects.get_or_create(
        title="1,000 Handcrafted Blue Pottery Corporate Gift Sets",
        defaults={
            'buyer': user,
            'product_category': 'Handcrafted Corporate Gifts',
            'quantity': 1000,
            'target_unit_price': 750.00,
            'deadline_days': 25,
            'customization_requirements': 'Royal Blue glaze with custom silk pouch packaging',
            'status': 'OPEN'
        }
    )

    B2BQuotation.objects.get_or_create(
        rfq=rfq1,
        supplier_or_collective="Jaipur Master Artisans Collective",
        defaults={
            'offered_unit_price': 720.00,
            'lead_time_days': 20,
            'moq': 100,
            'customization_notes': 'Hand-embossed logo included with natural clay finish',
            'status': 'SUBMITTED'
        }
    )

    SplitOrderAllocation.objects.get_or_create(
        rfq=rfq1,
        artisan_group_name="Jaipur Master Artisans Collective",
        defaults={
            'artisan': user,
            'allocated_quantity': 400,
            'unit_payout': 650.00,
            'status': 'IN_PRODUCTION'
        }
    )

    QualityControlCheckpoint.objects.get_or_create(
        rfq=rfq1,
        stage="PRODUCTION_INSPECTION",
        defaults={
            'status': 'PASSED',
            'inspector_notes': 'Visual AI Inspection: Zero hairline cracks. Pigment & weight tolerances verified.'
        }
    )

    # 10. Mega Prompt #9 Seed Data: Global Profile, Markets, Trade Documents, Compliance RAG
    from artisan_api.models import (
        GlobalCommerceProfile, MarketProfile, TradeDocumentWorkspace, ComplianceKnowledgeRule, ExportReadinessScorecard
    )

    GlobalCommerceProfile.objects.get_or_create(
        user=user,
        defaults={
            'business_country': 'India',
            'business_region': 'Rajasthan',
            'preferred_currencies': ['USD', 'EUR', 'GBP', 'AED', 'INR'],
            'supported_languages': ['English', 'German', 'Hindi'],
            'export_readiness_score': 88,
            'documentation_status': 'VERIFIED'
        }
    )

    m_de, _ = MarketProfile.objects.get_or_create(
        country_code='DE',
        defaults={
            'country_name': 'Germany',
            'currency': 'EUR',
            'languages': ['German', 'English'],
            'regulatory_summary': 'EU GPSR labeling, VerpackG recycling registration, and food-grade ceramics standards.',
            'compliance_confidence': 0.95,
            'official_source_url': 'https://trade.gov/germany',
            'freshness_status': 'FRESH'
        }
    )

    TradeDocumentWorkspace.objects.get_or_create(
        reference_code='EXP-INV-2026-001',
        defaults={
            'user': user,
            'doc_type': 'COMMERCIAL_INVOICE',
            'title': 'Export Commercial Invoice - 500 Ceramic Vases to Berlin',
            'status': 'VERIFIED',
            'content_data': {'sku': 'JV-001', 'qty': 500, 'unit_price_usd': 37.50, 'consignee': 'Berlin Craft Import GmbH'}
        }
    )

    ComplianceKnowledgeRule.objects.get_or_create(
        country_code='DE',
        category='Packaging & Labeling',
        defaults={
            'requirement_summary': 'EU General Product Safety Regulation requires manufacturer address and material declaration.',
            'source_title': 'EU Customs & Single Market Portal',
            'source_url': 'https://ec.europa.eu/growth/single-market/goods/gpsr',
            'scope': 'HANDICRAFTS_CERAMICS'
        }
    )

    if product:
        ExportReadinessScorecard.objects.get_or_create(
            product=product,
            target_country='DE',
            defaults={
                'readiness_status': 'READY',
                'readiness_breakdown': {'catalog': True, 'localization': True, 'pricing': True, 'shipping': True, 'documents': True},
                'missing_items': ['Confirm EU GPSR label printing'],
                'action_plan': [{'step': 1, 'task': 'Publish German Localized Listing'}]
            }
        )

    # 11. Mega Prompt #10 Seed Data: Agent Purchase Policy, Tool Definitions, Negotiation Session, Attribution
    from artisan_api.models import (
        AgentPurchasePolicy, AgentToolDefinition, AgentNegotiationSession, AgentAttributionLog
    )

    AgentPurchasePolicy.objects.get_or_create(
        user=user,
        defaults={
            'max_order_value': 3000.00,
            'requires_confirmation_above': 1500.00,
            'daily_budget_limit': 5000.00,
            'allowed_categories': ['Pottery & Handicrafts', 'Home Decor', 'Handloom Sarees']
        }
    )

    AgentToolDefinition.objects.get_or_create(
        name="product_search_v1",
        defaults={
            'description': 'Search canonical product catalog with structured filters',
            'version': 'v1.0',
            'risk_level': 'READ',
            'required_scopes': ['products:read']
        }
    )

    AgentToolDefinition.objects.get_or_create(
        name="rfq_negotiate_v1",
        defaults={
            'description': 'Execute structured B2B negotiation counter-offers',
            'version': 'v1.0',
            'risk_level': 'SENSITIVE',
            'required_scopes': ['rfq:write', 'quotes:read']
        }
    )

    AgentNegotiationSession.objects.get_or_create(
        buyer_agent_id="buyer_agent_google_shopping_01",
        defaults={
            'seller_agent_id': 'seller_agent_jaipur_collective_01',
            'rfq_id': 'rfq_demo_01',
            'status': 'AGREED_PENDING_APPROVAL',
            'offers_history': [
                {'round': 1, 'agent': 'Buyer Agent', 'offered_price': 700.0},
                {'round': 2, 'agent': 'Seller Agent', 'asking_price': 750.0}
            ],
            'agreement_data': {'agreed_unit_price': 725.0, 'total_contract_value': 725000.0}
        }
    )

    AgentAttributionLog.objects.get_or_create(
        agent_id="personal_shopping_agent_01",
        action_type="PURCHASE",
        defaults={
            'source_type': 'AI_AGENT',
            'gmv_impact': 1499.00
        }
    )

    # 12. Mega Prompt #11 Seed Data: Social Commerce, Creator Economy & Autonomous Growth Network
    from artisan_api.models import (
        SocialProfile, ContentAsset, ContentCampaign, ContentSchedule,
        CreatorProfile, CreatorCampaign, Referral, AffiliateCommission,
        Community, CommunityPost, LiveSession
    )

    SocialProfile.objects.get_or_create(
        user=user,
        defaults={
            'roles': ['artisan', 'creator', 'affiliate'],
            'bio': 'Master Ceramic Artisan from Jaipur creating traditional blue pottery.',
            'craft_story': 'Handcrafting heritage pottery with organic minerals and cobalt glaze.',
            'craft_region': 'Jaipur, Rajasthan',
            'verified_info': {'artisan_id_verified': True, 'org_verified': True}
        }
    )

    asset1, _ = ContentAsset.objects.get_or_create(
        title="Jaipur Blue Pottery Festive Reel Script",
        defaults={
            'artisan': user,
            'product': product,
            'content_type': 'short_video_script',
            'channel': 'instagram',
            'script_text': '0-3s: Close up of blue glaze. 3-10s: Artisan shaping vase. 20-30s: Available now for ₹1,850!',
            'caption': '✨ Bringing authentic Jaipur pottery to your festive home! Handcrafted by master artisans.',
            'status': 'approved',
            'factuality_status': 'VERIFIED_GROUNDED',
            'price_consistency_status': 'VALIDATED'
        }
    )

    camp1, _ = ContentCampaign.objects.get_or_create(
        title="Diwali Handcrafted Gifting Campaign",
        defaults={
            'artisan': user,
            'objective': 'Drive 50,000 views and ₹100k sales during festival season',
            'channels': ['instagram', 'whatsapp', 'facebook'],
            'budget': 5000.00,
            'estimated_reach': 25000,
            'status': 'active'
        }
    )

    creator_user, _ = User.objects.get_or_create(username='craft_influencer_ananya', defaults={'email': 'ananya@creator.org'})
    creator_prof, _ = CreatorProfile.objects.get_or_create(
        user=creator_user,
        defaults={
            'name': 'Ananya Roy - Craft & Lifestyle',
            'bio': 'Sharing authentic Indian craftsmanship, heritage decor, and sustainable living.',
            'categories': ['Pottery & Handicrafts', 'Home Decor', 'Handicrafts'],
            'content_style': 'Aesthetic Unboxing & Heritage Storytelling',
            'approved_metrics': {'avg_reach': 35000, 'engagement_rate': '5.2%'}
        }
    )

    collab, _ = CreatorCampaign.objects.get_or_create(
        artisan=user,
        creator=creator_user,
        defaults={
            'campaign': camp1,
            'requirements': '1x Unboxing Reel + 1 Story link',
            'fixed_compensation': 1500.00,
            'commission_rate': 5.00,
            'status': 'ACCEPTED'
        }
    )
    if product:
        collab.products.add(product)

    ref1, _ = Referral.objects.get_or_create(
        referral_code='ANANYA_CRAFT_2026',
        defaults={
            'referrer': creator_user,
            'status': 'CONVERTED',
            'total_clicks': 120,
            'total_conversions': 4,
            'reward_amount': 400.00
        }
    )

    if product:
        AffiliateCommission.objects.get_or_create(
            creator=creator_user,
            referral=ref1,
            product=product,
            defaults={
                'sale_amount': product.price,
                'commission_rate': 5.00,
                'commission_earned': (product.price * 5) / 100,
                'payout_status': 'APPROVED'
            }
        )

    comm1, _ = Community.objects.get_or_create(
        name="Indian Craft Heritage Circle",
        defaults={
            'owner': user,
            'topic_category': 'Craft Education & Care',
            'description': 'A community for artisans, collectors, and decor lovers celebrating Indian heritage.',
            'member_count': 1420
        }
    )

    CommunityPost.objects.get_or_create(
        community=comm1,
        title="How to clean and care for unglazed terracotta pottery?",
        defaults={
            'author': user,
            'body': 'Avoid harsh chemical detergents. Soak in warm water with vinegar or baking soda for 15 minutes and dry in sunlight.',
            'post_type': 'TUTORIAL',
            'verified_answer_flag': True,
            'status': 'PUBLISHED'
        }
    )

    # 13. Mega Prompt #12 Seed Data: AI Finance, Operations & Business Intelligence OS
    from artisan_api.models import (
        LedgerEntry, Expense, Invoice, SettlementReconciliation,
        FinancialScenario, FinancialAnomaly, PlatformBillingMeter
    )

    LedgerEntry.objects.get_or_create(
        reference_id='ORD_DEMO_2026',
        defaults={
            'artisan': user,
            'entry_type': 'SALE',
            'reference_type': 'ORDER',
            'amount': product.price if product else 1850.00,
            'direction': 'CREDIT',
            'category': 'Revenue',
            'status': 'POSTED'
        }
    )

    LedgerEntry.objects.get_or_create(
        reference_id='EXP_DEMO_001',
        defaults={
            'artisan': user,
            'entry_type': 'EXPENSE',
            'reference_type': 'EXPENSE',
            'amount': 350.00,
            'direction': 'DEBIT',
            'category': 'Packaging',
            'status': 'POSTED'
        }
    )

    Expense.objects.get_or_create(
        vendor_name="Jaipur Silk & Packaging Suppliers",
        defaults={
            'artisan': user,
            'category': 'Packaging',
            'amount': 350.00,
            'cost_center': 'Operations',
            'ai_confidence': 0.96,
            'status': 'APPROVED'
        }
    )

    Invoice.objects.get_or_create(
        invoice_number='INV-2026-8801',
        defaults={
            'artisan': user,
            'customer_name': 'Rohan Sharma',
            'invoice_type': 'B2C',
            'total_amount': 1850.00,
            'tax_amount': 92.50,
            'status': 'PAID'
        }
    )

    SettlementReconciliation.objects.get_or_create(
        marketplace_name="Amazon Handmade India",
        defaults={
            'artisan': user,
            'expected_amount': 8420.00,
            'actual_amount': 8120.00,
            'difference_amount': 300.00,
            'status': 'MISMATCH',
            'mismatch_reason': 'Settlement discrepancy of ₹300. Investigating gateway fees & return adjustments.'
        }
    )

    FinancialScenario.objects.get_or_create(
        scenario_name="Diwali 5% Price Reduction Simulation",
        defaults={
            'artisan': user,
            'price_change_pct': -5.00,
            'volume_change_pct': 15.00,
            'estimated_revenue_impact': 9250.00,
            'estimated_margin_impact': 4120.00
        }
    )

    FinancialAnomaly.objects.get_or_create(
        anomaly_type="SETTLEMENT_MISMATCH",
        defaults={
            'artisan': user,
            'severity': 'HIGH',
            'evidence': {'expected': 8420.00, 'actual': 8120.00, 'discrepancy': 300.00},
            'status': 'OPEN'
        }
    )

    PlatformBillingMeter.objects.get_or_create(
        user=user,
        defaults={
            'subscription_plan': 'GROWTH',
            'total_llm_tokens': 142000,
            'total_ai_cost': 28.40,
            'api_calls_count': 1240
        }
    )

    print("Mega Prompt #12 AI Finance, Operations & Business Intelligence OS Seed Complete!")

    # --- PROMPT #13 SEEDING: AI WORKFORCE OS & DIGITAL EMPLOYEES ---
    print("Seeding Prompt #13 AI Workforce OS Data...")
    from artisan_api.services.workforce_engine import DigitalEmployeeFactory, SOPConverterEngine
    from artisan_api.models import DigitalEmployee, AITeam, AISOP, WorkforceTask, WorkforceIncident

    # 1. Seed Default Digital Employees
    employees = DigitalEmployeeFactory.seed_default_employees(user)

    # 2. Seed Default AI Teams
    team, _ = AITeam.objects.get_or_create(
        artisan=user,
        name='Diwali Festival Preparation Team',
        defaults={
            'mission': 'Maximize Diwali sales velocity while preserving cash margins & stock levels.',
            'team_roles': ['GROWTH_MANAGER', 'FINANCE_ANALYST', 'OPERATIONS_MANAGER'],
            'budget': 25000.00,
            'current_spend': 45.00
        }
    )

    # 3. Seed Default AISOP
    sop, _ = AISOP.objects.get_or_create(
        artisan=user,
        sop_code='SOP-FEST-01',
        defaults={
            'title': 'Diwali Festival Sales & Procurement SOP',
            'category': 'Operations',
            'content': """# Diwali Sales SOP
1. Validate campaign target and cash flow reserves.
2. Require human manager signoff for ad spend > ₹10,000.
3. Pre-order raw clay inventory when stock is < 30 units.""",
            'source_authority': 'Head of Commerce Operations'
        }
    )
    SOPConverterEngine.convert_sop_to_dag(sop)

    # 4. Seed Default Workforce Task
    emp_growth = DigitalEmployee.objects.filter(artisan=user, role='GROWTH_MANAGER').first()
    WorkforceTask.objects.get_or_create(
        artisan=user,
        title='Diwali Festival Sales Campaign Audit',
        defaults={
            'assigned_employee': emp_growth,
            'team': team,
            'task_type': 'CAMPAIGN_PLANNING',
            'goal': 'Analyze past campaign conversions and draft ₹15,000 ad budget proposal.',
            'priority': 'HIGH',
            'status': 'WAITING_APPROVAL',
            'approval_required': True,
            'approval_status': 'PENDING',
            'approval_reason': 'Ad campaign budget exceeds ₹10,000 policy threshold.',
            'sop_reference': sop,
            'shared_memory': {
                'projected_revenue': '₹1,45,000',
                'target_margin': '29.5%',
                'recommended_ad_budget': '₹15,000'
            }
        }
    )

    # 5. Seed Workforce Incident
    WorkforceIncident.objects.get_or_create(
        artisan=user,
        incident_type='POLICY_CHECK_ENFORCED',
        defaults={
            'employee': emp_growth,
            'severity': 'LOW',
            'details': {'policy': 'Ad spend limit of ₹10,000 triggered mandatory human approval request.'},
            'status': 'RESOLVED'
        }
    )

    print("Mega Prompt #13 AI Workforce OS Seed Complete!")

    # --- PROMPT #14 SEEDING: AI TRUST, GOVERNANCE, PRIVACY & SECURITY ---
    print("Seeding Prompt #14 AI Trust, Governance, Privacy & Security Data...")
    from artisan_api.services.trust_governance_engine import (
        CentralPolicyEngine, DEFAULT_TOOL_TRUST_RECORDS, DEFAULT_GOVERNANCE_CONTROLS
    )
    from artisan_api.models import (
        GovernancePolicy, ToolTrustRecord, ConsentRecord,
        SecurityEvent, ModelRegistry, GovernanceControl
    )

    # 1. Seed Governance Policies
    CentralPolicyEngine.seed_default_policies(user)

    # 2. Seed Tool Trust Records
    for t_data in DEFAULT_TOOL_TRUST_RECORDS:
        ToolTrustRecord.objects.get_or_create(tool_name=t_data['tool_name'], defaults=t_data)

    # 3. Seed Governance Controls
    for c_data in DEFAULT_GOVERNANCE_CONTROLS:
        GovernanceControl.objects.get_or_create(control_code=c_data['control_code'], defaults=c_data)

    # 4. Seed Consents
    for purp in ['MARKETING', 'PERSONALIZATION', 'AI_PROCESSING', 'ANALYTICS']:
        ConsentRecord.objects.get_or_create(user=user, purpose=purp, defaults={'status': 'GRANTED'})

    # 5. Seed Security Event
    SecurityEvent.objects.get_or_create(
        artisan=user,
        event_type='INDIRECT_PROMPT_INJECTION_BLOCKED',
        defaults={
            'actor_type': 'HUMAN',
            'actor_id': 'artisan_demo',
            'severity': 'HIGH',
            'details': {'reason': 'Indirect prompt injection in untrusted PDF attachment blocked by Security Firewall.'},
            'status': 'RESOLVED'
        }
    )

    # 6. Seed Model Registry
    ModelRegistry.objects.get_or_create(
        model_name='gemini-2.5-pro-secure',
        defaults={'provider': 'Google DeepMind', 'purpose': 'REASONING', 'privacy_level': 'HIGH', 'approval_status': 'APPROVED'}
    )

    print("Mega Prompt #14 AI Trust & Governance Seed Complete!")

    # --- PROMPT #15 SEEDING: AI KNOWLEDGE FABRIC & ORGANIZATIONAL BRAIN ---
    print("Seeding Prompt #15 AI Knowledge Fabric & Organizational Brain Data...")
    from artisan_api.models import (
        KnowledgeSource, KnowledgeObject, KnowledgeGraphNode, KnowledgeGraphEdge,
        DecisionMemory, KnowledgeConflictRecord, KnowledgeGapRecord
    )
    from artisan_api.services.organizational_brain_engine import OrganizationalBrainEngine

    # 1. Knowledge Sources
    ks1, _ = KnowledgeSource.objects.get_or_create(
        artisan=user,
        name="Master Supplier Quality SOP 2026",
        defaults={
            'source_type': 'SOP',
            'trust_level': 'AUTHORITATIVE',
            'classification': 'INTERNAL',
            'owner': 'Quality Assurance Team',
            'version': 'v2.1',
            'freshness_status': 'FRESH'
        }
    )

    ks2, _ = KnowledgeSource.objects.get_or_create(
        artisan=user,
        name="Festival Campaign Strategy & Lessons Learned 2025",
        defaults={
            'source_type': 'DOCUMENT',
            'trust_level': 'VERIFIED',
            'classification': 'INTERNAL',
            'owner': 'Growth Marketing',
            'version': 'v1.0',
            'freshness_status': 'FRESH'
        }
    )

    # 2. Knowledge Objects
    ko1, _ = KnowledgeObject.objects.get_or_create(
        artisan=user,
        title="Pashmina Warp Thread Density Standard",
        defaults={
            'source': ks1,
            'knowledge_type': 'SOP',
            'content': "Handloom Pashmina Shawls must maintain a minimum warp density of 64 threads/inch. Variation above 3% triggers mandatory QC batch hold.",
            'summary': "Minimum 64 threads/inch warp density required for Pashmina Shawls.",
            'confidence_level': 'HIGH',
            'freshness_status': 'FRESH',
            'classification': 'INTERNAL',
            'status': 'APPROVED'
        }
    )

    ko2, _ = KnowledgeObject.objects.get_or_create(
        artisan=user,
        title="Gift Bundle Conversion Lift Principle",
        defaults={
            'source': ks2,
            'knowledge_type': 'INSIGHT',
            'content': "Artisan gift bundles with story cards generate 3.4x higher conversion lift compared to standalone price discounts.",
            'summary': "Story-backed gift bundles outperform flat discounts by 3.4x.",
            'confidence_level': 'HIGH',
            'freshness_status': 'FRESH',
            'classification': 'INTERNAL',
            'status': 'APPROVED'
        }
    )

    # 3. Knowledge Graph Nodes & Edges
    node_sup, _ = KnowledgeGraphNode.objects.get_or_create(
        artisan=user,
        name="Silk Craft Co",
        defaults={'entity_type': 'Supplier', 'trust_level': 'AUTHORITATIVE', 'attributes': {'location': 'Varanasi', 'rating': 98.5}}
    )

    node_prod, _ = KnowledgeGraphNode.objects.get_or_create(
        artisan=user,
        name="Handloom Pashmina Shawl",
        defaults={'entity_type': 'Product', 'trust_level': 'VERIFIED', 'attributes': {'sku': 'PS-101', 'price': 3499}}
    )

    node_sop, _ = KnowledgeGraphNode.objects.get_or_create(
        artisan=user,
        name="Master Supplier Quality SOP 2026",
        defaults={'entity_type': 'SOP', 'trust_level': 'AUTHORITATIVE', 'attributes': {'owner': 'QA Team'}}
    )

    KnowledgeGraphEdge.objects.get_or_create(
        source_node=node_sup,
        target_node=node_prod,
        relationship="SUPPLIES",
        defaults={'confidence': 'HIGH'}
    )

    KnowledgeGraphEdge.objects.get_or_create(
        source_node=node_sop,
        target_node=node_prod,
        relationship="GOVERNS",
        defaults={'confidence': 'HIGH'}
    )

    # 4. Decision Memory
    DecisionMemory.objects.get_or_create(
        artisan=user,
        title="Festival Bundle Discount Optimization DM-2025",
        defaults={
            'category': 'CAMPAIGN_STRATEGY',
            'decision_summary': "Reduced festival campaign discount from 15% to 10% while adding complimentary artisan wooden gift box.",
            'rationale_and_evidence': {'conversion_impact': '+340%', 'margin_gain': '+8.4%', 'evidence': 'A/B test campaign #14'},
            'approved_by': 'Business Owner',
            'actual_outcome': 'Achieved highest net revenue quarter in company history.',
            'confidence_score': 0.96
        }
    )

    # 5. Knowledge Conflict & Gap
    OrganizationalBrainEngine.resolve_knowledge_conflict(
        user,
        topic="Silk Yarn Lead Time",
        source_a_name="Master Supplier Quality SOP 2026",
        val_a="7 days",
        trust_a="AUTHORITATIVE",
        source_b_name="Supplier Portal Self-Report",
        val_b="10 days",
        trust_b="SECONDARY"
    )

    KnowledgeGapRecord.objects.get_or_create(
        artisan=user,
        topic="High-Volume B2B Production Audit Evidence for >5000 Units",
        defaults={
            'demand_score': 'HIGH',
            'current_coverage_pct': 42.0,
            'recommended_action': 'Schedule third-party factory capacity audit for Artisan Yarns Pvt Ltd.',
            'assigned_owner': 'Procurement Compliance Lead',
            'status': 'OPEN'
        }
    )

    print("Mega Prompt #15 AI Knowledge Fabric Seed Complete!")

    # --- PROMPT #16 SEEDING: AI DIGITAL TWIN, BUSINESS SIMULATION & STRATEGY LAB ---
    print("Seeding Prompt #16 AI Digital Twin & Strategy Lab Data...")
    from artisan_api.services.digital_twin_engine import DigitalTwinEngine
    from artisan_api.models import ScenarioCalibration, BusinessScenario

    # 1. Build Baseline Twin Snapshot & Flagship Demo
    demo_out = DigitalTwinEngine.run_flagship_strategy_lab_demo(user)

    # 2. Seed Historical Scenario Calibration
    sc_calib = BusinessScenario.objects.filter(artisan=user).first()
    if sc_calib:
        ScenarioCalibration.objects.get_or_create(
            scenario=sc_calib,
            artisan=user,
            defaults={
                'predicted_revenue_inr': 295000.00,
                'actual_revenue_inr': 282400.00,
                'forecast_error_pct': 4.27,
                'calibration_notes': 'Diwali campaign demand elasticity was predicted within 4.3% margin of accuracy.'
            }
        )

    print("Mega Prompt #16 AI Digital Twin & Strategy Lab Seed Complete!")

    # --- PROMPT #18 SEEDING: AI CAUSAL INTELLIGENCE, EXPERIMENTATION & OUTCOME LEARNING ---
    print("Seeding Prompt #18 AI Causal Intelligence & Experimentation Data...")
    from artisan_api.services.causal_intelligence_engine import CausalIntelligenceEngine
    causal_demo_out = CausalIntelligenceEngine.run_flagship_causal_demo(user)
    print("Mega Prompt #18 AI Causal Intelligence & Experimentation Seed Complete!")

    # --- PROMPT #19 SEEDING: AI MARKET INTELLIGENCE, COMPETITIVE INTELLIGENCE & OPPORTUNITY DISCOVERY ---
    print("Seeding Prompt #19 AI Market Intelligence & Opportunity Discovery Data...")
    from artisan_api.services.market_intelligence_engine import MarketIntelligenceEngine
    market_demo_out = MarketIntelligenceEngine.run_flagship_market_demo(user)
    print("Mega Prompt #19 AI Market Intelligence & Opportunity Discovery Seed Complete!")

    # --- PROMPT #20 SEEDING: AI NETWORK INTELLIGENCE & ECOSYSTEM OS ---
    print("Seeding Prompt #20 AI Network Intelligence & Ecosystem Coordination Data...")
    from decimal import Decimal
    from artisan_api.models import (
        NetworkEntityGraphNode, NetworkRelationshipEdge, NetworkSignalMessage,
        NetworkDemandPool, NetworkCapacityResource, NetworkEcosystemOpportunity, NetworkMultiPartyMatch
    )
    from artisan_api.services.network_intelligence_engine import NetworkIntelligenceEngine

    node1, _ = NetworkEntityGraphNode.objects.get_or_create(
        entity_id="node_artisan_jaipur_01",
        defaults={
            'artisan': user,
            'entity_name': 'Jaipur Master Artisan Collective',
            'entity_type': 'ARTISAN',
            'verification_status': 'VERIFIED',
            'location_region': 'Jaipur, Rajasthan',
            'capabilities': 'Blue Pottery, Heritage Crafting, Hand-glazing',
            'trust_score': Decimal('0.95'),
            'privacy_consent_level': 'OPT_IN_AGGREGATE'
        }
    )

    node2, _ = NetworkEntityGraphNode.objects.get_or_create(
        entity_id="node_supplier_silk_01",
        defaults={
            'artisan': user,
            'entity_name': 'Silk Craft Raw Materials & Dyes Co',
            'entity_type': 'SUPPLIER',
            'verification_status': 'VERIFIED',
            'location_region': 'Varanasi, Uttar Pradesh',
            'capabilities': 'Natural Dyes, Organic Silk, Terracotta Minerals',
            'trust_score': Decimal('0.92'),
            'privacy_consent_level': 'SHARED_PARTNER'
        }
    )

    node3, _ = NetworkEntityGraphNode.objects.get_or_create(
        entity_id="node_buyer_corporate_01",
        defaults={
            'artisan': user,
            'entity_name': 'Taj Hotels & Resorts B2B Procurement',
            'entity_type': 'B2B_BUYER',
            'verification_status': 'ENTERPRISE',
            'location_region': 'Mumbai, Maharashtra',
            'capabilities': 'Luxury Artisanal Gift Box Procurement',
            'trust_score': Decimal('0.98'),
            'privacy_consent_level': 'OPT_IN_AGGREGATE'
        }
    )

    node4, _ = NetworkEntityGraphNode.objects.get_or_create(
        entity_id="node_logistics_express_01",
        defaults={
            'artisan': user,
            'entity_name': 'Express Craft Logistics Network',
            'entity_type': 'LOGISTICS',
            'verification_status': 'VERIFIED',
            'location_region': 'National Network, India',
            'capabilities': 'Fragile Craft Express Freight & Temperature Control',
            'trust_score': Decimal('0.94'),
            'privacy_consent_level': 'FULL'
        }
    )

    NetworkRelationshipEdge.objects.get_or_create(
        artisan=user,
        source_node=node1,
        target_node=node2,
        relationship_type='ORDERS_FROM',
        defaults={'strength_weight': Decimal('0.90'), 'is_active': True, 'metadata_info': 'Raw Material Procurement'}
    )

    NetworkRelationshipEdge.objects.get_or_create(
        artisan=user,
        source_node=node3,
        target_node=node1,
        relationship_type='BUYS',
        defaults={'strength_weight': Decimal('0.95'), 'is_active': True, 'metadata_info': 'Bulk B2B Artisanal Order Contract'}
    )

    NetworkSignalMessage.objects.get_or_create(
        artisan=user,
        signal_type='DEMAND_SURGE',
        defaults={
            'source_category': 'B2B_RFQ_AGGREGATION',
            'category': 'Ceramics & Home Decor',
            'location_scope': 'Northern India Region',
            'confidence': Decimal('0.93'),
            'privacy_level': 'AGGREGATED_ANONYMOUS',
            'payload_json': '{"aggregated_rfqs": 4, "total_units_requested": 5000}'
        }
    )

    NetworkDemandPool.objects.get_or_create(
        artisan=user,
        pool_name='Diwali Festive Corporate Gift Sets Pool',
        defaults={
            'product_category': 'Ceramics & Decor',
            'aggregated_units': 5000,
            'participating_buyers_count': 4,
            'target_delivery_days': 20,
            'target_unit_price_inr': Decimal('450.00'),
            'feasibility_status': 'FEASIBLE'
        }
    )

    NetworkCapacityResource.objects.get_or_create(
        artisan=user,
        cluster_name='Jaipur Artisan Cooperative Cluster',
        defaults={
            'resource_type': 'PRODUCTION',
            'available_units_per_week': 5600,
            'utilization_rate_pct': Decimal('45.00'),
            'location_region': 'Jaipur, Rajasthan',
            'is_available_for_pooling': True
        }
    )

    NetworkEcosystemOpportunity.objects.get_or_create(
        artisan=user,
        title='Regional Sustainable Corporate Gifting Network Cluster',
        defaults={
            'opportunity_type': 'GROUP_PROCUREMENT',
            'match_score': 94,
            'estimated_economic_value_inr': Decimal('2250000.00'),
            'participating_nodes_summary': '25 Artisans + 3 Raw Material Suppliers + 2 Express Logistics Networks',
            'why_now_reason': '5,000 unit corporate gift pool aligned with 55% unused Jaipur pottery cluster capacity.',
            'status': 'OPEN'
        }
    )

    network_demo_out = NetworkIntelligenceEngine.run_flagship_network_demo(user)
    print("Mega Prompt #20 AI Network Intelligence & Ecosystem Coordination Seed Complete!")

    # --- PROMPT #21 SEEDING: AI CUSTOMER 360 & PERSONAL COMMERCE OS ---
    print("Seeding Prompt #21 AI Customer 360 & Personal Commerce OS Data...")
    from artisan_api.models import (
        CustomerPreferenceProfile, CustomerCommerceMemory, ShoppingSessionIntent,
        CustomerShortlist, CustomerConsentPreference
    )
    from artisan_api.services.customer_360_engine import Customer360PersonalCommerceEngine

    CustomerPreferenceProfile.objects.get_or_create(
        customer=user,
        defaults={
            'preferred_categories': 'Ceramics & Decor, Home Living, Festive Gifts',
            'preferred_price_min_inr': Decimal('500.00'),
            'preferred_price_max_inr': Decimal('3000.00'),
            'preferred_materials': 'Organic Terracotta, Cobalt Blue Glaze, Silk',
            'preferred_languages': 'Hindi, English',
            'gift_intent_frequency': 'HIGH',
            'inferred_style': 'Authentic Traditional & Modern Heritage',
            'privacy_mode': 'STANDARD'
        }
    )

    CustomerCommerceMemory.objects.get_or_create(
        customer=user,
        memory_key='festive_eco_gift_preference',
        defaults={
            'memory_type': 'EXPLICIT_PREFERENCE',
            'memory_value': 'Customer prefers eco-friendly handmade gifts under ₹2,000 for festival occasions.',
            'confidence_score': Decimal('0.94'),
            'provenance_source': 'USER_EXPLICIT_INPUT',
            'is_editable': True
        }
    )

    CustomerCommerceMemory.objects.get_or_create(
        customer=user,
        memory_key='preferred_region_jaipur_pottery',
        defaults={
            'memory_type': 'BEHAVIORAL_INSIGHT',
            'memory_value': 'Customer highly engages with authentic Jaipur blue pottery and terracotta items.',
            'confidence_score': Decimal('0.91'),
            'provenance_source': 'SEARCH_HISTORY',
            'is_editable': True
        }
    )

    intent_obj = ShoppingSessionIntent.objects.filter(customer=user, raw_query='Mujhe 2000 ke andar sister ke birthday ke liye handmade unique gift chahiye.').first()
    if not intent_obj:
        intent_obj = ShoppingSessionIntent.objects.create(
            customer=user,
            raw_query='Mujhe 2000 ke andar sister ke birthday ke liye handmade unique gift chahiye.',
            intent_type='GIFT_SHOPPING',
            extracted_category='Handmade Gift Sets',
            budget_max_inr=Decimal('2000.00'),
            target_delivery_days=5,
            recipient_type='Sister',
            occasion='Birthday',
            extracted_constraints_json='{"style": "unique", "material": "handmade ceramic/clay"}',
            status='ACTIVE'
        )

    CustomerShortlist.objects.get_or_create(
        customer=user,
        product=product,
        defaults={
            'shortlist_name': 'Birthday Gift Shortlist',
            'intent': intent_obj,
            'personal_fit_score': 95,
            'fit_explanation': 'Handmade authentic terracotta vase within your ₹2,000 budget with 4-day express delivery.',
            'tradeoffs_summary': 'Handcrafted glazing details; rated 4.9/5 by buyers.'
        }
    )

    CustomerConsentPreference.objects.get_or_create(
        customer=user,
        defaults={
            'allow_personalization': True,
            'allow_ai_memory': True,
            'allow_recommendations': True,
            'allow_behavioral_analytics': True,
            'allow_voice_vision_search': True
        }
    )

    customer_demo_out = Customer360PersonalCommerceEngine.run_flagship_customer_demo(user)
    print("Mega Prompt #21 AI Customer 360 & Personal Commerce OS Seed Complete!")

    # --- PROMPT #22 SEEDING: AI OMNICHANNEL, PHYGITAL COMMERCE & PHYSICAL WORLD INTELLIGENCE OS ---
    print("Seeding Prompt #22 AI Omnichannel, Phygital Commerce & Physical World Intelligence OS Data...")
    from artisan_api.models import (
        Store, StoreInventory, OmnichannelSession, QRAsset,
        KioskSession, PickupReservation, ExhibitionEvent, OfflineSyncQueue
    )
    from artisan_api.services.phygital_omnichannel_engine import PhygitalOmnichannelCommerceEngine

    st1, _ = Store.objects.get_or_create(
        name="Jaipur Flagship Heritage Store",
        defaults={
            'owner': user,
            'store_type': 'PERMANENT',
            'address': '77 Johari Bazaar, Pink City',
            'city': 'Jaipur',
            'region': 'Rajasthan',
            'contact_phone': '+91 98290 12345',
            'operating_hours': '10:00 AM - 08:00 PM IST',
            'capabilities_json': '{"pickup": true, "qr_enabled": true, "kiosk_enabled": true, "staff_copilot": true}'
        }
    )

    st2, _ = Store.objects.get_or_create(
        name="Delhi Crafts Union Pop-up Hub",
        defaults={
            'owner': user,
            'store_type': 'POP_UP',
            'address': 'Hauz Khas Craft Village, Stall 14',
            'city': 'New Delhi',
            'region': 'Delhi NCR',
            'contact_phone': '+91 98110 54321',
            'operating_hours': '11:00 AM - 09:00 PM IST',
            'capabilities_json': '{"pickup": true, "qr_enabled": true, "kiosk_enabled": false, "staff_copilot": true}'
        }
    )

    if product:
        StoreInventory.objects.get_or_create(
            store=st1,
            product=product,
            defaults={
                'quantity_available': 18,
                'quantity_reserved': 2,
                'low_stock_threshold': 4
            }
        )
        StoreInventory.objects.get_or_create(
            store=st2,
            product=product,
            defaults={
                'quantity_available': 8,
                'quantity_reserved': 0,
                'low_stock_threshold': 2
            }
        )

    qr1, _ = QRAsset.objects.get_or_create(
        qr_code_key="FLAGSHIP-DEMO-QR-001",
        defaults={
            'qr_type': 'PRODUCT_QR',
            'product': product,
            'store': st1,
            'resolution_target_url': 'https://artisancommerce.os/qr/resolve/FLAGSHIP-DEMO-QR-001',
            'scans_count': 42
        }
    )

    OmnichannelSession.objects.get_or_create(
        customer=user,
        session_token="SESSION-OMNI-JAIPUR-001",
        defaults={
            'channel': 'STORE',
            'current_store': st1,
            'context_json': '{"active_intent": "Gift Shopping", "last_qr_scanned": "FLAGSHIP-DEMO-QR-001"}'
        }
    )

    KioskSession.objects.get_or_create(
        kiosk_device_id="KIOSK_JAIPUR_01",
        defaults={
            'store': st1,
            'active_customer': user,
            'status': 'TRANSFERRED'
        }
    )

    if product:
        PickupReservation.objects.get_or_create(
            pickup_code="PICKUP-DEMO-99",
            defaults={
                'customer': user,
                'store': st1,
                'product': product,
                'quantity': 1,
                'status': 'READY_FOR_PICKUP'
            }
        )

    ExhibitionEvent.objects.get_or_create(
        name="National Heritage Handloom & Craft Expo 2026",
        defaults={
            'event_type': 'CRAFT_FAIR',
            'city': 'New Delhi',
            'participating_artisans_json': f'["{user.username}"]',
            'status': 'ACTIVE'
        }
    )

    OfflineSyncQueue.objects.get_or_create(
        idempotency_key="IDEM-DEMO-OFFLINE-01",
        defaults={
            'device_id': 'MOBILE_DEVICE_77',
            'event_type': 'OFFLINE_QR_SCAN',
            'payload_json': '{"product": "Terracotta Lamp", "scan_time": "2026-10-06T15:00:00Z"}',
            'status': 'SYNCED'
        }
    )

    # Mega Prompt #23: AI Edge Commerce, Smart Store, IoT & Physical Intelligence OS
    from artisan_api.models import PhysicalDevice, EdgeGateway, SensorInventorySignal
    from artisan_api.services.physical_intelligence_engine import PhysicalIntelligenceEngine

    gw, _ = EdgeGateway.objects.get_or_create(
        gateway_code="GW_JAIPUR_FLAGSHIP_01",
        defaults={
            'store': st1,
            'status': 'ONLINE',
            'local_queue_count': 0
        }
    )

    d1, _ = PhysicalDevice.objects.get_or_create(
        device_id="SCANNER_JAIPUR_01",
        defaults={
            'organization': user,
            'store': st1,
            'device_type': 'SCANNER',
            'manufacturer': 'Zebra Technologies',
            'model_name': 'DS2208 Handheld Scanner',
            'firmware_version': 'v2.4.1',
            'status': 'ONLINE',
            'trust_level': 'HIGH',
            'capabilities_json': '["scanner", "barcode_reader", "offline_queue"]'
        }
    )

    d2, _ = PhysicalDevice.objects.get_or_create(
        device_id="SHELF_SENSOR_ZONE_B",
        defaults={
            'organization': user,
            'store': st1,
            'device_type': 'SMART_SHELF',
            'manufacturer': 'Honeywell Industrial',
            'model_name': 'SS-4000 Smart Shelf Sensor',
            'firmware_version': 'v1.1.0',
            'status': 'ONLINE',
            'trust_level': 'MEDIUM',
            'capabilities_json': '["inventory_sensor", "weight_change", "shelf_activity"]'
        }
    )

    if product:
        SensorInventorySignal.objects.get_or_create(
            device=d2,
            product=product,
            defaults={
                'detected_quantity': 18,
                'previous_quantity': 20,
                'confidence_score': 0.88
            }
        )


    smart_store_demo_res = PhysicalIntelligenceEngine.run_flagship_smart_store_demo(user)
    print("Mega Prompt #23 AI Edge Commerce, Smart Store, IoT & Physical Intelligence OS Seed Complete!")

if __name__ == '__main__':
    seed()














