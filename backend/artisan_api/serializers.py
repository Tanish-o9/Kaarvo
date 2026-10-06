from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    ArtisanProfile, Product, ProductMedia, ProductFact, Variant, Inventory,
    Order, Conversation, Message, AgentRun, MarketplaceAccount,
    Organization, OrganizationMember, MarketplaceSyncLog, Payment, Shipment,
    Campaign, SyncQueue, AgentMemory, BusinessKnowledge, ProductPassport, LLMCostTracker,
    AgentIdentity, AgentSession, AgentAuditTrail, BusinessGoalPlan, FeatureFlag,
    AITask, ApprovalInboxItem, SmartSupportTicket, EventExhibitionMode,
    NetworkIdentity, ProductVersion, MarketExpansionExperiment, ThirdPartyAIAgent, DeadLetterQueueItem,
    AILearningStore, PromptVersion, AIPromptExperiment, ProductSearchGap
)

class UserSerializer(serializers.ModelSerializer):
    craft_type = serializers.CharField(source='artisan_profile.craft_type', read_only=True)
    region = serializers.CharField(source='artisan_profile.region', read_only=True)
    preferred_language = serializers.CharField(source='artisan_profile.preferred_language', read_only=True)
    organization_name = serializers.CharField(source='artisan_profile.organization.name', read_only=True, default='')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'craft_type', 'region', 'preferred_language', 'organization_name']

class ArtisanProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ArtisanProfile
        fields = '__all__'

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = '__all__'

class ProductFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFact
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class ProductPassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPassport
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    media = ProductMediaSerializer(many=True, read_only=True)
    facts = ProductFactSerializer(many=True, read_only=True)
    variants = VariantSerializer(many=True, read_only=True)
    inventory = InventorySerializer(read_only=True)
    passport = ProductPassportSerializer(read_only=True)
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    payment = PaymentSerializer(read_only=True)
    shipment = ShipmentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'

class AgentRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentRun
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    artisans_count = serializers.IntegerField(source='artisans.count', read_only=True)
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = OrganizationMember
        fields = '__all__'

class MarketplaceSyncLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceSyncLog
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class SyncQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncQueue
        fields = '__all__'

class AgentMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentMemory
        fields = '__all__'

class BusinessKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessKnowledge
        fields = '__all__'

class LLMCostTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMCostTracker
        fields = '__all__'

class AgentIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentIdentity
        fields = '__all__'

class AgentAuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentAuditTrail
        fields = '__all__'

class BusinessGoalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessGoalPlan
        fields = '__all__'

class FeatureFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureFlag
        fields = '__all__'

class AITaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AITask
        fields = '__all__'

class ApprovalInboxItemSerializer(serializers.ModelSerializer):
    task_detail = AITaskSerializer(source='task', read_only=True)

    class Meta:
        model = ApprovalInboxItem
        fields = '__all__'

class SmartSupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartSupportTicket
        fields = '__all__'

class EventExhibitionModeSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EventExhibitionMode
        fields = '__all__'

    def get_product_details(self, obj):
        return [{'id': str(p.id), 'title': p.title, 'price': float(p.price)} for p in obj.event_products.all()]


class NetworkIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkIdentity
        fields = '__all__'


class ProductVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = '__all__'


class MarketExpansionExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketExpansionExperiment
        fields = '__all__'


class ThirdPartyAIAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThirdPartyAIAgent
        fields = '__all__'


class DeadLetterQueueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadLetterQueueItem
        fields = '__all__'


class AILearningStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AILearningStore
        fields = '__all__'


class PromptVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptVersion
        fields = '__all__'


class AIPromptExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPromptExperiment
        fields = '__all__'


class ProductSearchGapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSearchGap
        fields = '__all__'


# --- PROMPT #7 SERIALIZERS ---
from .models import BusinessSignal, Opportunity, BusinessGoal, AIPlan, DecisionTrace, DailyAIBrief

class BusinessSignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessSignal
        fields = '__all__'

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = '__all__'

class BusinessGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessGoal
        fields = '__all__'

class AIPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPlan
        fields = '__all__'

class DecisionTraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionTrace
        fields = '__all__'

class DailyAIBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyAIBrief
        fields = '__all__'


# --- PROMPT #8 SERIALIZERS ---
from .models import (
    Supplier, RawMaterial, BillOfMaterials, ProcurementOrder,
    B2BBuyerProfile, RequestForQuote, B2BQuotation, SplitOrderAllocation, QualityControlCheckpoint
)

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class BillOfMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOfMaterials
        fields = '__all__'

class ProcurementOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcurementOrder
        fields = '__all__'

class B2BBuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BBuyerProfile
        fields = '__all__'

class RequestForQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestForQuote
        fields = '__all__'

class B2BQuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BQuotation
        fields = '__all__'

class SplitOrderAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SplitOrderAllocation
        fields = '__all__'

class QualityControlCheckpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityControlCheckpoint
        fields = '__all__'


# --- PROMPT #9 SERIALIZERS ---
from .models import (
    GlobalCommerceProfile, MarketProfile, TradeDocumentWorkspace, ComplianceKnowledgeRule, ExportReadinessScorecard
)

class GlobalCommerceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalCommerceProfile
        fields = '__all__'

class MarketProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketProfile
        fields = '__all__'

class TradeDocumentWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeDocumentWorkspace
        fields = '__all__'

class ComplianceKnowledgeRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceKnowledgeRule
        fields = '__all__'

class ExportReadinessScorecardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportReadinessScorecard
        fields = '__all__'


# --- PROMPT #10 SERIALIZERS ---
from .models import (
    AgentPurchasePolicy, AgentToolDefinition, AgentNegotiationSession, AgentAttributionLog
)

class AgentPurchasePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentPurchasePolicy
        fields = '__all__'

class AgentToolDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentToolDefinition
        fields = '__all__'

class AgentNegotiationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentNegotiationSession
        fields = '__all__'

class AgentAttributionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentAttributionLog
        fields = '__all__'


# --- PROMPT #11 SERIALIZERS ---
from .models import (
    SocialProfile, ContentAsset, ContentCampaign, ContentSchedule,
    CreatorProfile, CreatorCampaign, Referral, AffiliateCommission,
    Community, CommunityPost, LiveSession
)

class SocialProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = SocialProfile
        fields = '__all__'

class ContentAssetSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True, default='')

    class Meta:
        model = ContentAsset
        fields = '__all__'

class ContentCampaignSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    creator_name = serializers.CharField(source='creator.username', read_only=True, default='')

    class Meta:
        model = ContentCampaign
        fields = '__all__'

class ContentScheduleSerializer(serializers.ModelSerializer):
    asset_title = serializers.CharField(source='asset.title', read_only=True)

    class Meta:
        model = ContentSchedule
        fields = '__all__'

class CreatorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CreatorProfile
        fields = '__all__'

class CreatorCampaignSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    creator_name = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = CreatorCampaign
        fields = '__all__'

class ReferralSerializer(serializers.ModelSerializer):
    referrer_name = serializers.CharField(source='referrer.username', read_only=True)

    class Meta:
        model = Referral
        fields = '__all__'

class AffiliateCommissionSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = AffiliateCommission
        fields = '__all__'

class CommunitySerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Community
        fields = '__all__'

class CommunityPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = CommunityPost
        fields = '__all__'

class LiveSessionSerializer(serializers.ModelSerializer):
    host_name = serializers.CharField(source='host.username', read_only=True)

    class Meta:
        model = LiveSession
        fields = '__all__'


# --- PROMPT #12 SERIALIZERS ---
from .models import (
    LedgerEntry, Expense, Invoice, SettlementReconciliation,
    FinancialScenario, FinancialAnomaly, PlatformBillingMeter
)

class LedgerEntrySerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = LedgerEntry
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'

class SettlementReconciliationSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = SettlementReconciliation
        fields = '__all__'

class FinancialScenarioSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = FinancialScenario
        fields = '__all__'

class FinancialAnomalySerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = FinancialAnomaly
        fields = '__all__'

class PlatformBillingMeterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PlatformBillingMeter
        fields = '__all__'


# --- PROMPT #13 SERIALIZERS ---
from .models import DigitalEmployee, AITeam, AISOP, WorkforceTask, WorkforceIncident

class DigitalEmployeeSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = DigitalEmployee
        fields = '__all__'

class AITeamSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = AITeam
        fields = '__all__'

class AISOPSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = AISOP
        fields = '__all__'

class WorkforceTaskSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    assigned_employee_name = serializers.CharField(source='assigned_employee.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = WorkforceTask
        fields = '__all__'

class WorkforceIncidentSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = WorkforceIncident
        fields = '__all__'


# --- PROMPT #14 SERIALIZERS ---
from .models import (
    GovernancePolicy, ToolTrustRecord, ConsentRecord,
    SecurityEvent, ModelRegistry, GovernanceControl
)

class GovernancePolicySerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = GovernancePolicy
        fields = '__all__'

class ToolTrustRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolTrustRecord
        fields = '__all__'

class ConsentRecordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ConsentRecord
        fields = '__all__'

class SecurityEventSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = SecurityEvent
        fields = '__all__'

class ModelRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelRegistry
        fields = '__all__'

class GovernanceControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernanceControl
        fields = '__all__'


# --- PROMPT #15 SERIALIZERS ---
from .models import (
    KnowledgeSource, KnowledgeObject, KnowledgeGraphNode, KnowledgeGraphEdge,
    DecisionMemory, KnowledgeConflictRecord, KnowledgeGapRecord
)

class KnowledgeSourceSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = KnowledgeSource
        fields = '__all__'

class KnowledgeObjectSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True, default='')

    class Meta:
        model = KnowledgeObject
        fields = '__all__'

class KnowledgeGraphNodeSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = KnowledgeGraphNode
        fields = '__all__'

class KnowledgeGraphEdgeSerializer(serializers.ModelSerializer):
    source_node_name = serializers.CharField(source='source_node.name', read_only=True)
    target_node_name = serializers.CharField(source='target_node.name', read_only=True)

    class Meta:
        model = KnowledgeGraphEdge
        fields = '__all__'

class DecisionMemorySerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = DecisionMemory
        fields = '__all__'

class KnowledgeConflictRecordSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = KnowledgeConflictRecord
        fields = '__all__'

class KnowledgeGapRecordSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = KnowledgeGapRecord
        fields = '__all__'


# --- PROMPT #16 SERIALIZERS ---
from .models import (
    DigitalTwinSnapshot, BusinessScenario, SimulationResult,
    StrategyCouncilReview, ScenarioCalibration
)

class DigitalTwinSnapshotSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = DigitalTwinSnapshot
        fields = '__all__'

class BusinessScenarioSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    baseline_name = serializers.CharField(source='baseline_snapshot.snapshot_name', read_only=True, default='')

    class Meta:
        model = BusinessScenario
        fields = '__all__'

class SimulationResultSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    scenario_name = serializers.CharField(source='scenario.scenario_name', read_only=True)

    class Meta:
        model = SimulationResult
        fields = '__all__'

class StrategyCouncilReviewSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    scenario_name = serializers.CharField(source='scenario.scenario_name', read_only=True)

    class Meta:
        model = StrategyCouncilReview
        fields = '__all__'

class ScenarioCalibrationSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    scenario_name = serializers.CharField(source='scenario.scenario_name', read_only=True)

    class Meta:
        model = ScenarioCalibration
        fields = '__all__'


