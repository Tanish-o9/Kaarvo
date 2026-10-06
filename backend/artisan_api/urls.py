from django.urls import path
from .views import (
    RegisterView, LoginView, ArtisanProfileView, ProductListCreateView,
    ProductDetailView, ProductMediaUploadView, ProductAnalyzeView,
    ProductPriceSuggestView, ProductApproveView, ProductPublishView,
    OrderListCreateView, OrderDetailPatchView, AssistantChatView, AnalyticsOverviewView,
    MarketplaceSyncView, PaymentCreateVerifyView, ShipmentCreateView,
    SocialGenerateView, MobileSyncQueueView, CampaignGenerateApproveView,
    AIBusinessCoachInsightsView, OrganizationListImportView, OrganizationBulkOnboardView,
    CopilotQueryView, CustomerSearchQueryView, CustomerVisualSearchView,
    ProductPassportView, ProductOptimizeView, LLMCostAnalyticsView,
    MachineReadableFeedView, AgentDiscoverView, AgenticCheckoutView,
    AutopilotGoalPlanView, AutopilotApprovePlanView, AgentAuditTrailView,
    DeveloperSandboxSimulateView,
    AITaskListView, ApprovalInboxListView, ApprovalInboxActionView,
    SmartSupportTicketListView, EventExhibitionModeListView, EventQuickCheckoutView,
    PlatformHealthView, NetworkIdentityListView, MultiCurrencyConvertView,
    ChannelProfitabilityView, UniversalSearchView, ThirdPartyAIAgentListView,
    DeadLetterQueueView, AILearningStoreListView, ScenarioSimulationView,
    AgentConflictResolveView, ToolGatewayExecuteView, ProductSearchGapListView,
    PromptExperimentListView,
    BusinessSignalListView, OpportunityListView, DecisionEvaluateView, ScenarioLabView,
    BusinessGoalListView, ActionFirewallView, BusinessHealthView, DailyBriefView,
    SupplierListView, ProcurementRequirementsView, ProcurementOrderCreateView,
    B2BRFQCreateMatchView, SplitOrderAllocateView, SupplyChainRiskView,
    GlobalCommerceProfileView, MarketProfileListView, ProductLocalizeView,
    ExportReadinessEvaluateView, LandedCostCalculateView, ComplianceRAGQueryView,
    TradeDocumentValidateView, GlobalTradeWorkflowView,
    AgentAuthorizeActionView, AgentProductSearchView, AgentCartCreateView,
    AgentToAgentNegotiateView, AgentToolRegistryListView,
    B2CShoppingAgentDemoView, B2BAgentNegotiationDemoView,
    SocialProfileView, ContentStudioView, ContentCampaignView, CreatorMarketplaceView,
    CreatorCampaignView, ReferralAffiliateView, CommunityView, GrowthCoachView,
    FlagshipSocialGrowthDemoView,
    UnifiedLedgerView, RevenueCostAnalyticsView, UnitEconomicsView, ExpenseManagementView,
    SettlementReconciliationView, FinancialScenarioLabView, FinancialAnomalyView,
    PlatformBillingMeterView, FlagshipFinanceDemoView,
    DigitalEmployeeListView, DigitalEmployeeDetailView, DigitalEmployeeCertifyView,
    WorkforceTaskListView, WorkforceTaskDetailView, AITeamListView, SOPLibraryView,
    WorkforceCommandBarView, WorkforceHealthView, FlagshipWorkforceDemoView,
    GovernancePolicyListView, PolicySimulateView, SecurityEventListView, ToolTrustListView,
    ConsentRecordListView, PrivacyCenterView, ModelRegistryView, GovernanceRedTeamView,
    PlatformSafeModeView, GovernanceHealthView, FlagshipTrustDemoView,
    KnowledgeSourceViewSet, KnowledgeObjectViewSet, KnowledgeGraphNodeViewSet, KnowledgeGraphEdgeViewSet,
    DecisionMemoryViewSet, KnowledgeConflictViewSet, KnowledgeGapViewSet,
    OrganizationalBrainQueryView, KnowledgeHealthView, KnowledgeGraphExplorerView,
    DigitalTwinStateView, DigitalTwinSnapshotViewSet, BusinessScenarioViewSet,
    RunSimulationView, CompareScenariosView, StrategyAnalyzeView, StressTestView,
    CalibrationHistoryView, FlagshipStrategyLabDemoView,
    CausalGraphOverviewView, BusinessHypothesisViewSet, CausalExperimentViewSet,
    ProposeExperimentView, AnalyzeExperimentView, RootCauseInvestigateView,
    OutcomeLearningViewSet, BusinessUnknownViewSet, FlagshipCausalDemoView,
    MarketOverviewView, IntelligenceSourceViewSet, CompetitorProfileViewSet,
    MarketTrendViewSet, MarketOpportunityViewSet, MarketThreatViewSet,
    CompetitorMovesAnalysisView, DailyMarketBriefView, FlagshipMarketDemoView,
    NetworkOverviewView, NetworkGraphView, NetworkDemandPoolsView,
    NetworkCapacitiesView, NetworkOpportunitiesView, NetworkMatchesView,
    DailyNetworkBriefView, FlagshipNetworkDemoView,
    CustomerProfile360View, CustomerIntentParseView, CustomerRecommendationsView,
    CustomerShortlistsView, CustomerGiftBundlesView, CustomerCartCopilotView,
    CustomerMemoryViewSet, DailyCustomerBriefView, FlagshipCustomerDemoView,
    StoreListView, StoreInventoryListView, QRResolveView, StoreStockCheckView,
    ClickCollectReserveView, KioskSessionTransferView, StaffCopilotView,
    SmartOrderRoutingView, OfflineSyncQueueView, DailyOmnichannelBriefView, FlagshipPhygitalDemoView,
    PhysicalDeviceListView, DeviceHealthOverviewView, DeviceTelemetryIngestView,
    DeviceCommandExecuteView, DeviceSimulatorTriggerView, InventoryReconciliationView,
    DailyPhysicalBriefView, FlagshipSmartStoreDemoView,
    SecurityIncidentListView, SecurityActionFirewallEvaluateView,
    PromptInjectionDefenseView, FraudIntelligenceAuditView, SecurityIdentityGraphView,
    DailySecurityBriefView, FlagshipSecurityDemoView,
    ResilienceHealthMatrixView, ResilienceFailureIngestView, OperationalIncidentListView,
    RecoveryFirewallEvaluateView, CircuitBreakerManageView, DailyResilienceBriefView,
    FlagshipCascadingFailureDemoView,
    TelemetryGoldenSignalsView, ServiceCatalogDependencyView, SLOErrorBudgetView,
    LLMOpsAgentObservabilityView, OperationsActionFirewallView, AIRootCauseAnalystView,
    SRECopilotQueryView, DailySREBriefView, FlagshipDiwaliSurgeDemoView, FlagshipCostSpikeDemoView,
    CodebaseKnowledgeGraphView, RequirementParseView, AIBugInvestigatorView,
    CodeGenerateReviewView, DevSecOpsActionFirewallView, CICDPipelineRunView,
    DailyDevSecOpsBriefView, FlagshipBugFixDemoView, FlagshipArchDebtDemoView,
    DataPlatformOverviewView, DataIngestionView, SchemaDriftDetectionView,
    DataQualityEvaluationView, DataLineageGraphView, DataRouterQueryView,
    DataAutonomyFirewallView, DailyDataBriefView, FlagshipInventoryContradictionDemoView,
    DeepResearchOverviewView, DeepResearchPlanView, ClaimVerifyView,
    ContradictionAnalysisView, EvidencePackView, ResearchFirewallView,
    DailyResearchBriefView, FlagshipDeepResearchDemoView,
    ProcessPlatformOverviewView, ProcessMiningView, ProcessBottleneckDetectionView,
    WorkflowOptimizationSimulationView, ProcessFirewallView, DailyProcessBriefView,
    FlagshipB2BProcessDemoView, MasterSystemAuditView, MasterSystemLoopRunView
)