# --- PROMPT #18 AI CAUSAL INTELLIGENCE, EXPERIMENTATION & OUTCOME LEARNING OS SERIALIZERS ---
from .models import (
    CausalRelationship, BusinessHypothesis, CausalExperiment,
    ExperimentResult, OutcomeLearning, BusinessUnknown
)

class CausalRelationshipSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = CausalRelationship
        fields = '__all__'

class BusinessHypothesisSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = BusinessHypothesis
        fields = '__all__'

class CausalExperimentSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    hypothesis_title = serializers.CharField(source='hypothesis.title', read_only=True, default='')

    class Meta:
        model = CausalExperiment
        fields = '__all__'

class ExperimentResultSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    experiment_title = serializers.CharField(source='experiment.title', read_only=True)

    class Meta:
        model = ExperimentResult
        fields = '__all__'

class OutcomeLearningSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    experiment_title = serializers.CharField(source='experiment.title', read_only=True, default='')

    class Meta:
        model = OutcomeLearning
        fields = '__all__'

class BusinessUnknownSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = BusinessUnknown
        fields = '__all__'


# --- PROMPT #19 AI MARKET INTELLIGENCE, COMPETITIVE INTELLIGENCE & OPPORTUNITY DISCOVERY OS SERIALIZERS ---
from .models import (
    IntelligenceSource, CompetitorProfile, MarketTrend,
    MarketOpportunity, MarketThreat
)

class IntelligenceSourceSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = IntelligenceSource
        fields = '__all__'

class CompetitorProfileSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = CompetitorProfile
        fields = '__all__'

class MarketTrendSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = MarketTrend
        fields = '__all__'

class MarketOpportunitySerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = MarketOpportunity
        fields = '__all__'

class MarketThreatSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = MarketThreat
        fields = '__all__'


# --- PROMPT #20 SERIALIZERS ---
from .models import (
    NetworkEntityGraphNode, NetworkRelationshipEdge, NetworkSignalMessage,
    NetworkDemandPool, NetworkCapacityResource, NetworkEcosystemOpportunity, NetworkMultiPartyMatch
)

class NetworkEntityGraphNodeSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = NetworkEntityGraphNode
        fields = '__all__'

class NetworkRelationshipEdgeSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)
    source_name = serializers.CharField(source='source_node.entity_name', read_only=True)
    target_name = serializers.CharField(source='target_node.entity_name', read_only=True)

    class Meta:
        model = NetworkRelationshipEdge
        fields = '__all__'

class NetworkSignalMessageSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = NetworkSignalMessage
        fields = '__all__'

class NetworkDemandPoolSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = NetworkDemandPool
        fields = '__all__'

class NetworkCapacityResourceSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = NetworkCapacityResource
        fields = '__all__'

class NetworkEcosystemOpportunitySerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = NetworkEcosystemOpportunity
        fields = '__all__'

class NetworkMultiPartyMatchSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.username', read_only=True)

    class Meta:
        model = NetworkMultiPartyMatch
        fields = '__all__'


# --- PROMPT #21 SERIALIZERS ---
from .models import (
    CustomerPreferenceProfile, CustomerCommerceMemory, ShoppingSessionIntent,
    CustomerShortlist, CustomerConsentPreference
)

class CustomerPreferenceProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = CustomerPreferenceProfile
        fields = '__all__'

class CustomerCommerceMemorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = CustomerCommerceMemory
        fields = '__all__'

class ShoppingSessionIntentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = ShoppingSessionIntent
        fields = '__all__'

class CustomerShortlistSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='customer.username', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CustomerShortlist
        fields = '__all__'

class CustomerConsentPreferenceSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = CustomerConsentPreference
        fields = '__all__'


# --- MEGA PROMPT #22: AI OMNICHANNEL, PHYGITAL COMMERCE & PHYSICAL WORLD INTELLIGENCE OS SERIALIZERS ---
from .models import (
    Store, StoreInventory, OmnichannelSession, QRAsset,
    KioskSession, PickupReservation, ExhibitionEvent, OfflineSyncQueue
)

class StoreSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Store
        fields = '__all__'

class StoreInventorySerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = StoreInventory
        fields = '__all__'

class OmnichannelSessionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='customer.username', read_only=True)
    store_name = serializers.CharField(source='current_store.name', read_only=True, default='')

    class Meta:
        model = OmnichannelSession
        fields = '__all__'

class QRAssetSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True, default='')
    store_name = serializers.CharField(source='store.name', read_only=True, default='')

    class Meta:
        model = QRAsset
        fields = '__all__'

class KioskSessionSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    customer_name = serializers.CharField(source='active_customer.username', read_only=True, default='')

    class Meta:
        model = KioskSession
        fields = '__all__'

class PickupReservationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='customer.username', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = PickupReservation
        fields = '__all__'

class ExhibitionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExhibitionEvent
        fields = '__all__'

class OfflineSyncQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineSyncQueue
        fields = '__all__'


# --- MEGA PROMPT #23: AI EDGE COMMERCE, SMART STORE, IOT & PHYSICAL INTELLIGENCE OS SERIALIZERS ---
from .models import (
    PhysicalDevice, EdgeGateway, DeviceEventTelemetry, DeviceCommandLog,
    SensorInventorySignal, InventoryReconciliationReport, PhysicalStoreTask
)

class PhysicalDeviceSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    organization_name = serializers.CharField(source='organization.username', read_only=True)

    class Meta:
        model = PhysicalDevice
        fields = '__all__'
        read_only_fields = ['organization']


class EdgeGatewaySerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = EdgeGateway
        fields = '__all__'

class DeviceEventTelemetrySerializer(serializers.ModelSerializer):
    device_type = serializers.CharField(source='device.device_type', read_only=True)
    device_code = serializers.CharField(source='device.device_id', read_only=True)

    class Meta:
        model = DeviceEventTelemetry
        fields = '__all__'

class DeviceCommandLogSerializer(serializers.ModelSerializer):
    device_type = serializers.CharField(source='device.device_type', read_only=True)

    class Meta:
        model = DeviceCommandLog
        fields = '__all__'

class SensorInventorySignalSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = SensorInventorySignal
        fields = '__all__'

class InventoryReconciliationReportSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = InventoryReconciliationReport
        fields = '__all__'

class PhysicalStoreTaskSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    assigned_name = serializers.CharField(source='assigned_to.username', read_only=True, default='Unassigned')

    class Meta:
        model = PhysicalStoreTask
        fields = '__all__'


# --- MEGA PROMPT #24: SECURITY OS SERIALIZERS ---
from .models import (
    SecurityEvent, SecurityIncident, SecurityPolicyRule,
    ThreatIndicator, AgentSecurityProfile
)

class SecurityIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityIncident
        fields = '__all__'

class SecurityPolicyRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityPolicyRule
        fields = '__all__'

class ThreatIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatIndicator
        fields = '__all__'

class AgentSecurityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSecurityProfile
        fields = '__all__'


# --- MEGA PROMPT #25: RESILIENCE & SELF-HEALING OS SERIALIZERS ---
from .models import (
    ServiceHealthRecord, FailureEventRecord, OperationalIncident,
    RecoveryPlanRecord, CircuitBreakerRecord
)

class ServiceHealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceHealthRecord
        fields = '__all__'

class FailureEventRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailureEventRecord
        fields = '__all__'

class OperationalIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalIncident
        fields = '__all__'

class RecoveryPlanRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecoveryPlanRecord
        fields = '__all__'

class CircuitBreakerRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitBreakerRecord
        fields = '__all__'


# --- MEGA PROMPT #26: OBSERVABILITY & SRE OS SERIALIZERS ---
from .models import (
    TelemetryEventRecord, ServiceDefinitionRecord, SLORecord,
    AlertRecord, SRETraceRecord, RunbookRecord
)

class TelemetryEventRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryEventRecord
        fields = '__all__'

class ServiceDefinitionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDefinitionRecord
        fields = '__all__'

class SLORecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SLORecord
        fields = '__all__'

class AlertRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRecord
        fields = '__all__'

class SRETraceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRETraceRecord
        fields = '__all__'

class RunbookRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunbookRecord
        fields = '__all__'


# --- MEGA PROMPT #27: DEVSECOPS & SOFTWARE ENGINEERING OS SERIALIZERS ---
from .models import (
    CodeEntityRecord, RequirementRecord, EngineeringTaskRecord,
    CodeChangeRecord, CodeReviewRecord, TestCaseRecord,
    BuildArtifactRecord, ReleaseRecord, TechnicalDebtRecord, ADRRecord
)

class CodeEntityRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeEntityRecord
        fields = '__all__'

class RequirementRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementRecord
        fields = '__all__'

class EngineeringTaskRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineeringTaskRecord
        fields = '__all__'

class CodeChangeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeChangeRecord
        fields = '__all__'

class CodeReviewRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReviewRecord
        fields = '__all__'

class TestCaseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseRecord
        fields = '__all__'

class BuildArtifactRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildArtifactRecord
        fields = '__all__'

class ReleaseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseRecord
        fields = '__all__'

class TechnicalDebtRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalDebtRecord
        fields = '__all__'

class ADRRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADRRecord
        fields = '__all__'


# --- MEGA PROMPT #28: AI DATA ENGINEERING, DATAOPS & AUTONOMOUS DATA PLATFORM OS SERIALIZERS ---
from .models import (
    DataSourceRecord, IngestionJobRecord, SchemaRegistryRecord,
    DataContractRecord, DataQualityCheckRecord, DataLineageEdgeRecord,
    DataIncidentRecord, DataProductRecord
)

class DataSourceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSourceRecord
        fields = '__all__'

class IngestionJobRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngestionJobRecord
        fields = '__all__'

class SchemaRegistryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaRegistryRecord
        fields = '__all__'

class DataContractRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataContractRecord
        fields = '__all__'

class DataQualityCheckRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataQualityCheckRecord
        fields = '__all__'

class DataLineageEdgeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataLineageEdgeRecord
        fields = '__all__'

class DataIncidentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataIncidentRecord
        fields = '__all__'

class DataProductRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataProductRecord
        fields = '__all__'


# --- MEGA PROMPT #29: AI RESEARCH, WEB INTELLIGENCE & DEEP RESEARCH OS SERIALIZERS ---
from .models import (
    ResearchSourceRecord, ResearchQuestionRecord, ClaimRecord,
    EvidencePackRecord, ResearchReportRecord, ResearchWatchlistRecord
)

class ResearchSourceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchSourceRecord
        fields = '__all__'

class ResearchQuestionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchQuestionRecord
        fields = '__all__'

class ClaimRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimRecord
        fields = '__all__'

class EvidencePackRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidencePackRecord
        fields = '__all__'

class ResearchReportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchReportRecord
        fields = '__all__'

class ResearchWatchlistRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchWatchlistRecord
        fields = '__all__'


# --- MEGA PROMPT #30: AI PROCESS INTELLIGENCE, WORKFLOW MINING & AUTONOMOUS BUSINESS OPERATIONS OS SERIALIZERS ---
from .models import (
    BusinessProcessRecord, ProcessStepRecord, ProcessEventRecord,
    ProcessBottleneckRecord, WorkflowOptimizationProposalRecord, ProcessDecisionReceiptRecord
)

class BusinessProcessRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProcessRecord
        fields = '__all__'

class ProcessStepRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStepRecord
        fields = '__all__'

class ProcessEventRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessEventRecord
        fields = '__all__'

class ProcessBottleneckRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessBottleneckRecord
        fields = '__all__'

class WorkflowOptimizationProposalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowOptimizationProposalRecord
        fields = '__all__'

class ProcessDecisionReceiptRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessDecisionReceiptRecord
        fields = '__all__'

