urlpatterns = [
    # Mega Prompt #21: AI Customer 360, Personal Commerce & Adaptive Shopping OS
    path('customer/360/profile', CustomerProfile360View.as_view(), name='customer-360-profile'),
    path('customer/360/intent/parse', CustomerIntentParseView.as_view(), name='customer-360-intent-parse'),
    path('customer/360/recommendations', CustomerRecommendationsView.as_view(), name='customer-360-recommendations'),
    path('customer/360/shortlists', CustomerShortlistsView.as_view(), name='customer-360-shortlists'),
    path('customer/360/gift-bundles', CustomerGiftBundlesView.as_view(), name='customer-360-gift-bundles'),
    path('customer/360/cart-copilot', CustomerCartCopilotView.as_view(), name='customer-360-cart-copilot'),
    path('customer/360/memory', CustomerMemoryViewSet.as_view(), name='customer-360-memory'),
    path('customer/360/brief', DailyCustomerBriefView.as_view(), name='customer-360-brief'),
    path('customer/360/flagship-demo', FlagshipCustomerDemoView.as_view(), name='customer-360-flagship-demo'),

    # Mega Prompt #20: AI Network Intelligence, Collective Commerce Graph & Ecosystem OS
    path('network-intelligence/overview', NetworkOverviewView.as_view(), name='network-intel-overview'),
    path('network-intelligence/graph', NetworkGraphView.as_view(), name='network-intel-graph'),
    path('network-intelligence/demand-pools', NetworkDemandPoolsView.as_view(), name='network-intel-demand-pools'),
    path('network-intelligence/capacities', NetworkCapacitiesView.as_view(), name='network-intel-capacities'),
    path('network-intelligence/opportunities', NetworkOpportunitiesView.as_view(), name='network-intel-opportunities'),
    path('network-intelligence/matches', NetworkMatchesView.as_view(), name='network-intel-matches'),
    path('network-intelligence/brief', DailyNetworkBriefView.as_view(), name='network-intel-brief'),
    path('network-intelligence/flagship-demo', FlagshipNetworkDemoView.as_view(), name='network-intel-flagship-demo'),

    # Mega Prompt #19: AI Market Intelligence, Competitive Intelligence & Opportunity Discovery OS
    path('market/overview', MarketOverviewView.as_view(), name='market-overview'),
    path('market/sources', IntelligenceSourceViewSet.as_view({'get': 'list', 'post': 'create'}), name='market-sources'),
    path('market/competitors', CompetitorProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='market-competitors'),
    path('market/trends', MarketTrendViewSet.as_view({'get': 'list', 'post': 'create'}), name='market-trends'),
    path('market/opportunities', MarketOpportunityViewSet.as_view({'get': 'list', 'post': 'create'}), name='market-opportunities'),
    path('market/threats', MarketThreatViewSet.as_view({'get': 'list', 'post': 'create'}), name='market-threats'),
    path('market/competitors/analysis', CompetitorMovesAnalysisView.as_view(), name='market-competitors-analysis'),
    path('market/brief', DailyMarketBriefView.as_view(), name='market-brief'),
    path('market/flagship-demo', FlagshipMarketDemoView.as_view(), name='market-flagship-demo'),
    # Mega Prompt #18: AI Causal Intelligence, Experimentation & Outcome Learning OS
    path('causal/graph', CausalGraphOverviewView.as_view(), name='causal-graph'),
    path('causal/hypotheses', BusinessHypothesisViewSet.as_view({'get': 'list', 'post': 'create'}), name='causal-hypotheses'),
    path('causal/experiments', CausalExperimentViewSet.as_view({'get': 'list', 'post': 'create'}), name='causal-experiments'),
    path('causal/experiments/propose', ProposeExperimentView.as_view(), name='causal-experiments-propose'),
    path('causal/experiments/analyze', AnalyzeExperimentView.as_view(), name='causal-experiments-analyze'),
    path('causal/root-cause', RootCauseInvestigateView.as_view(), name='causal-root-cause'),
    path('causal/learnings', OutcomeLearningViewSet.as_view({'get': 'list'}), name='causal-learnings'),
    path('causal/unknowns', BusinessUnknownViewSet.as_view({'get': 'list'}), name='causal-unknowns'),
    path('causal/flagship-demo', FlagshipCausalDemoView.as_view(), name='causal-flagship-demo'),

    # Mega Prompt #16: AI Digital Twin, Business Simulation & Strategy Lab
    # Mega Prompt #16: AI Digital Twin, Business Simulation & Strategy Lab
    path('twin/state', DigitalTwinStateView.as_view(), name='twin-state'),
    path('twin/snapshots', DigitalTwinSnapshotViewSet.as_view({'get': 'list', 'post': 'create'}), name='twin-snapshots'),
    path('twin/scenarios', BusinessScenarioViewSet.as_view({'get': 'list', 'post': 'create'}), name='twin-scenarios'),
    path('twin/scenarios/run', RunSimulationView.as_view(), name='twin-scenarios-run'),
    path('twin/scenarios/compare', CompareScenariosView.as_view(), name='twin-scenarios-compare'),
    path('twin/strategy/analyze', StrategyAnalyzeView.as_view(), name='twin-strategy-analyze'),
    path('twin/strategy/stress-test', StressTestView.as_view(), name='twin-strategy-stress-test'),
    path('twin/calibration', CalibrationHistoryView.as_view(), name='twin-calibration'),
    path('twin/flagship-demo', FlagshipStrategyLabDemoView.as_view(), name='twin-flagship-demo'),

    # Mega Prompt #15: AI Knowledge Fabric, Organizational Brain & Enterprise Memory OS

    path('knowledge/sources', KnowledgeSourceViewSet.as_view({'get': 'list', 'post': 'create'}), name='knowledge-sources'),
    path('knowledge/objects', KnowledgeObjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='knowledge-objects'),
    path('knowledge/graph-nodes', KnowledgeGraphNodeViewSet.as_view({'get': 'list', 'post': 'create'}), name='knowledge-graph-nodes'),
    path('knowledge/graph-edges', KnowledgeGraphEdgeViewSet.as_view({'get': 'list', 'post': 'create'}), name='knowledge-graph-edges'),
    path('knowledge/decisions', DecisionMemoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='knowledge-decisions'),
    path('knowledge/conflicts', KnowledgeConflictViewSet.as_view({'get': 'list', 'post': 'create'}), name='knowledge-conflicts'),
    path('knowledge/gaps', KnowledgeGapViewSet.as_view({'get': 'list', 'post': 'create'}), name='knowledge-gaps'),
    path('knowledge/brain-query', OrganizationalBrainQueryView.as_view(), name='knowledge-brain-query'),
    path('knowledge/health', KnowledgeHealthView.as_view(), name='knowledge-health'),
    path('knowledge/graph-explorer', KnowledgeGraphExplorerView.as_view(), name='knowledge-graph-explorer'),

    # Mega Prompt #14: AI Trust, Governance, Privacy, Security & Compliance OS

    path('governance/policies', GovernancePolicyListView.as_view(), name='governance-policies'),
    path('governance/policy-simulate', PolicySimulateView.as_view(), name='governance-policy-simulate'),
    path('governance/security-events', SecurityEventListView.as_view(), name='governance-security-events'),
    path('governance/tools', ToolTrustListView.as_view(), name='governance-tools'),
    path('governance/consents', ConsentRecordListView.as_view(), name='governance-consents'),
    path('governance/privacy', PrivacyCenterView.as_view(), name='governance-privacy'),
    path('governance/models', ModelRegistryView.as_view(), name='governance-models'),
    path('governance/red-team', GovernanceRedTeamView.as_view(), name='governance-red-team'),
    path('governance/safe-mode', PlatformSafeModeView.as_view(), name='governance-safe-mode'),
    path('governance/health', GovernanceHealthView.as_view(), name='governance-health'),
    path('governance/flagship-demo', FlagshipTrustDemoView.as_view(), name='governance-flagship-demo'),

    # Mega Prompt #13: AI Workforce OS & Digital Employees
    path('workforce/employees', DigitalEmployeeListView.as_view(), name='workforce-employees'),
    path('workforce/employees/<uuid:pk>', DigitalEmployeeDetailView.as_view(), name='workforce-employee-detail'),
    path('workforce/employees/<uuid:pk>/certify', DigitalEmployeeCertifyView.as_view(), name='workforce-employee-certify'),
    path('workforce/tasks', WorkforceTaskListView.as_view(), name='workforce-tasks'),
    path('workforce/tasks/<uuid:pk>', WorkforceTaskDetailView.as_view(), name='workforce-task-detail'),
    path('workforce/teams', AITeamListView.as_view(), name='workforce-teams'),
    path('workforce/sops', SOPLibraryView.as_view(), name='workforce-sops'),
    path('workforce/command-bar', WorkforceCommandBarView.as_view(), name='workforce-command-bar'),
    path('workforce/health', WorkforceHealthView.as_view(), name='workforce-health'),
    path('workforce/flagship-demo', FlagshipWorkforceDemoView.as_view(), name='workforce-flagship-demo'),

    # Mega Prompt #12: AI Finance, Operations & Business Intelligence OS
    path('finance/ledger', UnifiedLedgerView.as_view(), name='finance-ledger'),
    path('finance/analytics', RevenueCostAnalyticsView.as_view(), name='finance-analytics'),
    path('finance/unit-economics', UnitEconomicsView.as_view(), name='finance-unit-economics'),
    path('finance/expenses', ExpenseManagementView.as_view(), name='finance-expenses'),
    path('finance/reconciliation', SettlementReconciliationView.as_view(), name='finance-reconciliation'),
    path('finance/scenario-lab', FinancialScenarioLabView.as_view(), name='finance-scenario-lab'),
    path('finance/anomalies', FinancialAnomalyView.as_view(), name='finance-anomalies'),
    path('finance/billing-meter', PlatformBillingMeterView.as_view(), name='finance-billing-meter'),
    path('finance/flagship-demo', FlagshipFinanceDemoView.as_view(), name='finance-flagship-demo'),

    # Mega Prompt #11: AI Social Commerce, Creator Economy & Autonomous Growth Network
    path('social/profiles', SocialProfileView.as_view(), name='social-profiles'),
    path('social/content-studio', ContentStudioView.as_view(), name='social-content-studio'),
    path('social/campaigns', ContentCampaignView.as_view(), name='social-campaigns'),
    path('creators/marketplace', CreatorMarketplaceView.as_view(), name='creators-marketplace'),
    path('creators/campaigns', CreatorCampaignView.as_view(), name='creators-campaigns'),
    path('social/referrals-affiliate', ReferralAffiliateView.as_view(), name='social-referrals-affiliate'),
    path('social/community', CommunityView.as_view(), name='social-community'),
    path('growth/coach', GrowthCoachView.as_view(), name='growth-coach'),
    path('growth/flagship-demo', FlagshipSocialGrowthDemoView.as_view(), name='growth-flagship-demo'),


    # Mega Prompt #10: AI Agent Marketplace, Agent-to-Agent Commerce & Developer Ecosystem
    path('agent-network/authorize', AgentAuthorizeActionView.as_view(), name='agent-network-authorize'),
    path('agent-network/products/search', AgentProductSearchView.as_view(), name='agent-network-product-search'),
    path('agent-network/cart/create', AgentCartCreateView.as_view(), name='agent-network-cart-create'),
    path('agent-network/negotiate', AgentToAgentNegotiateView.as_view(), name='agent-network-negotiate'),
    path('agent-network/tools', AgentToolRegistryListView.as_view(), name='agent-network-tools'),
    path('agent-network/demo/b2c-shopping', B2CShoppingAgentDemoView.as_view(), name='agent-network-demo-b2c'),
    path('agent-network/demo/b2b-negotiation', B2BAgentNegotiationDemoView.as_view(), name='agent-network-demo-b2b'),


    # Mega Prompt #9: Global Commerce, Export & AI Trade Network
    path('global/profile', GlobalCommerceProfileView.as_view(), name='global-profile'),
    path('global/markets', MarketProfileListView.as_view(), name='global-markets'),
    path('global/products/localize', ProductLocalizeView.as_view(), name='global-product-localize'),
    path('global/export-readiness', ExportReadinessEvaluateView.as_view(), name='global-export-readiness'),
    path('global/landed-cost', LandedCostCalculateView.as_view(), name='global-landed-cost'),
    path('global/compliance-rag', ComplianceRAGQueryView.as_view(), name='global-compliance-rag'),
    path('global/documents/validate', TradeDocumentValidateView.as_view(), name='global-documents-validate'),
    path('global/trade-workflow', GlobalTradeWorkflowView.as_view(), name='global-trade-workflow'),


    # Auth & Profile

    # Auth & Profile
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('artisan/profile', ArtisanProfileView.as_view(), name='artisan-profile'),
    
    # Products & AI Pipeline
    path('products', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<uuid:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('products/<uuid:pk>/media', ProductMediaUploadView.as_view(), name='product-media-upload'),
    path('products/<uuid:pk>/analyze', ProductAnalyzeView.as_view(), name='product-analyze'),
    path('products/<uuid:pk>/price-suggest', ProductPriceSuggestView.as_view(), name='product-price-suggest'),
    path('products/<uuid:pk>/approve', ProductApproveView.as_view(), name='product-approve'),
    path('products/<uuid:pk>/publish', ProductPublishView.as_view(), name='product-publish'),

    # Mega Prompt #8: Supply Chain, B2B Commerce & Artisan Super App
    path('supply-chain/suppliers', SupplierListView.as_view(), name='supply-chain-suppliers'),
    path('procurement/calculate-requirements', ProcurementRequirementsView.as_view(), name='procurement-requirements'),
    path('procurement/orders/create', ProcurementOrderCreateView.as_view(), name='procurement-order-create'),
    path('b2b/rfq', B2BRFQCreateMatchView.as_view(), name='b2b-rfq-list-create'),
    path('b2b/order-allocation', SplitOrderAllocateView.as_view(), name='b2b-order-allocation'),
    path('supply-chain/risk', SupplyChainRiskView.as_view(), name='supply-chain-risk'),

    # Mega Prompt #7: Commerce Intelligence & Autonomous Decision Infrastructure
    path('intelligence/signals', BusinessSignalListView.as_view(), name='intelligence-signals'),
    path('intelligence/opportunities', OpportunityListView.as_view(), name='intelligence-opportunities'),
    path('intelligence/decisions/evaluate', DecisionEvaluateView.as_view(), name='intelligence-decisions-evaluate'),
    path('intelligence/scenario-lab', ScenarioLabView.as_view(), name='intelligence-scenario-lab'),
    path('intelligence/goals', BusinessGoalListView.as_view(), name='intelligence-goals'),
    path('security/firewall/execute', ActionFirewallView.as_view(), name='firewall-execute'),
    path('intelligence/health-score', BusinessHealthView.as_view(), name='intelligence-health-score'),
    path('intelligence/daily-brief', DailyBriefView.as_view(), name='intelligence-daily-brief'),


    # Mega Prompt #6: Autonomous Intelligence & Self-Improving AI
    path('intelligence/learning', AILearningStoreListView.as_view(), name='ai-learning-store'),

    path('intelligence/simulate', ScenarioSimulationView.as_view(), name='scenario-simulation'),
    path('intelligence/agent-conflict', AgentConflictResolveView.as_view(), name='agent-conflict-resolve'),
    path('security/tool-gateway', ToolGatewayExecuteView.as_view(), name='tool-gateway-execute'),
    path('intelligence/search-gaps', ProductSearchGapListView.as_view(), name='product-search-gaps'),
    path('intelligence/prompt-experiments', PromptExperimentListView.as_view(), name='prompt-experiments'),

    # Mega Prompt #5: AI-Native Commerce Network & Autonomous Merchant Operations
    path('network/identity', NetworkIdentityListView.as_view(), name='network-identity-list'),
    path('network/currency/convert', MultiCurrencyConvertView.as_view(), name='network-currency-convert'),
    path('merchant/profitability', ChannelProfitabilityView.as_view(), name='merchant-profitability'),
    path('network/search', UniversalSearchView.as_view(), name='universal-search'),
    path('agent-marketplace', ThirdPartyAIAgentListView.as_view(), name='agent-marketplace'),
    path('admin/dlq', DeadLetterQueueView.as_view(), name='admin-dlq-list'),
    path('admin/dlq/<uuid:pk>/replay', DeadLetterQueueView.as_view(), name='admin-dlq-replay'),

    # Mega Prompt #4: AI Organization, Approval Inbox, Support Tickets, Event Mode, Platform Health
    path('ai-tasks', AITaskListView.as_view(), name='ai-tasks-list-create'),
    path('approval-inbox', ApprovalInboxListView.as_view(), name='approval-inbox-list'),
    path('approval-inbox/<uuid:pk>/<str:action>', ApprovalInboxActionView.as_view(), name='approval-inbox-action'),
    path('support-tickets', SmartSupportTicketListView.as_view(), name='smart-support-tickets'),
    path('event-mode', EventExhibitionModeListView.as_view(), name='event-mode-list'),
    path('event-mode/<uuid:pk>/quick-checkout', EventQuickCheckoutView.as_view(), name='event-mode-quick-checkout'),
    path('admin/platform-health', PlatformHealthView.as_view(), name='platform-health'),

    # Prompt #3: Agentic Commerce Infrastructure & Machine-Readable Feed
    path('agent/products/feed', MachineReadableFeedView.as_view(), name='agent-products-feed'),
    path('agent/discover', AgentDiscoverView.as_view(), name='agent-discover'),
    path('agent/checkout', AgenticCheckoutView.as_view(), name='agent-checkout'),
    path('autopilot/goal-plan', AutopilotGoalPlanView.as_view(), name='autopilot-goal-plan'),
    path('autopilot/goal-plan/<uuid:pk>/approve', AutopilotApprovePlanView.as_view(), name='autopilot-approve-plan'),
    path('admin/agent-audit-trail', AgentAuditTrailView.as_view(), name='admin-agent-audit-trail'),
    path('developer/sandbox/simulate-checkout', DeveloperSandboxSimulateView.as_view(), name='developer-sandbox-simulate'),
    
    # Phase 5+: Copilot, Customer Search & Digital Product Passport
    path('copilot/query', CopilotQueryView.as_view(), name='copilot-query'),
    path('customer/search', CustomerSearchQueryView.as_view(), name='customer-search'),
    path('customer/visual-search', CustomerVisualSearchView.as_view(), name='customer-visual-search'),
    path('products/<uuid:pk>/passport', ProductPassportView.as_view(), name='product-passport'),
    path('products/<uuid:pk>/optimize', ProductOptimizeView.as_view(), name='product-optimize'),
    path('admin/llm-costs', LLMCostAnalyticsView.as_view(), name='admin-llm-costs'),

    # Phase 2, 3, 4: Marketplaces, Payments, Logistics, Social, Campaigns, NGO
    path('marketplaces/<uuid:pk>/sync', MarketplaceSyncView.as_view(), name='marketplace-sync'),
    path('payments/create', PaymentCreateVerifyView.as_view(), name='payment-create'),
    path('shipments/create', ShipmentCreateView.as_view(), name='shipment-create'),
    path('social/<uuid:pk>/generate', SocialGenerateView.as_view(), name='social-generate'),
    path('mobile/sync-queue', MobileSyncQueueView.as_view(), name='mobile-sync-queue'),
    path('campaigns/generate', CampaignGenerateApproveView.as_view(), name='campaign-generate'),
    path('business-coach/insights', AIBusinessCoachInsightsView.as_view(), name='business-coach-insights'),
    path('organizations', OrganizationListImportView.as_view(), name='organization-list'),
    path('organizations/<uuid:pk>/artisans/import', OrganizationBulkOnboardView.as_view(), name='organization-import'),
    
    # Orders, Assistant & Analytics
    path('orders', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<uuid:pk>', OrderDetailPatchView.as_view(), name='order-detail-patch'),
    path('assistant/chat', AssistantChatView.as_view(), name='assistant-chat'),
    path('analytics/overview', AnalyticsOverviewView.as_view(), name='analytics-overview'),

    # Mega Prompt #22: AI Omnichannel, Phygital Commerce & Physical World OS
    path('stores', StoreListView.as_view(), name='store-list'),
    path('stores/inventory', StoreInventoryListView.as_view(), name='store-inventory-list'),
    path('qr/resolve', QRResolveView.as_view(), name='qr-resolve'),
    path('stores/stock-check', StoreStockCheckView.as_view(), name='store-stock-check'),
    path('pickup/reserve', ClickCollectReserveView.as_view(), name='pickup-reserve'),
    path('kiosk/transfer', KioskSessionTransferView.as_view(), name='kiosk-transfer'),
    path('stores/staff-copilot', StaffCopilotView.as_view(), name='staff-copilot'),
    path('omnichannel/route-order', SmartOrderRoutingView.as_view(), name='omnichannel-route-order'),
    path('omnichannel/offline-sync', OfflineSyncQueueView.as_view(), name='omnichannel-offline-sync'),
    path('omnichannel/daily-brief', DailyOmnichannelBriefView.as_view(), name='omnichannel-daily-brief'),
    path('omnichannel/flagship-demo', FlagshipPhygitalDemoView.as_view(), name='omnichannel-flagship-demo'),

    # Mega Prompt #23: AI Edge Commerce, Smart Store, IoT & Physical Intelligence OS
    path('devices', PhysicalDeviceListView.as_view(), name='device-list'),
    path('devices/health', DeviceHealthOverviewView.as_view(), name='device-health'),
    path('devices/telemetry', DeviceTelemetryIngestView.as_view(), name='device-telemetry'),
    path('devices/commands', DeviceCommandExecuteView.as_view(), name='device-command'),
    path('devices/simulator', DeviceSimulatorTriggerView.as_view(), name='device-simulator'),
    path('inventory/reconcile', InventoryReconciliationView.as_view(), name='inventory-reconcile'),
    path('physical/daily-brief', DailyPhysicalBriefView.as_view(), name='physical-daily-brief'),
    path('physical/flagship-demo', FlagshipSmartStoreDemoView.as_view(), name='physical-flagship-demo'),

    # Mega Prompt #24: AI Security + Cyber Defense + Fraud/Risk Intelligence OS
    path('security/events', SecurityEventListView.as_view(), name='security-events'),
    path('security/incidents', SecurityIncidentListView.as_view(), name='security-incidents'),
    path('security/firewall/evaluate', SecurityActionFirewallEvaluateView.as_view(), name='security-firewall-evaluate'),
    path('security/prompt-defense', PromptInjectionDefenseView.as_view(), name='security-prompt-defense'),
    path('security/fraud-audit', FraudIntelligenceAuditView.as_view(), name='security-fraud-audit'),
    path('security/graph', SecurityIdentityGraphView.as_view(), name='security-graph'),
    path('security/daily-brief', DailySecurityBriefView.as_view(), name='security-daily-brief'),
    path('security/flagship-demo', FlagshipSecurityDemoView.as_view(), name='security-flagship-demo'),

    # Mega Prompt #25: AI Resilience + Disaster Recovery + Self-Healing Commerce OS
    path('resilience/health', ResilienceHealthMatrixView.as_view(), name='resilience-health'),
    path('resilience/services', ResilienceFailureIngestView.as_view(), name='resilience-services'),
    path('resilience/incidents', OperationalIncidentListView.as_view(), name='resilience-incidents'),
    path('resilience/firewall/evaluate-recovery', RecoveryFirewallEvaluateView.as_view(), name='resilience-firewall-evaluate'),
    path('resilience/circuit-breakers', CircuitBreakerManageView.as_view(), name='resilience-circuit-breakers'),
    path('resilience/daily-brief', DailyResilienceBriefView.as_view(), name='resilience-daily-brief'),
    path('resilience/flagship-demo', FlagshipCascadingFailureDemoView.as_view(), name='resilience-flagship-demo'),

    # Mega Prompt #26: AI Observability + SRE + Autonomous Operations OS
    path('observability/telemetry', TelemetryGoldenSignalsView.as_view(), name='observability-telemetry'),
    path('observability/services', ServiceCatalogDependencyView.as_view(), name='observability-services'),
    path('observability/slos', SLOErrorBudgetView.as_view(), name='observability-slos'),
    path('observability/llmops', LLMOpsAgentObservabilityView.as_view(), name='observability-llmops'),
    path('observability/firewall/evaluate', OperationsActionFirewallView.as_view(), name='observability-firewall-evaluate'),
    path('observability/root-cause', AIRootCauseAnalystView.as_view(), name='observability-root-cause'),
    path('observability/copilot', SRECopilotQueryView.as_view(), name='observability-copilot'),
    path('observability/daily-brief', DailySREBriefView.as_view(), name='observability-daily-brief'),
    path('observability/flagship-diwali-demo', FlagshipDiwaliSurgeDemoView.as_view(), name='observability-flagship-diwali-demo'),
    path('observability/flagship-cost-demo', FlagshipCostSpikeDemoView.as_view(), name='observability-flagship-cost-demo'),

    # Mega Prompt #27: AI Software Engineering + Autonomous DevSecOps OS
    path('devsecops/graph', CodebaseKnowledgeGraphView.as_view(), name='devsecops-graph'),
    path('devsecops/requirement/parse', RequirementParseView.as_view(), name='devsecops-requirement-parse'),
    path('devsecops/bug-investigate', AIBugInvestigatorView.as_view(), name='devsecops-bug-investigate'),
    path('devsecops/code/generate-review', CodeGenerateReviewView.as_view(), name='devsecops-code-generate-review'),
    path('devsecops/firewall/evaluate', DevSecOpsActionFirewallView.as_view(), name='devsecops-firewall-evaluate'),
    path('devsecops/cicd/run', CICDPipelineRunView.as_view(), name='devsecops-cicd-run'),
    path('devsecops/daily-brief', DailyDevSecOpsBriefView.as_view(), name='devsecops-daily-brief'),
    path('devsecops/flagship-bug-demo', FlagshipBugFixDemoView.as_view(), name='devsecops-flagship-bug-demo'),
    path('devsecops/flagship-arch-demo', FlagshipArchDebtDemoView.as_view(), name='devsecops-flagship-arch-demo'),

    # Mega Prompt #28: AI Data Engineering, DataOps & Autonomous Data Platform OS
    path('data/overview', DataPlatformOverviewView.as_view(), name='data-overview'),
    path('data/ingest', DataIngestionView.as_view(), name='data-ingest'),
    path('data/schema-drift', SchemaDriftDetectionView.as_view(), name='data-schema-drift'),
    path('data/quality', DataQualityEvaluationView.as_view(), name='data-quality'),
    path('data/lineage', DataLineageGraphView.as_view(), name='data-lineage'),
    path('data/router/query', DataRouterQueryView.as_view(), name='data-router-query'),
    path('data/firewall/evaluate', DataAutonomyFirewallView.as_view(), name='data-firewall-evaluate'),
    path('data/daily-brief', DailyDataBriefView.as_view(), name='data-daily-brief'),
    path('data/flagship-demo', FlagshipInventoryContradictionDemoView.as_view(), name='data-flagship-demo'),

    # Mega Prompt #29: AI Research, Web Intelligence & Deep Research OS
    path('research/overview', DeepResearchOverviewView.as_view(), name='research-overview'),
    path('research/plan', DeepResearchPlanView.as_view(), name='research-plan'),
    path('research/verify-claim', ClaimVerifyView.as_view(), name='research-verify-claim'),
    path('research/contradictions', ContradictionAnalysisView.as_view(), name='research-contradictions'),
    path('research/evidence-pack', EvidencePackView.as_view(), name='research-evidence-pack'),
    path('research/firewall/evaluate', ResearchFirewallView.as_view(), name='research-firewall-evaluate'),
    path('research/daily-brief', DailyResearchBriefView.as_view(), name='research-daily-brief'),
    path('research/flagship-demo', FlagshipDeepResearchDemoView.as_view(), name='research-flagship-demo'),

    # Mega Prompt #30: AI Process Intelligence, Workflow Mining & Autonomous Business Operations OS
    path('process/overview', ProcessPlatformOverviewView.as_view(), name='process-overview'),
    path('process/mining', ProcessMiningView.as_view(), name='process-mining'),
    path('process/bottlenecks', ProcessBottleneckDetectionView.as_view(), name='process-bottlenecks'),
    path('process/optimize-simulate', WorkflowOptimizationSimulationView.as_view(), name='process-optimize-simulate'),
    path('process/firewall/evaluate', ProcessFirewallView.as_view(), name='process-firewall-evaluate'),
    path('process/daily-brief', DailyProcessBriefView.as_view(), name='process-daily-brief'),
    path('process/flagship-demo', FlagshipB2BProcessDemoView.as_view(), name='process-flagship-demo'),

    # FINAL MASTER PROMPT: AI-Native Commerce Operating System Master Loop & Audit
    path('master/system-audit', MasterSystemAuditView.as_view(), name='master-system-audit'),
    path('master/master-loop', MasterSystemLoopRunView.as_view(), name='master-master-loop'),
]







