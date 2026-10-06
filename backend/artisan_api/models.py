import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Existing Enums
class Role(models.TextChoices):
    SUPER_ADMIN = 'super_admin', 'Super Admin'
    ORG_ADMIN = 'org_admin', 'Organization Admin'
    MANAGER = 'manager', 'Manager'
    ARTISAN = 'artisan', 'Artisan'
    CUSTOMER = 'customer', 'Customer'
    VIEWER = 'viewer', 'Viewer'

class ArtisanProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artisan_profile')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='artisans')
    craft_type = models.CharField(max_length=100, default='Handicrafts')
    region = models.CharField(max_length=100, default='Rajasthan, India')
    bio = models.TextField(blank=True, default='')
    preferred_language = models.CharField(max_length=50, default='hi')
    phone = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.craft_type})"

class ProductStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ANALYZED = 'analyzed', 'AI Analyzed'
    APPROVED = 'approved', 'Approved by Artisan'
    PUBLISHED = 'published', 'Published to Storefront'

class VerificationState(models.TextChoices):
    UNVERIFIED = 'unverified', 'Unverified'
    DECLARED = 'declared', 'Declared by Artisan'
    ORGANIZATION_VERIFIED = 'org_verified', 'Organization Verified'
    PLATFORM_VERIFIED = 'platform_verified', 'Platform Verified'

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    title = models.CharField(max_length=255, blank=True, default='Untitled Artisan Creation')
    description = models.TextField(blank=True, default='')
    category = models.CharField(max_length=100, default='Handicrafts')
    tags = models.JSONField(default=list, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=ProductStatus.choices, default=ProductStatus.DRAFT)
    verification_state = models.CharField(max_length=30, choices=VerificationState.choices, default=VerificationState.ORGANIZATION_VERIFIED)
    
    # AI Cost & Pricing metadata
    material_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    packaging_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    margin_percent = models.DecimalField(max_digits=5, decimal_places=2, default=30.00)
    suggested_min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    suggested_max_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pricing_explanation = models.TextField(blank=True, default='')
    
    # AI Readiness & Quality score
    quality_score = models.IntegerField(default=85)
    ai_readiness_score = models.IntegerField(default=92)
    quality_issues = models.JSONField(default=list, blank=True)
    
    # Multilingual & Verified facts
    translations = models.JSONField(default=dict, blank=True)
    verified_facts = models.JSONField(default=dict, blank=True)
    quality_flags = models.JSONField(default=list, blank=True)
    voice_transcript = models.TextField(blank=True, default='')
    
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - ₹{self.price} [{self.status}]"

class ProductMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    original_file = models.ImageField(upload_to='products/original/')
    processed_file = models.ImageField(upload_to='products/processed/', blank=True, null=True)
    media_type = models.CharField(max_length=50, default='image/jpeg')
    is_primary = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductFact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='facts')
    field = models.CharField(max_length=100)
    value = models.TextField()
    source = models.CharField(max_length=50, default='voice')
    confidence = models.FloatField(default=0.9)
    verified = models.BooleanField(default=False)

class Variant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    stock = models.IntegerField(default=10)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.IntegerField(default=15)
    reserved_quantity = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

class InventoryReservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reservations')
    quantity = models.IntegerField(default=1)
    session_id = models.CharField(max_length=100)
    is_committed = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=150, default='Guest Customer')
    customer_phone = models.CharField(max_length=30, blank=True, default='')
    customer_email = models.EmailField(blank=True, default='')
    shipping_address = models.TextField(default='New Delhi, India')
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='orders')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_orders')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_status = models.CharField(max_length=50, default='Paid via UPI')
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100, default='Interested Buyer')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    channel = models.CharField(max_length=50, default='web_chat')
    status = models.CharField(max_length=50, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20)
    content = models.TextField()
    tool_calls = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class AgentRun(models.Model):
    run_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    input_data = models.JSONField(default=dict, blank=True)
    output_data = models.JSONField(default=dict, blank=True)
    latency_ms = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=6, decimal_places=4, default=0.0000)
    status = models.CharField(max_length=50, default='success')
    timestamp = models.DateTimeField(auto_now_add=True)

class OrganizationType(models.TextChoices):
    NGO = 'ngo', 'NGO'
    SHG = 'shg', 'Self Help Group'
    COOPERATIVE = 'cooperative', 'Cooperative'
    GOVT = 'govt', 'Government Organization'
    COLLECTIVE = 'collective', 'Artisan Collective'

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    org_type = models.CharField(max_length=50, choices=OrganizationType.choices, default=OrganizationType.NGO)
    registration_number = models.CharField(max_length=100, blank=True, default='')
    region = models.CharField(max_length=100, default='India')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_org_type_display()})"

class OrganizationMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_memberships')
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.ARTISAN)
    joined_at = models.DateTimeField(auto_now_add=True)

class MarketplaceAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marketplace_accounts')
    platform = models.CharField(max_length=50)
    account_ref = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='connected')
    created_at = models.DateTimeField(auto_now_add=True)

class MarketplaceSyncLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sync_logs')
    action = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='success')
    error_message = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    provider = models.CharField(max_length=50, default='Razorpay')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, default='captured')
    signature_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Shipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')
    carrier = models.CharField(max_length=50, default='India Post')
    tracking_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='in_transit')
    estimated_delivery = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=255)
    festival = models.CharField(max_length=100, default='Diwali')
    suggested_bundle = models.JSONField(default=dict, blank=True)
    whatsapp_copy = models.TextField(blank=True, default='')
    instagram_caption = models.TextField(blank=True, default='')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class SyncQueue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sync_queue')
    operation_type = models.CharField(max_length=50)
    payload = models.JSONField(default=dict)
    retry_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class AgentMemory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_memories')
    memory_type = models.CharField(max_length=50, default='long_term_preference')
    key = models.CharField(max_length=100)
    value = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

class BusinessKnowledge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=100, default='shipping_policy')
    title = models.CharField(max_length=255)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductPassport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='passport')
    passport_code = models.CharField(max_length=100, unique=True)
    artisan_verified = models.BooleanField(default=True)
    material_declaration = models.CharField(max_length=255, default='100% Genuine Artisan Material')
    origin_declaration = models.CharField(max_length=255, default='Rajasthan, India')
    sustainability_rating = models.CharField(max_length=50, default='A+ Eco-Friendly Handcrafted')
    created_at = models.DateTimeField(auto_now_add=True)

class LLMCostTracker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=50, default='Gemini')
    model_name = models.CharField(max_length=100, default='gemini-3.6-flash')
    operation = models.CharField(max_length=100, default='CopilotQuery')
    tokens_used = models.IntegerField(default=350)
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=6, default=0.000350)
    latency_ms = models.IntegerField(default=180)
    timestamp = models.DateTimeField(auto_now_add=True)

class AgentIdentity(models.Model):
    agent_id = models.CharField(max_length=100, primary_key=True)
    client_name = models.CharField(max_length=150)
    scopes = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AgentSession(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(AgentIdentity, on_delete=models.CASCADE, related_name='sessions')
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class AgentAuditTrail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_id = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=30, default='READ')
    input_summary = models.JSONField(default=dict)
    result_summary = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

class BusinessGoalPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goal_plans')
    goal = models.CharField(max_length=255)
    plan_steps = models.JSONField(default=list)
    status = models.CharField(max_length=30, default='proposed')
    created_at = models.DateTimeField(auto_now_add=True)

class FeatureFlag(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    is_enabled = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True, default='')

# --- PROMPT #4 NEW EXTENSION MODELS ---

class TaskPriority(models.TextChoices):
    LOW = 'low', 'Low'
    NORMAL = 'normal', 'Normal'
    HIGH = 'high', 'High'
    URGENT = 'urgent', 'Urgent'

class TaskStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    RUNNING = 'running', 'Running'
    WAITING_APPROVAL = 'waiting_approval', 'Waiting Approval'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'

class AITask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_ai_tasks')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_team = models.CharField(max_length=50, default='ProductTeam') # ProductTeam, BusinessTeam, CommerceTeam
    assigned_agent = models.CharField(max_length=100, default='Catalog Agent')
    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=20, choices=TaskPriority.choices, default=TaskPriority.NORMAL)
    status = models.CharField(max_length=30, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    payload = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True)
    requires_approval = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ApprovalInboxItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(AITask, on_delete=models.CASCADE, null=True, blank=True, related_name='approval_items')
    artisan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approval_inbox_items')
    action_type = models.CharField(max_length=100) # UPDATE_PRICE, PUBLISH_MARKETPLACE, LAUNCH_CAMPAIGN, BUNDLE_CREATE
    summary = models.TextField(default='')
    reason = models.TextField(default='')
    description = models.TextField(default='')
    expected_impact = models.CharField(max_length=255, default='Increases conversion by ~18%')
    preview_data = models.JSONField(default=dict, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default='pending') # pending, approved, rejected, edited
    created_at = models.DateTimeField(auto_now_add=True)

class SmartSupportTicket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=150, default='Valued Customer')
    issue = models.TextField()
    customer_context = models.JSONField(default=dict, blank=True)
    ai_summary = models.TextField(blank=True, default='')
    suggested_resolution = models.TextField(blank=True, default='')
    priority = models.CharField(max_length=20, default='normal')
    status = models.CharField(max_length=30, default='open') # open, escalated, resolved
    created_at = models.DateTimeField(auto_now_add=True)

class EventExhibitionMode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=255, default='Craft Fair Event')
    name = models.CharField(max_length=255, default='Craft Fair Event')
    location = models.CharField(max_length=255, default='New Delhi')
    qr_code_slug = models.CharField(max_length=100, default='event-qr')
    qr_code_ref = models.CharField(max_length=100, default='event-ref')
    event_products = models.ManyToManyField(Product, blank=True, related_name='events')
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.CharField(max_length=150)
    action = models.CharField(max_length=150)
    object_id = models.CharField(max_length=150, blank=True, default='')
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class ParticipantType(models.TextChoices):
    ARTISAN = 'ARTISAN', 'Artisan'
    CUSTOMER = 'CUSTOMER', 'Customer'
    ORGANIZATION = 'ORGANIZATION', 'Organization'
    MARKETPLACE = 'MARKETPLACE', 'Marketplace'
    AI_AGENT = 'AI_AGENT', 'AI Agent'
    DEVELOPER = 'DEVELOPER', 'Developer'
    PARTNER = 'PARTNER', 'Partner'


class TrustLevel(models.TextChoices):
    UNVERIFIED = 'UNVERIFIED', 'Unverified'
    BASIC_VERIFIED = 'BASIC_VERIFIED', 'Basic Verified'
    ORGANIZATION_VERIFIED = 'ORGANIZATION_VERIFIED', 'Organization Verified'
    PLATFORM_VERIFIED = 'PLATFORM_VERIFIED', 'Platform Verified'


class NetworkIdentity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='network_identity')
    participant_type = models.CharField(max_length=30, choices=ParticipantType.choices, default=ParticipantType.ARTISAN)
    trust_level = models.CharField(max_length=30, choices=TrustLevel.choices, default=TrustLevel.BASIC_VERIFIED)
    trust_signals = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField(default=1)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, default='')
    provenance_sources = models.JSONField(default=dict, blank=True) # e.g. {'materials': 'ARTISAN_DECLARED', 'description': 'AI_GENERATED'}
    created_at = models.DateTimeField(auto_now_add=True)


class MarketExpansionExperiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    target_market = models.CharField(max_length=50, default='UAE') # UAE, USA, EU
    currency = models.CharField(max_length=10, default='AED')
    products = models.ManyToManyField(Product, blank=True)
    status = models.CharField(max_length=20, default='ACTIVE') # DRAFT, ACTIVE, COMPLETED
    metrics = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ThirdPartyAIAgent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    developer_name = models.CharField(max_length=150, default='Ecosystem Developer')
    version = models.CharField(max_length=20, default='v1.0')
    pricing_model = models.CharField(max_length=30, default='FREE') # FREE, SUBSCRIPTION, USAGE_BASED
    required_scopes = models.JSONField(default=list, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.85)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DeadLetterQueueItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_type = models.CharField(max_length=100)
    payload = models.JSONField(default=dict, blank=True)
    error_log = models.TextField(blank=True, default='')
    retry_count = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default='FAILED') # FAILED, REPLAYED, DISCARDED
    created_at = models.DateTimeField(auto_now_add=True)


class LearningSource(models.TextChoices):
    OBSERVED = 'OBSERVED', 'Observed'
    DERIVED = 'DERIVED', 'Derived'
    USER_FEEDBACK = 'USER_FEEDBACK', 'User Feedback'
    EXPERIMENT = 'EXPERIMENT', 'Experiment'
    EXTERNAL_DATA = 'EXTERNAL_DATA', 'External Data'
    AI_GENERATED = 'AI_GENERATED', 'AI Generated'


class AILearningStore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recommendation_title = models.CharField(max_length=255)
    context = models.JSONField(default=dict, blank=True)
    action_taken = models.CharField(max_length=255)
    expected_outcome = models.CharField(max_length=255)
    actual_outcome = models.CharField(max_length=255, default='Pending Evaluation')
    source = models.CharField(max_length=30, choices=LearningSource.choices, default=LearningSource.EXPERIMENT)
    is_successful = models.BooleanField(default=True)
    impact_delta = models.CharField(max_length=100, default='+0.0%')
    created_at = models.DateTimeField(auto_now_add=True)


class PromptVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt_key = models.CharField(max_length=100) # e.g. catalog-agent-v1, pricing-agent-v2
    version = models.CharField(max_length=20, default='v1.0')
    template_text = models.TextField()
    status = models.CharField(max_length=20, default='PRODUCTION') # DRAFT, EVALUATED, CANARY, PRODUCTION
    evaluation_score = models.DecimalField(max_digits=4, decimal_places=2, default=94.50)
    created_at = models.DateTimeField(auto_now_add=True)


class AIPromptExperiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experiment_name = models.CharField(max_length=255)
    variant_a = models.ForeignKey(PromptVersion, on_delete=models.CASCADE, related_name='experiments_a')
    variant_b = models.ForeignKey(PromptVersion, on_delete=models.CASCADE, related_name='experiments_b')
    metrics_a = models.JSONField(default=dict, blank=True) # {latency: 420, approval_rate: "92%"}
    metrics_b = models.JSONField(default=dict, blank=True)
    winning_variant = models.CharField(max_length=20, default='VARIANT_A')
    created_at = models.DateTimeField(auto_now_add=True)


class ProductSearchGap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    search_query = models.CharField(max_length=255, unique=True)
    query_count = models.IntegerField(default=1)
    category_hint = models.CharField(max_length=100, default='Pottery & Craft')
    suggested_artisan_action = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, default='OPEN') # OPEN, IN_DEVELOPMENT, RESOLVED
    created_at = models.DateTimeField(auto_now_add=True)


# --- PROMPT #7 COMMERCE INTELLIGENCE & AUTONOMOUS DECISION ENGINE MODELS ---

class SignalSeverity(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'
    CRITICAL = 'critical', 'Critical'

class BusinessSignal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='signals')
    signal_type = models.CharField(max_length=100) # e.g. LOW_CONVERSION, HIGH_DEMAND_LOW_STOCK, BUNDLE_OPPORTUNITY
    entity_type = models.CharField(max_length=50, default='product') # product, inventory, order, channel
    entity_id = models.CharField(max_length=100, blank=True, default='')
    severity = models.CharField(max_length=20, choices=SignalSeverity.choices, default=SignalSeverity.MEDIUM)
    confidence = models.FloatField(default=0.85)
    evidence = models.JSONField(default=list, blank=True)
    detected_at = models.DateTimeField(auto_now_add=True)

class OpportunityStatus(models.TextChoices):
    DISCOVERED = 'discovered', 'Discovered'
    EVALUATING = 'evaluating', 'Evaluating'
    PLAN_READY = 'plan_ready', 'Plan Ready'
    APPROVED = 'approved', 'Approved'
    EXECUTING = 'executing', 'Executing'
    COMPLETED = 'completed', 'Completed'
    DISMISSED = 'dismissed', 'Dismissed'

class Opportunity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='opportunities')
    opportunity_type = models.CharField(max_length=100) # e.g. IMPROVE_LISTING, RESTOCK, FESTIVAL_CAMPAIGN, BUNDLE
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    entity_type = models.CharField(max_length=50, default='product')
    entity_id = models.CharField(max_length=100, blank=True, default='')
    evidence = models.JSONField(default=list, blank=True)
    confidence = models.FloatField(default=0.88)
    expected_impact = models.CharField(max_length=255, default='+15% Conversion')
    urgency = models.CharField(max_length=20, default='HIGH') # LOW, MEDIUM, HIGH, URGENT
    possible_actions = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=30, choices=OpportunityStatus.choices, default=OpportunityStatus.DISCOVERED)
    created_at = models.DateTimeField(auto_now_add=True)

class GoalStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    PAUSED = 'paused', 'Paused'
    ACHIEVED = 'achieved', 'Achieved'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'

class BusinessGoal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_goals')
    tenant_id = models.CharField(max_length=100, blank=True, default='default-tenant')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    target_metric = models.CharField(max_length=100, default='REVENUE') # REVENUE, UNITS_SOLD, CONVERSION_RATE, CLEARANCE
    target_value = models.DecimalField(max_digits=12, decimal_places=2, default=50000.00)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=18450.00)
    deadline = models.DateField(null=True, blank=True)
    constraints = models.JSONField(default=dict, blank=True) # {"max_spend": 5000, "max_discount_pct": 12}
    autonomy_level = models.IntegerField(default=2) # Level 0..4
    status = models.CharField(max_length=20, choices=GoalStatus.choices, default=GoalStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

class AIPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal = models.ForeignKey(BusinessGoal, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=255)
    steps = models.JSONField(default=list, blank=True)
    dependencies = models.JSONField(default=list, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    risk_level = models.CharField(max_length=20, default='MEDIUM') # LOW, MEDIUM, HIGH, CRITICAL
    required_permissions = models.JSONField(default=list, blank=True)
    success_metrics = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=30, default='in_progress') # in_progress, paused, completed, failed
    created_at = models.DateTimeField(auto_now_add=True)

class DecisionTrace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='decision_traces')
    agent_name = models.CharField(max_length=100, default='Commerce Decision Engine')
    model_name = models.CharField(max_length=100, default='gemini-3.6-flash')
    input_context_ref = models.CharField(max_length=255, blank=True, default='')
    retrieved_evidence = models.JSONField(default=list, blank=True)
    candidate_actions = models.JSONField(default=list, blank=True)
    selected_action = models.JSONField(default=dict, blank=True)
    confidence = models.FloatField(default=0.88)
    risk_assessment = models.CharField(max_length=30, default='MEDIUM')
    policy_evaluation = models.JSONField(default=dict, blank=True)
    approval_required = models.BooleanField(default=True)
    tool_calls = models.JSONField(default=list, blank=True)
    execution_result = models.JSONField(default=dict, blank=True)
    outcome_measurement = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class DailyAIBrief(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_briefs')
    date = models.DateField(default=timezone.now)
    orders_count = models.IntegerField(default=12)
    revenue_amount = models.DecimalField(max_digits=10, decimal_places=2, default=18450.00)
    needs_attention = models.JSONField(default=list, blank=True)
    opportunity_text = models.TextField(blank=True, default='')
    suggested_action = models.TextField(blank=True, default='')
    pending_approvals_count = models.IntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)


# --- PROMPT #8 SUPPLY CHAIN, B2B COMMERCE & ARTISAN SUPER APP MODELS ---

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default='Terracotta & Raw Clay')
    materials_provided = models.JSONField(default=list, blank=True)
    location = models.CharField(max_length=150, default='Jaipur, Rajasthan')
    lead_time_days = models.IntegerField(default=4)
    moq = models.IntegerField(default=25)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=450.00)
    quality_rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.85)
    reliability_score = models.IntegerField(default=96)
    payment_terms = models.CharField(max_length=100, default='Net 30 Days')
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

class RawMaterial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='raw_materials')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default='Clay') # Clay, Cotton, Silk, Natural Dyes, Wood, Metal, Packaging
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=65.00)
    unit = models.CharField(max_length=20, default='kg') # kg, meter, liter, piece
    moq = models.IntegerField(default=10)
    stock_available = models.IntegerField(default=500)
    lead_time_days = models.IntegerField(default=3)

class BillOfMaterials(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bom_items')
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity_required = models.DecimalField(max_digits=8, decimal_places=2, default=2.5) # e.g. 2.5 kg
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=65.00)
    labor_hours = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)

class ProcurementOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='procurement_orders')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    material_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=65.00)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=3250.00)
    status = models.CharField(max_length=30, default='ORDERED') # DRAFT, PENDING_APPROVAL, ORDERED, RECEIVED, CANCELLED
    created_at = models.DateTimeField(auto_now_add=True)

class B2BBuyerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='b2b_buyer_profile')
    company_name = models.CharField(max_length=255, default='Heritage Craft Boutique Retail')
    buyer_type = models.CharField(max_length=50, default='RETAIL_STORE') # RETAIL_STORE, HOTEL, EXPORTER, CORPORATE_GIFT
    tax_id = models.CharField(max_length=100, blank=True, default='GSTIN08AAACH1234F1Z5')
    shipping_address = models.TextField(default='Bandra Kurla Complex, Mumbai')
    created_at = models.DateTimeField(auto_now_add=True)

class RequestForQuote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rfqs')
    title = models.CharField(max_length=255)
    product_category = models.CharField(max_length=100, default='Handcrafted Corporate Gifts')
    quantity = models.IntegerField(default=1000)
    target_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=750.00)
    deadline_days = models.IntegerField(default=25)
    customization_requirements = models.TextField(blank=True, default='Blue silk packaging with company logo embossing')
    status = models.CharField(max_length=30, default='OPEN') # OPEN, QUOTED, ALLOCATED, COMPLETED
    created_at = models.DateTimeField(auto_now_add=True)

class B2BQuotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfq = models.ForeignKey(RequestForQuote, on_delete=models.CASCADE, related_name='quotations')
    supplier_or_collective = models.CharField(max_length=255, default='Jaipur Artisan Collective')
    offered_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=720.00)
    lead_time_days = models.IntegerField(default=20)
    moq = models.IntegerField(default=100)
    customization_notes = models.TextField(blank=True, default='Hand-embossed logo included with natural clay finish')
    status = models.CharField(max_length=30, default='SUBMITTED') # DRAFT, SUBMITTED, ACCEPTED, REJECTED
    created_at = models.DateTimeField(auto_now_add=True)

class SplitOrderAllocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfq = models.ForeignKey(RequestForQuote, on_delete=models.CASCADE, related_name='allocations')
    artisan_group_name = models.CharField(max_length=255, default='Jaipur Craft Group')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE)
    allocated_quantity = models.IntegerField(default=350)
    unit_payout = models.DecimalField(max_digits=10, decimal_places=2, default=650.00)
    status = models.CharField(max_length=30, default='IN_PRODUCTION') # IN_PRODUCTION, QC_PASSED, FULFILLED
    created_at = models.DateTimeField(auto_now_add=True)

class QualityControlCheckpoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfq = models.ForeignKey(RequestForQuote, on_delete=models.CASCADE, related_name='qc_checkpoints')
    stage = models.CharField(max_length=50, default='PRODUCTION_INSPECTION') # MATERIAL_INSPECTION, PRODUCTION_INSPECTION, FINAL_PACKAGING
    status = models.CharField(max_length=30, default='PASSED') # PASSED, REJECTED, NEEDS_REVIEW
    inspector_notes = models.TextField(blank=True, default='Zero hairline cracks. Uniform pigment density verified.')
    created_at = models.DateTimeField(auto_now_add=True)


# --- PROMPT #9 GLOBAL COMMERCE, EXPORT & AI TRADE NETWORK MODELS ---

class GlobalCommerceProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='global_commerce_profile')
    business_country = models.CharField(max_length=100, default='India')
    business_region = models.CharField(max_length=100, default='Rajasthan')
    preferred_currencies = models.JSONField(default=list, blank=True)
    supported_languages = models.JSONField(default=list, blank=True)
    export_readiness_score = models.IntegerField(default=85)
    shipping_capabilities = models.JSONField(default=dict, blank=True)
    accepted_payment_methods = models.JSONField(default=list, blank=True)
    documentation_status = models.CharField(max_length=50, default='PARTIALLY_READY')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Global Profile ({self.user.username}) - {self.business_country}"

class MarketProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country_code = models.CharField(max_length=10, unique=True) # US, DE, AE, GB, JP
    country_name = models.CharField(max_length=100)
    currency = models.CharField(max_length=10, default='USD')
    languages = models.JSONField(default=list, blank=True)
    shipping_carriers = models.JSONField(default=list, blank=True)
    regulatory_summary = models.TextField(blank=True, default='')
    compliance_confidence = models.FloatField(default=0.92)
    official_source_url = models.CharField(max_length=255, blank=True, default='https://trade.gov')
    freshness_status = models.CharField(max_length=30, default='FRESH') # FRESH, STALE, UNKNOWN
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.country_name} ({self.country_code})"

class TradeDocumentWorkspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_documents')
    doc_type = models.CharField(max_length=100, default='COMMERCIAL_INVOICE') # COMMERCIAL_INVOICE, PACKING_LIST, CERTIFICATE_OF_ORIGIN, CUSTOMS_DECLARATION
    title = models.CharField(max_length=255)
    reference_code = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=30, default='VERIFIED') # DRAFT, PENDING_REVIEW, VERIFIED, MISMATCH
    content_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} - {self.reference_code}"

class ComplianceKnowledgeRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country_code = models.CharField(max_length=10)
    category = models.CharField(max_length=100, default='Packaging & Labeling')
    requirement_summary = models.TextField()
    source_title = models.CharField(max_length=255, default='Official Customs & Trade Portal')
    source_url = models.CharField(max_length=255, default='https://customs.gov')
    retrieved_at = models.DateTimeField(auto_now_add=True)
    scope = models.CharField(max_length=100, default='HANDICRAFTS_CERAMICS')

    def __str__(self):
        return f"{self.country_code} - {self.category}"

class ExportReadinessScorecard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='export_scorecards')
    target_country = models.CharField(max_length=10, default='DE')
    readiness_status = models.CharField(max_length=30, default='PARTIALLY_READY') # READY, PARTIALLY_READY, NOT_READY
    readiness_breakdown = models.JSONField(default=dict, blank=True)
    missing_items = models.JSONField(default=list, blank=True)
    action_plan = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scorecard: {self.product.title} -> {self.target_country} [{self.readiness_status}]"


# --- PROMPT #10 AI AGENT MARKETPLACE & DEVELOPER ECOSYSTEM MODELS ---

class AgentPurchasePolicy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_purchase_policy')
    max_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00)
    requires_confirmation_above = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00)
    daily_budget_limit = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    allowed_categories = models.JSONField(default=list, blank=True)
    allowed_merchants = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Purchase Policy ({self.user.username}) - Max ₹{self.max_order_value}"

class AgentToolDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    version = models.CharField(max_length=20, default='v1.0')
    input_schema = models.JSONField(default=dict, blank=True)
    output_schema = models.JSONField(default=dict, blank=True)
    required_scopes = models.JSONField(default=list, blank=True)
    risk_level = models.CharField(max_length=30, default='READ') # READ, WRITE, SENSITIVE, CRITICAL
    status = models.CharField(max_length=30, default='PUBLISHED') # DRAFT, PUBLISHED, DEPRECATED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.version}) [{self.risk_level}]"

class AgentNegotiationSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer_agent_id = models.CharField(max_length=100, default='buyer_agent_01')
    seller_agent_id = models.CharField(max_length=100, default='seller_agent_01')
    rfq_id = models.CharField(max_length=100)
    status = models.CharField(max_length=30, default='OPEN') # OPEN, COUNTER_OFFER, AGREED, REJECTED
    offers_history = models.JSONField(default=list, blank=True)
    agreement_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Negotiation #{str(self.id)[:8]} [{self.status}]"

class AgentAttributionLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_id = models.CharField(max_length=100)
    source_type = models.CharField(max_length=30, default='AI_AGENT') # HUMAN, AI_AGENT
    action_type = models.CharField(max_length=50) # SEARCH, COMPARE, CART, CHECKOUT, PURCHASE
    gmv_impact = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attribution: {self.agent_id} -> {self.action_type} (₹{self.gmv_impact})"


# --- PROMPT #11 AI SOCIAL COMMERCE & CREATOR ECONOMY MODELS ---

class SocialProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_profile')
    roles = models.JSONField(default=list, blank=True) # ['artisan', 'creator', 'buyer', 'affiliate']
    bio = models.TextField(blank=True, default='')
    craft_story = models.TextField(blank=True, default='')
    craft_region = models.CharField(max_length=100, default='Rajasthan, India')
    verified_info = models.JSONField(default=dict, blank=True)
    public_visibility = models.BooleanField(default=True)
    social_links = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SocialProfile ({self.user.username}) Roles: {self.roles}"

class ContentAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_assets')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='content_assets')
    title = models.CharField(max_length=255, default='AI Social Content Draft')
    content_type = models.CharField(max_length=50, default='instagram_post') # instagram_post, short_video_script, carousel, whatsapp_msg, blog_post, story
    channel = models.CharField(max_length=50, default='instagram') # instagram, whatsapp, facebook, website, pinterest, email
    script_text = models.TextField(blank=True, default='')
    visual_storyboard = models.JSONField(default=list, blank=True)
    caption = models.TextField(blank=True, default='')
    version = models.IntegerField(default=1)
    prompt_version = models.CharField(max_length=20, default='v1.0')
    factuality_status = models.CharField(max_length=50, default='VERIFIED_GROUNDED') # VERIFIED_GROUNDED, AI_WORDING, UNVERIFIED
    price_consistency_status = models.CharField(max_length=50, default='VALIDATED') # VALIDATED, MISMATCH
    status = models.CharField(max_length=30, default='draft') # draft, preview, approved, scheduled, published, rejected
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Asset: {self.title} [{self.channel} - {self.status}]"

class ContentCampaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_campaigns')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='creator_content_campaigns')
    title = models.CharField(max_length=255, default='Artisan Campaign')
    objective = models.CharField(max_length=255, default='Diwali Handmade Gifting Campaign')
    target_audience = models.CharField(max_length=255, default='Eco-Conscious & Craft Admirers')
    channels = models.JSONField(default=list, blank=True) # ['instagram', 'whatsapp', 'facebook']
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    estimated_reach = models.IntegerField(default=15000)
    status = models.CharField(max_length=30, default='draft') # draft, active, paused, completed, cancelled
    content_themes = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Campaign: {self.title} (₹{self.budget})"

class ContentSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(ContentCampaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules')
    asset = models.ForeignKey(ContentAsset, on_delete=models.CASCADE, related_name='schedules')
    channel = models.CharField(max_length=50, default='instagram')
    scheduled_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, default='scheduled') # draft, pending, approved, scheduled, published, failed, cancelled
    publication_logs = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Schedule: {self.asset.title} on {self.channel} [{self.status}]"

class CreatorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_profile')
    name = models.CharField(max_length=255, default='Artisan Creator')
    bio = models.TextField(blank=True, default='')
    categories = models.JSONField(default=list, blank=True) # ['handicrafts', 'home_decor', 'gifting']
    audience_languages = models.JSONField(default=list, blank=True) # ['hi', 'en']
    content_style = models.CharField(max_length=100, default='Storytelling & Unboxing')
    approved_metrics = models.JSONField(default=dict, blank=True) # {'avg_reach': 25000, 'engagement_rate': '4.8%'}
    public_portfolio = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Creator: {self.name} ({self.content_style})"

class CreatorCampaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artisan_creator_collaborations')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_collaborations')
    campaign = models.ForeignKey(ContentCampaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='creator_links')
    products = models.ManyToManyField(Product, blank=True)
    requirements = models.TextField(blank=True, default='Create 1 Unboxing Video + 1 Instagram Reel highlighting craft process')
    deadline = models.DateTimeField(default=timezone.now)
    fixed_compensation = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    status = models.CharField(max_length=30, default='INVITED') # INVITED, ACCEPTED, DRAFT_SUBMITTED, APPROVED, PUBLISHED, COMPLETED, REJECTED
    deliverables = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Creator Collab: {self.artisan.username} x {self.creator.username} [{self.status}]"

class Referral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_referrals')
    referred_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_referrals')
    referral_code = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, CONVERTED, EXPIRED
    total_clicks = models.IntegerField(default=0)
    total_conversions = models.IntegerField(default=0)
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral {self.referral_code} by {self.referrer.username} [{self.status}]"

class AffiliateCommission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='affiliate_commissions')
    referral = models.ForeignKey(Referral, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payout_status = models.CharField(max_length=30, default='PENDING') # PENDING, APPROVED, PAID, CANCELLED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission ₹{self.commission_earned} for {self.creator.username} [{self.payout_status}]"

class Community(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    topic_category = models.CharField(max_length=100, default='Craft Education')
    description = models.TextField(blank=True, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_communities')
    is_private = models.BooleanField(default=False)
    member_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Community: {self.name} ({self.topic_category})"

class CommunityPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    title = models.CharField(max_length=255)
    body = models.TextField()
    post_type = models.CharField(max_length=50, default='QUESTION') # QUESTION, CRAFT_STORY, REVIEW, TUTORIAL
    verified_answer_flag = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default='PUBLISHED') # PUBLISHED, FLAGGED, REMOVED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post: {self.title} by {self.author.username}"

class LiveSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='live_sessions')
    scheduled_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, default='SCHEDULED') # SCHEDULED, LIVE, ENDED
    viewer_count = models.IntegerField(default=0)
    product_showcase = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Live: {self.title} by {self.host.username} [{self.status}]"


# --- PROMPT #12 AI FINANCE, OPERATIONS & BUSINESS INTELLIGENCE MODELS ---

class LedgerEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ledger_entries')
    entry_type = models.CharField(max_length=50, default='SALE') # SALE, REFUND, PAYMENT, PAYOUT, EXPENSE, PURCHASE, SHIPPING_COST, PLATFORM_FEE, MARKETPLACE_FEE, CREATOR_COMMISSION, AFFILIATE_COMMISSION, TAX_RESERVE, PRODUCTION_COST, RAW_MATERIAL_COST, AD_SPEND
    reference_type = models.CharField(max_length=50, default='ORDER') # ORDER, INVOICE, EXPENSE, CAMPAIGN, SETTLEMENT
    reference_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    direction = models.CharField(max_length=10, default='CREDIT') # CREDIT, DEBIT
    category = models.CharField(max_length=100, default='Revenue')
    status = models.CharField(max_length=30, default='POSTED') # DRAFT, POSTED, REVERSED
    occurred_at = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ledger: {self.entry_type} ₹{self.amount} ({self.direction}) [{self.status}]"

class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    vendor_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default='Packaging') # Raw Material, Shipping, Packaging, Marketing, Utilities, Platform Fee
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    invoice_number = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=30, default='APPROVED') # DRAFT, PENDING_APPROVAL, APPROVED, REJECTED
    cost_center = models.CharField(max_length=100, default='Operations')
    ai_confidence = models.FloatField(default=0.95)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense: {self.vendor_name} ₹{self.amount} ({self.category}) [{self.status}]"

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=100, unique=True)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    customer_name = models.CharField(max_length=255)
    customer_email = models.CharField(max_length=255, blank=True, default='')
    invoice_type = models.CharField(max_length=50, default='B2C') # B2C, B2B, WHOLESALE, INTERNATIONAL
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=30, default='ISSUED') # DRAFT, ISSUED, PAID, OVERDUE, CANCELLED
    due_date = models.DateTimeField(default=timezone.now)
    line_items = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.customer_name} ₹{self.total_amount} [{self.status}]"

class SettlementReconciliation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settlements')
    marketplace_name = models.CharField(max_length=100, default='Amazon Handmade')
    expected_amount = models.DecimalField(max_digits=10, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=10, decimal_places=2)
    difference_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=30, default='MATCHED') # MATCHED, MISMATCH, UNDER_REVIEW
    mismatch_reason = models.CharField(max_length=255, blank=True, default='')
    settlement_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Settlement ({self.marketplace_name}): Exp ₹{self.expected_amount} vs Act ₹{self.actual_amount} [{self.status}]"

class FinancialScenario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_scenarios')
    scenario_name = models.CharField(max_length=255, default='Price Adjustment Simulation')
    price_change_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cost_change_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    shipping_change_inr = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    volume_change_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    estimated_revenue_impact = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estimated_margin_impact = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scenario: {self.scenario_name} (Rev impact: ₹{self.estimated_revenue_impact})"

class FinancialAnomaly(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_anomalies')
    anomaly_type = models.CharField(max_length=100) # REFUND_SPIKE, SETTLEMENT_MISMATCH, MARGIN_DROP, COST_SPIKE
    severity = models.CharField(max_length=30, default='HIGH') # CRITICAL, HIGH, MEDIUM, LOW
    evidence = models.JSONField(default=dict, blank=True)
    affected_entity_id = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=30, default='OPEN') # OPEN, INVESTIGATING, RESOLVED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anomaly: {self.anomaly_type} [{self.severity}] - {self.status}"

class PlatformBillingMeter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='billing_meter')
    subscription_plan = models.CharField(max_length=50, default='GROWTH') # FREE, STARTER, GROWTH, BUSINESS, ENTERPRISE
    total_llm_tokens = models.IntegerField(default=142000)
    total_ai_cost = models.DecimalField(max_digits=10, decimal_places=2, default=28.40)
    api_calls_count = models.IntegerField(default=1240)
    billing_cycle_start = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Billing ({self.user.username}): Plan {self.subscription_plan} - Cost ₹{self.total_ai_cost}"


# --- PROMPT #13 AI WORKFORCE OS & DIGITAL EMPLOYEES MODELS ---

class DigitalEmployee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='digital_employees')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='digital_employees')
    name = models.CharField(max_length=255) # e.g., "AI Finance Analyst", "AI Growth Manager"
    role = models.CharField(max_length=100, default='SPECIALIST') # FINANCE_ANALYST, GROWTH_MANAGER, OPERATIONS_MANAGER, PROCUREMENT_AGENT, SUPPORT_AGENT, EXPORT_ASSISTANT, RESEARCH_AGENT, QUALITY_AGENT, SALES_AGENT
    description = models.TextField(blank=True, default='')
    agent_type = models.CharField(max_length=50, default='DIGITAL_EMPLOYEE')
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, PAUSED, MAINTENANCE, SANDBOX, BUDGET_EXHAUSTED, RETIRED
    autonomy_level = models.IntegerField(default=2) # 0: Observe, 1: Recommend, 2: Prepare, 3: Pre-authorized low risk, 4: Autonomous
    system_instructions = models.TextField(blank=True, default='')
    goals = models.JSONField(default=list, blank=True)
    capabilities = models.JSONField(default=list, blank=True) # ["READ_FINANCE", "CREATE_TASK", "REQUEST_APPROVAL", "REFUND_PAYMENT"]
    tool_scopes = models.JSONField(default=dict, blank=True) # {"allowed": [...], "denied": [...], "approval_required": [...]}
    memory_scope = models.CharField(max_length=100, default='BUSINESS_MEMORY')
    knowledge_scope = models.JSONField(default=list, blank=True) # ["finance_sop", "return_sop"]
    approval_policy = models.JSONField(default=dict, blank=True) # {"financial_limit_inr": 5000, "require_human_approval": True}
    risk_policy = models.CharField(max_length=30, default='MEDIUM')
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    current_spend = models.DecimalField(max_digits=10, decimal_places=2, default=42.50)
    certification_status = models.CharField(max_length=30, default='CERTIFIED') # CERTIFIED, SANDBOX, FAILED, NEEDS_REVIEW
    version = models.CharField(max_length=30, default='v1.0')
    performance_score = models.FloatField(default=94.5)
    reliability_score = models.FloatField(default=96.0)
    accuracy_score = models.FloatField(default=95.0)
    tasks_completed_count = models.IntegerField(default=34)
    tasks_failed_count = models.IntegerField(default=1)
    human_corrections_count = models.IntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Digital Employee: {self.name} ({self.role}) [{self.status}]"

class AITeam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_teams')
    name = models.CharField(max_length=255) # e.g. "Diwali Festival Sales Team"
    mission = models.TextField()
    team_roles = models.JSONField(default=list, blank=True) # Roles/Employee IDs included
    status = models.CharField(max_length=30, default='ACTIVE')
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)
    current_spend = models.DecimalField(max_digits=10, decimal_places=2, default=150.00)
    team_memory = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Team: {self.name} - Budget ₹{self.budget}"

class AISOP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_sops')
    title = models.CharField(max_length=255) # e.g. "Customer Support & Return SOP"
    category = models.CharField(max_length=100, default='Support') # Support, Finance, Quality, Operations, Export
    sop_code = models.CharField(max_length=50, default='SOP-001')
    content = models.TextField() # Markdown SOP text
    structured_steps = models.JSONField(default=list, blank=True) # DAG steps: Trigger -> Validation -> Decision -> Action -> Approval
    source_authority = models.CharField(max_length=100, default='Human Manager')
    version = models.CharField(max_length=30, default='1.0')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOP: {self.title} [{self.sop_code}] (v{self.version})"

class WorkforceTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workforce_tasks')
    assigned_employee = models.ForeignKey(DigitalEmployee, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    team = models.ForeignKey(AITeam, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    task_type = models.CharField(max_length=100, default='ANALYSIS') # ANALYSIS, CAMPAIGN_CREATION, REORDER_PLAN, SETTLEMENT_INVESTIGATION, SOP_EXECUTION
    title = models.CharField(max_length=255)
    goal = models.TextField()
    priority = models.CharField(max_length=20, default='NORMAL') # LOW, NORMAL, HIGH, URGENT
    status = models.CharField(max_length=30, default='QUEUED') # BACKLOG, QUEUED, ASSIGNED, RUNNING, WAITING_APPROVAL, BLOCKED, COMPLETED, FAILED, CANCELLED
    input_context = models.JSONField(default=dict, blank=True)
    output_result = models.JSONField(default=dict, blank=True)
    shared_memory = models.JSONField(default=dict, blank=True) # Evidence, intermediate findings, decisions
    handoff_chain = models.JSONField(default=list, blank=True) # [{from_employee, to_employee, reason, timestamp}]
    dependencies = models.JSONField(default=list, blank=True) # [task_id_1, task_id_2]
    risk_level = models.CharField(max_length=20, default='MEDIUM') # LOW, MEDIUM, HIGH, CRITICAL
    approval_required = models.BooleanField(default=False)
    approval_status = models.CharField(max_length=30, default='NOT_REQUIRED') # NOT_REQUIRED, PENDING, APPROVED, REJECTED
    approval_reason = models.TextField(blank=True, default='')
    cost_budget = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sop_reference = models.ForeignKey(AISOP, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Workforce Task: {self.title} [{self.status}]"

class WorkforceIncident(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workforce_incidents')
    employee = models.ForeignKey(DigitalEmployee, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidents')
    incident_type = models.CharField(max_length=100) # POLICY_VIOLATION, INFINITE_LOOP_PREVENTED, BUDGET_EXCEEDED, PROMPT_INJECTION_BLOCKED, TOOL_EXECUTION_ERROR
    severity = models.CharField(max_length=20, default='HIGH') # LOW, MEDIUM, HIGH, CRITICAL
    details = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=30, default='RESOLVED') # OPEN, MITIGATED, RESOLVED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incident: {self.incident_type} [{self.severity}] - {self.status}"


# --- PROMPT #14 AI TRUST, GOVERNANCE, PRIVACY & SECURITY MODELS ---

class GovernancePolicy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='governance_policies')
    name = models.CharField(max_length=255) # e.g. "AI Payout Approval Threshold Policy"
    category = models.CharField(max_length=100, default='FINANCIAL') # FINANCIAL, SECURITY, PRIVACY, AGENT, DATA_ACCESS, EXPORT
    scope = models.CharField(max_length=50, default='TENANT') # GLOBAL, TENANT, ORGANIZATION, ROLE, AGENT
    conditions = models.JSONField(default=dict, blank=True) # e.g. {"action": "approve_payout", "actor_type": "AI_AGENT", "amount_min_inr": 0}
    effect = models.CharField(max_length=30, default='REQUIRE_APPROVAL') # ALLOW, DENY, REQUIRE_APPROVAL, REQUIRE_REVIEW, REDACT, LOG_ONLY
    priority = models.IntegerField(default=10) # 1 = Highest Security, 100 = Task Level
    version = models.CharField(max_length=30, default='v1.0')
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, DRAFT, DEPRECATED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Policy: {self.name} [{self.effect}] (v{self.version})"

class ToolTrustRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool_name = models.CharField(max_length=100, unique=True) # execute_payment, approve_payout, get_revenue, change_price
    description = models.TextField(blank=True, default='')
    risk_level = models.CharField(max_length=20, default='MEDIUM') # LOW, MEDIUM, HIGH, CRITICAL
    data_scope = models.CharField(max_length=50, default='INTERNAL') # PUBLIC, INTERNAL, CONFIDENTIAL, SENSITIVE, HIGHLY_SENSITIVE
    allowed_roles = models.JSONField(default=list, blank=True) # ["FINANCE_ANALYST", "SUPER_ADMIN"]
    require_human_approval = models.BooleanField(default=False)
    max_calls_per_hour = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Tool Trust: {self.tool_name} [{self.risk_level}] - Approval: {self.require_human_approval}"

class ConsentRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consent_records')
    purpose = models.CharField(max_length=100) # MARKETING, PERSONALIZATION, AI_PROCESSING, ANALYTICS, THIRD_PARTY_SHARING
    status = models.CharField(max_length=30, default='GRANTED') # GRANTED, REVOKED, EXPIRED
    version = models.CharField(max_length=30, default='1.0')
    granted_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Consent ({self.user.username}): {self.purpose} [{self.status}]"

class SecurityEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_events', null=True, blank=True)
    tenant_id = models.CharField(max_length=100, default='default_tenant')
    actor_id = models.CharField(max_length=100, blank=True, default='customer_user_01')
    actor_type = models.CharField(max_length=50, default='CUSTOMER') # HUMAN, CUSTOMER, ARTISAN, ADMIN, EMPLOYEE, AGENT, DEVICE, CONNECTOR, UNKNOWN
    event_type = models.CharField(max_length=100, default='LOGIN_ATTEMPT') # LOGIN_ATTEMPT, PAYMENT_INITIATED, AGENT_TOOL_CALL, PROMPT_SUBMITTED, DEVICE_TELEMETRY, REFUND_REQUEST, PROMO_REDEMPTION
    source = models.CharField(max_length=100, default='API_GATEWAY')
    ip_reference = models.CharField(max_length=50, default='198.51.100.44')
    device_reference = models.CharField(max_length=100, default='DEV_SIM_001')
    session_reference = models.CharField(max_length=100, default=uuid.uuid4)
    resource_type = models.CharField(max_length=100, default='ORDER')
    resource_id = models.CharField(max_length=100, default='ORD_9901')
    severity = models.CharField(max_length=30, default='MEDIUM') # LOW, MEDIUM, HIGH, CRITICAL
    confidence_score = models.FloatField(default=0.92)
    risk_signals_json = models.TextField(default='["unusual_ip", "new_device_context"]')
    details = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=30, default='PROCESSED') # PROCESSED, FLAGGED, ESCALATED, QUARANTINED
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Security Event: {self.event_type} [{self.severity}] - {self.status}"

class ModelRegistry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_name = models.CharField(max_length=100) # gemini-2.5-flash, gemini-2.5-pro, gpt-4o-secure
    provider = models.CharField(max_length=100, default='Google DeepMind')
    purpose = models.CharField(max_length=100, default='REASONING') # REASONING, CLASSIFICATION, PII_REDACTION, PLANNING
    privacy_level = models.CharField(max_length=50, default='HIGH') # HIGH, MEDIUM, PUBLIC
    approval_status = models.CharField(max_length=30, default='APPROVED') # APPROVED, UNDER_REVIEW, DEPRECATED
    version_pinned = models.CharField(max_length=50, default='2026-v1')

    def __str__(self):
        return f"Model: {self.model_name} ({self.provider}) [{self.approval_status}]"

class GovernanceControl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    control_code = models.CharField(max_length=50, unique=True) # AC-01, DP-02, AI-03, AU-04, SE-05
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default='Access Control') # Access Control, Data Protection, AI Governance, Audit Logging, Incident Response
    status = models.CharField(max_length=30, default='IMPLEMENTED') # IMPLEMENTED, PARTIAL, NEEDS_REVIEW
    evidence_summary = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Control {self.control_code}: {self.name} [{self.status}]"


# --- PROMPT #15 AI KNOWLEDGE FABRIC & ORGANIZATIONAL BRAIN MODELS ---

class KnowledgeSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_sources')
    name = models.CharField(max_length=255) # e.g. "Master Supplier Quality SOP 2026"
    source_type = models.CharField(max_length=100, default='SOP') # DOCUMENT, SOP, POLICY, CONTRACT, INVOICE, AUDIO, VIDEO, WEB_PAGE, SUPPLIER_DATA, AGENT_OUTPUT
    trust_level = models.CharField(max_length=50, default='VERIFIED') # AUTHORITATIVE, VERIFIED, INTERNAL, SECONDARY, UNVERIFIED, UNKNOWN
    classification = models.CharField(max_length=50, default='INTERNAL') # PUBLIC, INTERNAL, CONFIDENTIAL, SENSITIVE, HIGHLY_SENSITIVE
    owner = models.CharField(max_length=100, default='Operations Team')
    version = models.CharField(max_length=30, default='v1.0')
    freshness_status = models.CharField(max_length=30, default='FRESH') # FRESH, AGING, STALE, EXPIRED, UNKNOWN
    effective_from = models.DateTimeField(default=timezone.now)
    effective_until = models.DateTimeField(null=True, blank=True)
    uri_or_path = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Source: {self.name} ({self.source_type}) [{self.trust_level}]"

class KnowledgeObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(KnowledgeSource, on_delete=models.SET_NULL, null=True, blank=True, related_name='knowledge_objects')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_objects')
    title = models.CharField(max_length=255)
    knowledge_type = models.CharField(max_length=100, default='FACT') # FACT, POLICY, SOP, DECISION, INSIGHT, EVENT, RELATIONSHIP, RULE, PRODUCT_KNOWLEDGE, SUPPLIER_KNOWLEDGE, FINANCIAL_INSIGHT, AGENT_LEARNING
    content = models.TextField()
    summary = models.TextField(blank=True, default='')
    confidence_level = models.CharField(max_length=30, default='HIGH') # HIGH, MEDIUM, LOW, UNKNOWN
    freshness_status = models.CharField(max_length=30, default='FRESH') # FRESH, AGING, STALE, EXPIRED, UNKNOWN
    classification = models.CharField(max_length=50, default='INTERNAL') # PUBLIC, INTERNAL, CONFIDENTIAL, SENSITIVE
    version = models.CharField(max_length=30, default='v1.0')
    status = models.CharField(max_length=30, default='APPROVED') # APPROVED, DRAFT, UNDER_REVIEW, STALE, EXPIRED, ARCHIVED
    metadata = models.JSONField(default=dict, blank=True)
    effective_from = models.DateTimeField(default=timezone.now)
    effective_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Knowledge: {self.title} [{self.knowledge_type}] (Conf: {self.confidence_level})"

class KnowledgeGraphNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='graph_nodes')
    entity_type = models.CharField(max_length=100) # Customer, Product, Supplier, Creator, Campaign, Invoice, Payment, Organization, Agent, Document, Policy, SOP, Decision
    name = models.CharField(max_length=255)
    entity_id_ref = models.CharField(max_length=100, blank=True, default='') # Foreign key reference string if applicable
    attributes = models.JSONField(default=dict, blank=True)
    trust_level = models.CharField(max_length=50, default='VERIFIED') # AUTHORITATIVE, VERIFIED, INTERNAL, SECONDARY, UNVERIFIED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Node: {self.name} [{self.entity_type}]"

class KnowledgeGraphEdge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_node = models.ForeignKey(KnowledgeGraphNode, on_delete=models.CASCADE, related_name='outgoing_edges')
    target_node = models.ForeignKey(KnowledgeGraphNode, on_delete=models.CASCADE, related_name='incoming_edges')
    relationship = models.CharField(max_length=100) # BOUGHT, SUPPLIES, PROMOTED, BELONGS_TO, GENERATED, PAID, SETTLED, MENTIONS, GOVERNS, DEPENDS_ON, DERIVED_FROM, APPROVED_BY, USED_BY
    confidence = models.CharField(max_length=30, default='HIGH') # HIGH, MEDIUM, LOW
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edge: {self.source_node.name} --({self.relationship})--> {self.target_node.name}"

class DecisionMemory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decision_memories')
    title = models.CharField(max_length=255) # e.g. "Festival Campaign Creator Commission Strategy"
    category = models.CharField(max_length=100, default='CAMPAIGN_STRATEGY') # PRICING, SUPPLIER_SELECTION, CAMPAIGN_STRATEGY, COST_OPTIMIZATION, DISCOUNT_POLICY
    decision_summary = models.TextField()
    rationale_and_evidence = models.JSONField(default=dict, blank=True)
    approved_by = models.CharField(max_length=100, default='Business Manager')
    actual_outcome = models.TextField(blank=True, default='')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.92)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Decision: {self.title} [{self.category}]"

class KnowledgeConflictRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_conflicts')
    topic = models.CharField(max_length=255) # e.g. "Supplier Lead Time for Raw Silk"
    source_a_name = models.CharField(max_length=255)
    source_a_value = models.CharField(max_length=255)
    source_b_name = models.CharField(max_length=255)
    source_b_value = models.CharField(max_length=255)
    preferred_source = models.CharField(max_length=255)
    reason = models.TextField()
    status = models.CharField(max_length=30, default='DETECTED') # DETECTED, RESOLVED, UNDER_REVIEW
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conflict: {self.topic} [{self.status}]"

class KnowledgeGapRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_gaps')
    topic = models.CharField(max_length=255) # e.g. "Export Customs Duty Exemption for Handicrafts"
    demand_score = models.CharField(max_length=20, default='HIGH') # HIGH, MEDIUM, LOW
    current_coverage_pct = models.DecimalField(max_digits=5, decimal_places=2, default=35.00)
    recommended_action = models.TextField()
    assigned_owner = models.CharField(max_length=100, default='Compliance Specialist')
    status = models.CharField(max_length=30, default='OPEN') # OPEN, IN_PROGRESS, RESOLVED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Knowledge Gap: {self.topic} ({self.current_coverage_pct}%) [{self.status}]"


# --- PROMPT #16 AI DIGITAL TWIN, BUSINESS SIMULATION & STRATEGY LAB MODELS ---

class DigitalTwinSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='digital_twin_snapshots')
    snapshot_name = models.CharField(max_length=255, default='Live Business State Snapshot')
    snapshot_type = models.CharField(max_length=50, default='DAILY') # DAILY, WEEKLY, PRE_EXECUTION, POST_EXECUTION, BASELINE
    cash_position_inr = models.DecimalField(max_digits=12, decimal_places=2, default=184500.00)
    inventory_value_inr = models.DecimalField(max_digits=12, decimal_places=2, default=94200.00)
    active_orders_count = models.IntegerField(default=18)
    production_capacity_units = models.IntegerField(default=500)
    workforce_capacity_pct = models.DecimalField(max_digits=5, decimal_places=2, default=85.00)
    twin_health_score = models.IntegerField(default=94) # 0 to 100
    state_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Twin Snapshot: {self.snapshot_name} (Health: {self.twin_health_score}/100)"

class BusinessScenario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_scenarios')
    scenario_name = models.CharField(max_length=255) # e.g. "Diwali 10% Discount + Gift Bundle"
    category = models.CharField(max_length=100, default='CAMPAIGN') # PRICING, DISCOUNT, CAMPAIGN, B2B_BULK, SUPPLY_DISRUPTION, MARKET_ENTRY, STRESS_TEST
    baseline_snapshot = models.ForeignKey(DigitalTwinSnapshot, on_delete=models.SET_NULL, null=True, blank=True, related_name='scenarios')
    parameters = models.JSONField(default=dict, blank=True) # e.g. {"price_change_pct": -10, "gift_bundle_cost_inr": 150, "demand_uplift_pct": 35}
    duration_days = models.IntegerField(default=30)
    status = models.CharField(max_length=30, default='DRAFT') # DRAFT, SIMULATED, APPROVED, EXECUTING, COMPLETED, ARCHIVED
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scenario: {self.scenario_name} [{self.category}] - {self.status}"

class SimulationResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scenario = models.OneToOneField(BusinessScenario, on_delete=models.CASCADE, related_name='simulation_result')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulation_results')
    projected_revenue_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    revenue_delta_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    projected_margin_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    margin_delta_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    projected_cash_impact_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    inventory_delta_units = models.IntegerField(default=0)
    risk_level = models.CharField(max_length=20, default='LOW') # LOW, MEDIUM, HIGH, CRITICAL
    strategic_score = models.IntegerField(default=82) # 0 to 100
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.88)
    sensitivity_drivers = models.JSONField(default=list, blank=True)
    assumptions_summary = models.JSONField(default=list, blank=True)
    uncertainties = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sim Result: {self.scenario.scenario_name} (Rev Delta: ₹{self.revenue_delta_inr}, Risk: {self.risk_level})"

class StrategyCouncilReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scenario = models.ForeignKey(BusinessScenario, on_delete=models.CASCADE, related_name='council_reviews')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='council_reviews')
    finance_agent_perspective = models.TextField(blank=True, default='')
    growth_agent_perspective = models.TextField(blank=True, default='')
    supply_agent_perspective = models.TextField(blank=True, default='')
    risk_agent_perspective = models.TextField(blank=True, default='')
    consensus_recommendation = models.TextField()
    reversibility = models.CharField(max_length=30, default='REVERSIBLE') # REVERSIBLE, PARTIALLY_REVERSIBLE, IRREVERSIBLE
    requires_human_approval = models.BooleanField(default=True)
    approval_status = models.CharField(max_length=30, default='PENDING') # PENDING, APPROVED, REJECTED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Council Review: {self.scenario.scenario_name} [{self.approval_status}]"

class ScenarioCalibration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scenario = models.ForeignKey(BusinessScenario, on_delete=models.CASCADE, related_name='calibrations')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scenario_calibrations')
    predicted_revenue_inr = models.DecimalField(max_digits=12, decimal_places=2)
    actual_revenue_inr = models.DecimalField(max_digits=12, decimal_places=2)
    forecast_error_pct = models.DecimalField(max_digits=5, decimal_places=2)
    calibration_notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calibration ({self.scenario.scenario_name}): Error {self.forecast_error_pct}%"


# --- PROMPT #18 AI CAUSAL INTELLIGENCE, EXPERIMENTATION & OUTCOME LEARNING OS MODELS ---

class CausalRelationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='causal_relationships')
    cause_node = models.CharField(max_length=255) # e.g. "Diwali Festival", "10% Discount", "Product Image Upgrade"
    effect_node = models.CharField(max_length=255) # e.g. "Conversion Rate", "Average Order Value", "Contribution Margin"
    relationship_type = models.CharField(max_length=50, default='INFLUENCES') # CAUSES, INFLUENCES, CORRELATES_WITH, DEPENDS_ON, MEDIATES, CONFOUNDS, UNKNOWN
    evidence_level = models.CharField(max_length=50, default='E2_OBSERVATIONAL') # E0_NO_EVIDENCE, E1_AI_HYPOTHESIS, E2_OBSERVATIONAL, E3_BEFORE_AFTER, E4_QUASI_EXP, E5_CONTROLLED_EXP
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.75)
    estimated_effect_size = models.CharField(max_length=255, default='+12.4% Lift')
    context_payload = models.JSONField(default=dict, blank=True)
    last_validated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Causal Edge: {self.cause_node} --[{self.relationship_type}]--> {self.effect_node} ({self.evidence_level})"

class BusinessHypothesis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_hypotheses')
    title = models.CharField(max_length=255) # e.g. "Handicraft Bundling Increases Average Order Value"
    treatment_variable = models.CharField(max_length=255) # e.g. "Gift Set Bundle"
    outcome_variable = models.CharField(max_length=255) # e.g. "Average Order Value"
    predicted_direction = models.CharField(max_length=20, default='INCREASE') # INCREASE, DECREASE, NEUTRAL
    rationale = models.TextField()
    prior_confidence = models.DecimalField(max_digits=5, decimal_places=2, default=0.65)
    impact_score = models.IntegerField(default=85) # 0 to 100
    status = models.CharField(max_length=30, default='PROPOSED') # PROPOSED, PRIORITIZED, TESTING, VALIDATED, REJECTED, ARCHIVED
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Hypothesis: {self.title} [{self.status}]"

class CausalExperiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='causal_experiments')
    hypothesis = models.ForeignKey(BusinessHypothesis, on_delete=models.SET_NULL, null=True, blank=True, related_name='experiments')
    title = models.CharField(max_length=255) # e.g. "Diwali 10% Discount vs Gift Bundle A/B Test"
    experiment_type = models.CharField(max_length=50, default='AB_TEST') # AB_TEST, HOLDOUT, BEFORE_AFTER, MULTIVARIATE, SEQUENTIAL
    treatment_definition = models.JSONField(default=dict, blank=True)
    control_definition = models.JSONField(default=dict, blank=True)
    target_population = models.CharField(max_length=255, default='Eligible Returning Customers')
    primary_metric = models.CharField(max_length=100, default='Conversion Rate')
    secondary_metrics = models.JSONField(default=list, blank=True)
    guardrail_metrics = models.JSONField(default=dict, blank=True)
    sample_size_treatment = models.IntegerField(default=500)
    sample_size_control = models.IntegerField(default=500)
    status = models.CharField(max_length=30, default='DRAFT') # DRAFT, PENDING_APPROVAL, APPROVED, RUNNING, PAUSED, STOPPED, COMPLETED, ANALYZED
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Experiment: {self.title} [{self.experiment_type}] - {self.status}"

class ExperimentResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experiment = models.OneToOneField(CausalExperiment, on_delete=models.CASCADE, related_name='result')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiment_results')
    control_metric_value = models.DecimalField(max_digits=10, decimal_places=4, default=4.2000)
    treatment_metric_value = models.DecimalField(max_digits=10, decimal_places=4, default=4.8000)
    absolute_lift = models.DecimalField(max_digits=10, decimal_places=4, default=0.6000)
    relative_lift_pct = models.DecimalField(max_digits=7, decimal_places=2, default=14.29)
    confidence_interval_low = models.DecimalField(max_digits=7, decimal_places=2, default=3.10)
    confidence_interval_high = models.DecimalField(max_digits=7, decimal_places=2, default=12.50)
    p_value = models.DecimalField(max_digits=6, decimal_places=4, default=0.0240)
    bayesian_win_probability = models.DecimalField(max_digits=5, decimal_places=2, default=0.94)
    incremental_revenue_inr = models.DecimalField(max_digits=12, decimal_places=2, default=18500.00)
    guardrails_passed = models.BooleanField(default=True)
    evidence_level = models.CharField(max_length=50, default='E5_CONTROLLED_EXP')
    analysis_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exp Result ({self.experiment.title}): Lift +{self.relative_lift_pct}% (E-Level: {self.evidence_level})"

class OutcomeLearning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outcome_learnings')
    experiment = models.ForeignKey(CausalExperiment, on_delete=models.SET_NULL, null=True, blank=True, related_name='learnings')
    title = models.CharField(max_length=255) # e.g. "10% Bundle Increases Contribution Margin for Returning Customers"
    learning_summary = models.TextField()
    context_constraints = models.JSONField(default=dict, blank=True)
    evidence_level = models.CharField(max_length=50, default='E5_CONTROLLED_EXP')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.90)
    is_stale = models.BooleanField(default=False)
    valid_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Learning: {self.title} ({self.evidence_level}) [Confidence: {self.confidence_score}]"

class BusinessUnknown(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_unknowns')
    question = models.CharField(max_length=255) # e.g. "Will customers pay ₹999 for premium gift packaging?"
    business_impact = models.CharField(max_length=20, default='HIGH') # HIGH, MEDIUM, LOW
    cost_to_learn = models.CharField(max_length=20, default='LOW') # LOW, MEDIUM, HIGH
    value_of_information_score = models.IntegerField(default=88) # 0 to 100
    recommended_experiment = models.TextField()
    status = models.CharField(max_length=30, default='OPEN') # OPEN, EXPERIMENTING, RESOLVED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Unknown: {self.question} (VOI Score: {self.value_of_information_score}) [{self.status}]"


# --- PROMPT #19 AI MARKET INTELLIGENCE, COMPETITIVE INTELLIGENCE & OPPORTUNITY DISCOVERY OS MODELS ---

class IntelligenceSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='intelligence_sources')
    name = models.CharField(max_length=255) # e.g. "ONDC Open Catalog Index", "Etsy Handicrafts Trends RSS"
    source_type = models.CharField(max_length=50, default='OFFICIAL_API') # OFFICIAL_API, PUBLIC_WEBSITE, MARKETPLACE_CATALOG, GOVERNMENT_DATA, SOCIAL_SIGNAL
    url_identifier = models.CharField(max_length=500, blank=True, default='')
    authority_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.90)
    reliability_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.88)
    freshness_status = models.CharField(max_length=30, default='FRESH') # FRESH, STALE, NEEDS_REFRESH
    last_checked = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Intel Source: {self.name} [{self.source_type}] (Auth: {self.authority_score})"

class CompetitorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competitor_profiles')
    name = models.CharField(max_length=255) # e.g. "Royal Jaipur Pottery Co", "Silk Craft India"
    competitor_type = models.CharField(max_length=50, default='DIRECT') # DIRECT, INDIRECT, EMERGING, SUBSTITUTE
    category = models.CharField(max_length=100, default='Pottery & Handicrafts')
    observed_pricing_range = models.CharField(max_length=100, default='₹999 - ₹2,499')
    market_positioning = models.CharField(max_length=255, default='Mass Premium Craft Decor')
    observed_channels = models.JSONField(default=list, blank=True)
    last_observed_move = models.TextField(blank=True, default='Reduced Jaipur Pottery Vase price by 12% for festive promotion.')
    last_observed_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Competitor: {self.name} [{self.competitor_type}] ({self.category})"

class MarketTrend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='market_trends')
    title = models.CharField(max_length=255) # e.g. "Surge in Demand for Eco-Friendly Terracotta & Blue Pottery Decor"
    category = models.CharField(max_length=100, default='Home & Living')
    trend_status = models.CharField(max_length=30, default='GROWING') # EMERGING, GROWING, MAINSTREAM, MATURE, DECLINING
    velocity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.82)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.88)
    evidence_sources_count = models.IntegerField(default=4)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trend: {self.title} [{self.trend_status}] (Velocity: {self.velocity_score})"

class MarketOpportunity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='market_opportunities')
    title = models.CharField(max_length=255) # e.g. "Personalized Festive Blue Pottery Gift Boxes"
    category = models.CharField(max_length=50, default='PRODUCT') # PRODUCT, MARKET, CHANNEL, CREATOR, B2B, EXPORT, SUPPLY
    urgency = models.CharField(max_length=30, default='IMMEDIATE') # IMMEDIATE, NEAR_TERM, STRATEGIC
    opportunity_score = models.IntegerField(default=88) # 0 to 100
    estimated_revenue_potential_inr = models.DecimalField(max_digits=12, decimal_places=2, default=125000.00)
    required_resources = models.TextField(blank=True, default='Existing pottery workshop capacity + ₹5,000 custom packaging.')
    why_now_reason = models.TextField(blank=True, default='Festive corporate gifting demand surged +35% with low competitor personalization.')
    opportunity_window_months = models.IntegerField(default=3)
    status = models.CharField(max_length=30, default='DETECTED') # DETECTED, VALIDATED, SCORED, SIMULATED, EXECUTING, COMPLETED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Opportunity: {self.title} (Score: {self.opportunity_score}) [{self.status}]"

class MarketThreat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='market_threats')
    title = models.CharField(max_length=255) # e.g. "Competitor Price Drop (-15%) on Jaipur Pottery Vases"
    threat_type = models.CharField(max_length=50, default='COMPETITOR_PRICING') # COMPETITOR_PRICING, SUPPLY_SHORTAGE, DEMAND_DECLINE, REGULATORY_CHANGE
    severity = models.CharField(max_length=20, default='MEDIUM') # LOW, MEDIUM, HIGH, CRITICAL
    impact_description = models.TextField()
    recommended_defensive_strategy = models.TextField()
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, MITIGATED, MONITORING
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Threat: {self.title} [{self.severity}] - {self.status}"


# ==========================================
# MEGA PROMPT #20: AI NETWORK INTELLIGENCE & COLLECTIVE COMMERCE GRAPH OS
# ==========================================

class NetworkEntityGraphNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_nodes')
    entity_id = models.CharField(max_length=100, unique=True)
    entity_name = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=50, default='ARTISAN') # ARTISAN, CUSTOMER, SUPPLIER, B2B_BUYER, RETAILER, WHOLESALER, CREATOR, MARKETPLACE, LOGISTICS, AI_AGENT
    verification_status = models.CharField(max_length=30, default='VERIFIED') # UNVERIFIED, PENDING, VERIFIED, ENTERPRISE
    location_region = models.CharField(max_length=100, default='Jaipur, Rajasthan, India')
    capabilities = models.TextField(blank=True, default='Blue Pottery, Handcrafting, Direct B2B Fulfillment')
    trust_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.92) # 0.0 to 1.0
    privacy_consent_level = models.CharField(max_length=30, default='OPT_IN_AGGREGATE') # ANONYMOUS, OPT_IN_AGGREGATE, SHARED_PARTNER, FULL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"NetworkNode: {self.entity_name} [{self.entity_type}] - {self.location_region}"


class NetworkRelationshipEdge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_edges')
    source_node = models.ForeignKey(NetworkEntityGraphNode, on_delete=models.CASCADE, related_name='outgoing_edges')
    target_node = models.ForeignKey(NetworkEntityGraphNode, on_delete=models.CASCADE, related_name='incoming_edges')
    relationship_type = models.CharField(max_length=50, default='SUPPLIES') # SELLS, BUYS, SUPPLIES, PRODUCES, CREATES, PROMOTES, SHIPS, WORKS_WITH, ORDERS_FROM, MATCHED_WITH
    strength_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.85)
    is_active = models.BooleanField(default=True)
    metadata_info = models.TextField(blank=True, default='Active procurement & fulfillment edge')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edge: {self.source_node.entity_name} --[{self.relationship_type}]--> {self.target_node.entity_name}"


class NetworkSignalMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_signals')
    signal_type = models.CharField(max_length=50, default='DEMAND_SURGE') # DEMAND_SURGE, CAPACITY_SURPLUS, SUPPLY_SHORTAGE, BOTTLENECK, PRICE_SHIFT, LOGISTICS_DELAY
    source_category = models.CharField(max_length=100, default='B2B_RFQ_AGGREGATION')
    category = models.CharField(max_length=100, default='Handicrafts & Decor')
    location_scope = models.CharField(max_length=100, default='Northern India Region')
    confidence = models.DecimalField(max_digits=5, decimal_places=2, default=0.91)
    privacy_level = models.CharField(max_length=30, default='AGGREGATED_ANONYMOUS')
    payload_json = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signal: {self.signal_type} [{self.category}] - Confidence: {self.confidence}"


class NetworkDemandPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_demand_pools')
    pool_name = models.CharField(max_length=255) # e.g. "Diwali Festive Corporate Gift Sets Pool"
    product_category = models.CharField(max_length=100, default='Ceramics & Decor')
    aggregated_units = models.IntegerField(default=1100)
    participating_buyers_count = models.IntegerField(default=4)
    target_delivery_days = models.IntegerField(default=25)
    target_unit_price_inr = models.DecimalField(max_digits=10, decimal_places=2, default=450.00)
    feasibility_status = models.CharField(max_length=30, default='FEASIBLE') # FEASIBLE, IN_MATCHING, COMMITTED, FULFILLED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DemandPool: {self.pool_name} ({self.aggregated_units} units) [{self.feasibility_status}]"


class NetworkCapacityResource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_capacities')
    cluster_name = models.CharField(max_length=255) # e.g. "Jaipur Artisan Cooperative Cluster"
    resource_type = models.CharField(max_length=50, default='PRODUCTION') # PRODUCTION, PACKAGING, STORAGE, SHIPPING, PHOTOGRAPHY
    available_units_per_week = models.IntegerField(default=1000)
    utilization_rate_pct = models.DecimalField(max_digits=5, decimal_places=2, default=45.00)
    location_region = models.CharField(max_length=100, default='Jaipur, Rajasthan')
    is_available_for_pooling = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Capacity: {self.cluster_name} - {self.available_units_per_week} units/wk [{self.resource_type}]"


class NetworkEcosystemOpportunity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_opportunities')
    title = models.CharField(max_length=255) # e.g. "Regional Sustainable Corporate Gifting Network Cluster"
    opportunity_type = models.CharField(max_length=50, default='GROUP_PROCUREMENT') # GROUP_PROCUREMENT, DEMAND_POOLING, REGIONAL_CLUSTER, LOGISTICS_CONSOLIDATION, CREATOR_MATCH
    match_score = models.IntegerField(default=92) # 0 to 100
    estimated_economic_value_inr = models.DecimalField(max_digits=12, decimal_places=2, default=495000.00)
    participating_nodes_summary = models.TextField(blank=True, default='18 Artisans + 3 Raw Material Suppliers + 2 Logistics Networks')
    why_now_reason = models.TextField(blank=True, default='High B2B buyer demand pool aligned with 55% unused artisan pottery capacity.')
    status = models.CharField(max_length=30, default='OPEN') # OPEN, MATCHED, NEGOTIATING, EXECUTING, FULFILLED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"EcosystemOpp: {self.title} (Match: {self.match_score}%) [{self.status}]"


class NetworkMultiPartyMatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_matches')
    match_title = models.CharField(max_length=255) # e.g. "5,000 Unit B2B Gift Set Multi-Party Fulfillment Plan"
    match_score = models.IntegerField(default=95)
    matched_buyers_summary = models.CharField(max_length=255, default='4 Corporate B2B Buyers (Pooled Demand: 5,000 units)')
    matched_artisans_summary = models.CharField(max_length=255, default='Jaipur Artisan Cluster (25 Artisans, 5,600 units capacity)')
    matched_suppliers_summary = models.CharField(max_length=255, default='Silk Craft Dyes & Terracotta Clay Supplies')
    matched_logistics_summary = models.CharField(max_length=255, default='Express Logistics Regional Network')
    status = models.CharField(max_length=30, default='RECOMMENDED') # RECOMMENDED, APPROVED, EXECUTING, FULFILLED
    provenance_receipt = models.TextField(blank=True, default='Verified deterministic constraint solver + trust policy validation')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match: {self.match_title} (Score: {self.match_score}%) [{self.status}]"


# ==========================================
# MEGA PROMPT #21: AI CUSTOMER 360 & PERSONAL COMMERCE OS
# ==========================================

class CustomerPreferenceProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_360_profiles')
    preferred_categories = models.CharField(max_length=255, default='Ceramics & Decor, Home Living, Festive Gifts')
    preferred_price_min_inr = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    preferred_price_max_inr = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00)
    preferred_materials = models.CharField(max_length=255, default='Organic Terracotta, Cobalt Blue Glaze, Silk')
    preferred_languages = models.CharField(max_length=100, default='Hindi, English')
    gift_intent_frequency = models.CharField(max_length=50, default='HIGH') # LOW, MEDIUM, HIGH
    inferred_style = models.CharField(max_length=100, default='Authentic Traditional & Modern Heritage')
    privacy_mode = models.CharField(max_length=30, default='STANDARD') # STANDARD, MINIMAL, PRIVATE, NO_AI_PERSONALIZATION
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer360Profile: {self.customer.username} [{self.privacy_mode}]"


class CustomerCommerceMemory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_memories')
    memory_type = models.CharField(max_length=50, default='EXPLICIT_PREFERENCE') # EXPLICIT_PREFERENCE, BEHAVIORAL_INSIGHT, INFERRED_STYLE, REPEAT_INTENT
    memory_key = models.CharField(max_length=100, default='festive_eco_gift_preference')
    memory_value = models.TextField(default='Customer prefers eco-friendly handmade gifts under ₹2,000 for festival occasions.')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.94)
    provenance_source = models.CharField(max_length=100, default='USER_EXPLICIT_INPUT') # USER_EXPLICIT_INPUT, SEARCH_HISTORY, ORDER_HISTORY
    is_editable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CustomerMemory: {self.customer.username} - {self.memory_key} (Score: {self.confidence_score})"


class ShoppingSessionIntent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_intents')
    raw_query = models.TextField(default='Mujhe 2000 ke andar sister ke birthday ke liye handmade unique gift chahiye.')
    intent_type = models.CharField(max_length=50, default='GIFT_SHOPPING') # BROWSING, GIFT_SHOPPING, URGENT_PURCHASE, RESEARCH, COMPARISON, FESTIVAL_SHOPPING
    extracted_category = models.CharField(max_length=100, default='Handmade Gift Sets')
    budget_max_inr = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)
    target_delivery_days = models.IntegerField(default=5)
    recipient_type = models.CharField(max_length=50, default='Sister')
    occasion = models.CharField(max_length=50, default='Birthday')
    extracted_constraints_json = models.TextField(default='{"style": "unique", "material": "handmade ceramic/clay"}')
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, SHORTLISTED, CARTED, CHECKED_OUT, EXPIRED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Intent: {self.customer.username} [{self.intent_type}] - ₹{self.budget_max_inr}"


class CustomerShortlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_shortlists')
    shortlist_name = models.CharField(max_length=255, default='Birthday Gift Shortlist')
    intent = models.ForeignKey(ShoppingSessionIntent, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shortlisted_by')
    personal_fit_score = models.IntegerField(default=94) # 0 to 100
    fit_explanation = models.TextField(default='Handmade authentic terracotta vase within your ₹2,000 budget with 4-day express delivery.')
    tradeoffs_summary = models.TextField(default='Fragile material requires standard craft packaging; high customer rating (4.9/5).')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shortlist: {self.customer.username} - {self.product.title} (Fit: {self.personal_fit_score}%)"


class CustomerConsentPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_consents')
    allow_personalization = models.BooleanField(default=True)
    allow_ai_memory = models.BooleanField(default=True)
    allow_recommendations = models.BooleanField(default=True)
    allow_behavioral_analytics = models.BooleanField(default=True)
    allow_voice_vision_search = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CustomerConsent: {self.customer.username} [Personalization: {self.allow_personalization}]"


# --- MEGA PROMPT #22: AI OMNICHANNEL, PHYGITAL COMMERCE & PHYSICAL WORLD INTELLIGENCE OS MODELS ---

class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stores')
    name = models.CharField(max_length=255)
    store_type = models.CharField(max_length=50, default='PERMANENT') # PERMANENT, POP_UP, EXHIBITION, WORKSHOP, KIOSK, PARTNER
    address = models.TextField(default='Main Artisan Hub, Craft Lane')
    city = models.CharField(max_length=100, default='Jaipur')
    region = models.CharField(max_length=100, default='Rajasthan')
    contact_phone = models.CharField(max_length=50, default='+91 98765 43210')
    operating_hours = models.CharField(max_length=100, default='10:00 AM - 08:00 PM IST')
    is_active = models.BooleanField(default=True)
    capabilities_json = models.TextField(default='{"pickup": true, "qr_enabled": true, "kiosk_enabled": true, "staff_copilot": true}')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Store: {self.name} ({self.city}) [{self.store_type}]"


class StoreInventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inventories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_inventories')
    quantity_available = models.IntegerField(default=15)
    quantity_reserved = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=3)
    last_synced_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"StoreInventory: {self.store.name} - {self.product.title} (Stock: {self.quantity_available})"


class OmnichannelSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='omnichannel_sessions')
    channel = models.CharField(max_length=50, default='WEB') # WEB, MOBILE, WHATSAPP, QR, STORE, KIOSK, VOICE, SOCIAL, B2B
    current_store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    session_token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    context_json = models.TextField(default='{"active_intent": "Browsing", "last_qr_scanned": null}')

    def __str__(self):
        return f"OmniSession: {self.customer.username} [{self.channel}]"


class QRAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code_key = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    qr_type = models.CharField(max_length=50, default='PRODUCT_QR') # PRODUCT_QR, TABLE_QR, STORE_QR, PICKUP_QR, EVENT_QR
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    resolution_target_url = models.URLField(default='https://artisancommerce.os/qr/resolve')
    scans_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR: {self.qr_type} ({self.qr_code_key[:8]}) [Scans: {self.scans_count}]"


class KioskSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='kiosk_sessions')
    kiosk_device_id = models.CharField(max_length=100, default='KIOSK_JAIPUR_01')
    active_customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, TRANSFERRED, COMPLETED, EXPIRED
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KioskSession: {self.kiosk_device_id} [{self.status}]"


class PickupReservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickup_reservations')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='pickup_reservations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    pickup_code = models.CharField(max_length=20, default='PICKUP-9821')
    status = models.CharField(max_length=30, default='RESERVED') # RESERVED, READY_FOR_PICKUP, COMPLETED, CANCELLED
    reserved_at = models.DateTimeField(auto_now_add=True)
    pickup_window_end = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Pickup: {self.pickup_code} - {self.store.name} [{self.status}]"


class ExhibitionEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='National Heritage Handloom & Craft Expo')
    event_type = models.CharField(max_length=50, default='CRAFT_FAIR') # CRAFT_FAIR, TRADE_SHOW, POPUP_MARKET, FESTIVAL
    city = models.CharField(max_length=100, default='New Delhi')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    participating_artisans_json = models.TextField(default='["artisan_1", "artisan_2"]')
    status = models.CharField(max_length=30, default='ACTIVE') # SCHEDULED, ACTIVE, ENDED

    def __str__(self):
        return f"Exhibition: {self.name} ({self.city}) [{self.status}]"


class OfflineSyncQueue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=100, default='MOBILE_DEVICE_77')
    event_type = models.CharField(max_length=50, default='OFFLINE_QR_SCAN') # OFFLINE_QR_SCAN, OFFLINE_CART_ADD, OFFLINE_ORDER_DRAFT
    payload_json = models.TextField(default='{}')
    status = models.CharField(max_length=30, default='PENDING') # PENDING, SYNCED, CONFLICT_RESOLVED, FAILED
    idempotency_key = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OfflineSync: {self.event_type} [{self.status}]"


# --- MEGA PROMPT #23: AI EDGE COMMERCE, SMART STORE, IOT & PHYSICAL INTELLIGENCE OS MODELS ---

class PhysicalDevice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    organization = models.ForeignKey(User, on_delete=models.CASCADE, related_name='physical_devices')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='devices')
    device_type = models.CharField(max_length=50, default='SCANNER') # POS, SCANNER, PRINTER, KIOSK, SMART_SHELF, INVENTORY_SENSOR, GATEWAY, PACKING_STATION
    manufacturer = models.CharField(max_length=100, default='Zebra Technologies')
    model_name = models.CharField(max_length=100, default='DS2208 Handheld Scanner')
    firmware_version = models.CharField(max_length=50, default='v2.4.1')
    status = models.CharField(max_length=30, default='ONLINE') # ONLINE, DEGRADED, OFFLINE, MAINTENANCE
    trust_level = models.CharField(max_length=30, default='HIGH') # HIGH, MEDIUM, LOW, REVOKED
    capabilities_json = models.TextField(default='["scanner", "barcode_reader"]')
    health_score = models.IntegerField(default=95) # 0 to 100
    last_seen = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Device: {self.device_type} ({self.device_id[:12]}) [{self.status}]"


class EdgeGateway(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gateway_code = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='edge_gateways')
    status = models.CharField(max_length=30, default='ONLINE') # ONLINE, OFFLINE, SYNCING
    local_queue_count = models.IntegerField(default=0)
    last_sync_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Gateway: {self.gateway_code[:8]} - {self.store.name} [{self.status}]"


class DeviceEventTelemetry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(PhysicalDevice, on_delete=models.CASCADE, related_name='telemetry_events')
    event_type = models.CharField(max_length=50, default='ScanReceived') # DeviceConnected, ScanReceived, InventorySignalReceived, POSTransaction, ShelfMovement, DeviceError
    payload_json = models.TextField(default='{}')
    confidence_score = models.FloatField(default=0.95)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Telemetry: {self.device.device_type} - {self.event_type} [{self.confidence_score}]"


class DeviceCommandLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(PhysicalDevice, on_delete=models.CASCADE, related_name='command_logs')
    agent_id = models.CharField(max_length=100, default='physical_ops_agent_01')
    command_name = models.CharField(max_length=100, default='display_product')
    parameters_json = models.TextField(default='{}')
    risk_level = models.CharField(max_length=30, default='LOW') # LOW, MEDIUM, HIGH
    approval_status = models.CharField(max_length=30, default='APPROVED') # APPROVED, DENIED, PENDING
    execution_result_json = models.TextField(default='{"status": "SUCCESS"}')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Command: {self.command_name} -> {self.device.device_type} [{self.approval_status}]"


class SensorInventorySignal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(PhysicalDevice, on_delete=models.CASCADE, related_name='sensor_signals')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    detected_quantity = models.IntegerField(default=14)
    previous_quantity = models.IntegerField(default=15)
    confidence_score = models.FloatField(default=0.92)
    calibration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"SensorSignal: {self.product.title} Qty: {self.detected_quantity} (Conf: {self.confidence_score})"


class InventoryReconciliationReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reconciliations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pos_count = models.IntegerField(default=18)
    system_count = models.IntegerField(default=15)
    sensor_count = models.IntegerField(default=17)
    confidence_score = models.FloatField(default=0.88)
    discrepancy_reason = models.TextField(default='Possible un-scanned POS return or misplaced shelf stock.')
    recommended_action = models.TextField(default='Schedule physical audit task for Shelf 3 and adjust system inventory count to 17.')
    status = models.CharField(max_length=30, default='OPEN') # OPEN, RECONCILED, ESCALATED_TO_STAFF
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reconciliation: {self.product.title} - POS:{self.pos_count}/SYS:{self.system_count}/SNS:{self.sensor_count} [{self.status}]"


class PhysicalStoreTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    task_type = models.CharField(max_length=50, default='SHELF_RESTOCK') # SHELF_RESTOCK, DEVICE_MAINTENANCE, INVENTORY_VERIFY, PICKUP_PREPARE
    title = models.CharField(max_length=255, default='Restock Terracotta Lamp on Shelf 2')
    description = models.TextField(default='Smart shelf sensor detected stock level below 4 units. Restock 10 units from Jaipur backroom.')
    priority = models.CharField(max_length=30, default='HIGH') # LOW, MEDIUM, HIGH, URGENT
    status = models.CharField(max_length=30, default='PENDING') # PENDING, IN_PROGRESS, COMPLETED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"StoreTask: {self.title} [{self.priority}] - {self.status}"


# --- MEGA PROMPT #24: AI SECURITY, CYBER DEFENSE & FRAUD/RISK INTELLIGENCE OS MODELS ---


class SecurityIncident(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='Suspicious Payment Velocity & New Device Context')
    category = models.CharField(max_length=100, default='PAYMENT_FRAUD') # PAYMENT_FRAUD, ACCOUNT_TAKEOVER, PROMPT_INJECTION, AGENT_ABUSE, DEVICE_COMPROMISE, MARKETPLACE_MANIPULATION, REFUND_ABUSE
    severity = models.CharField(max_length=30, default='HIGH') # LOW, MEDIUM, HIGH, CRITICAL
    status = models.CharField(max_length=30, default='OPEN') # OPEN, INVESTIGATING, CONTAINED, RESOLVED, FALSE_POSITIVE
    affected_actor_id = models.CharField(max_length=100, default='customer_user_01')
    risk_score = models.IntegerField(default=85) # 0-100
    confidence_score = models.FloatField(default=0.94)
    evidence_summary = models.TextField(default='Rapid 4 orders within 90 seconds from unrecognized IP reference.')
    recommended_containment = models.TextField(default='Require Step-Up 2FA verification and temporarily freeze auto-payout.')
    containment_status = models.CharField(max_length=50, default='STEP_UP_VERIFICATION_REQUIRED')
    detected_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"SecurityIncident: {self.title} [{self.severity}] - {self.status}"


class SecurityPolicyRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rule_code = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, default='High Value Payment Step-Up Verification Policy')
    category = models.CharField(max_length=100, default='PAYMENT_RISK') # PAYMENT_RISK, AGENT_FIREWALL, PROMPT_SAFETY, DEVICE_TRUST, BOT_DEFENSE
    actor_scope = models.CharField(max_length=50, default='ALL')
    risk_threshold = models.IntegerField(default=75) # Risk score >= threshold triggers effect
    effect = models.CharField(max_length=30, default='CHALLENGE') # ALLOW, CHALLENGE, STEP_UP_VERIFICATION, REQUIRE_HUMAN_APPROVAL, QUARANTINE, BLOCK
    conditions_json = models.TextField(default='{"transaction_amount_gt": 10000, "new_device": true}')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PolicyRule: {self.name} -> {self.effect} [Risk >= {self.risk_threshold}]"


class ThreatIndicator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    indicator_value = models.CharField(max_length=255, default='198.51.100.44')
    indicator_type = models.CharField(max_length=50, default='IP_ADDRESS') # IP_ADDRESS, DEVICE_FINGERPRINT, PROMPT_SIGNATURE, BAD_DOMAINS
    category = models.CharField(max_length=100, default='BOTNET_ANOMALY')
    confidence_score = models.FloatField(default=0.88)
    first_seen = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"ThreatIndicator: {self.indicator_type} ({self.indicator_value}) [Conf: {self.confidence_score}]"


class AgentSecurityProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_id = models.CharField(max_length=100, unique=True, default='catalog_agent_01')
    autonomy_level = models.IntegerField(default=2) # Level 0 to 4
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, SUSPICIOUS, QUARANTINED, REJECTED
    allowed_tools_json = models.TextField(default='["update_catalog", "read_inventory"]')
    max_tool_calls_per_minute = models.IntegerField(default=30)
    prompt_injection_shield_active = models.BooleanField(default=True)
    last_security_audit = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"AgentSecurity: {self.agent_id} [Status: {self.status}] (Autonomy L{self.autonomy_level})"


# --- MEGA PROMPT #25: AI RESILIENCE, DISASTER RECOVERY & SELF-HEALING OS MODELS ---

class ServiceHealthRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_name = models.CharField(max_length=100, default='Commerce API Gateway')
    category = models.CharField(max_length=50, default='API') # API, FINANCE, AI, EDGE, KNOWLEDGE, SIMULATION, DATABASE
    status = models.CharField(max_length=30, default='HEALTHY') # HEALTHY, DEGRADED, UNAVAILABLE
    latency_ms = models.IntegerField(default=14)
    error_rate_pct = models.FloatField(default=0.01)
    criticality = models.CharField(max_length=20, default='CRITICAL') # CRITICAL, HIGH, MEDIUM, LOW
    rto_minutes = models.IntegerField(default=1)
    rpo_minutes = models.IntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ServiceHealth: {self.service_name} [{self.status}] - Latency: {self.latency_ms}ms"


class FailureEventRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.CharField(max_length=100, default='default_tenant')
    service = models.CharField(max_length=100, default='Unified Ledger & Payments')
    failure_type = models.CharField(max_length=100, default='PAYMENT_PROVIDER_TIMEOUT') # APPLICATION, DATABASE, AI_PROVIDER, PAYMENT, LOGISTICS, DEVICE
    severity = models.CharField(max_length=30, default='HIGH') # LOW, MEDIUM, HIGH, CRITICAL
    symptoms = models.TextField(default='Provider timeout after 5000ms')
    affected_resources_json = models.TextField(default='["ORD_9901"]')
    status = models.CharField(max_length=30, default='FLAGGED') # FLAGGED, CONTAINED, RECOVERED, IGNORED
    detected_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"FailureEvent: {self.failure_type} in {self.service} [{self.severity}]"


class OperationalIncident(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='Resilience Incident: Payment Provider Timeout')
    category = models.CharField(max_length=50, default='PAYMENT') # SECURITY, AVAILABILITY, PERFORMANCE, DATA, DEPENDENCY, AI, COMMERCE, PAYMENT, DEVICE
    severity = models.CharField(max_length=30, default='HIGH')
    status = models.CharField(max_length=30, default='INVESTIGATING') # INVESTIGATING, CONTAINED, RECOVERED, RESOLVED
    affected_service = models.CharField(max_length=100, default='Unified Ledger & Payments')
    impact_summary = models.TextField(default='Primary payment gateway timed out.')
    rto_target_minutes = models.IntegerField(default=2)
    rpo_target_minutes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"OperationalIncident: {self.title} [{self.status}]"


class RecoveryPlanRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(OperationalIncident, on_delete=models.CASCADE, related_name='recovery_plans', null=True, blank=True)
    plan_title = models.CharField(max_length=255, default='Failover to Secondary Payment Gateway')
    recovery_action = models.CharField(max_length=100, default='SWITCH_PAYMENT_GATEWAY')
    target_resource = models.CharField(max_length=100, default='PG_SECONDARY')
    risk_score = models.IntegerField(default=15)
    requires_approval = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default='RECOMMENDED') # RECOMMENDED, EXECUTED, VERIFIED, ROLLED_BACK
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"RecoveryPlan: {self.plan_title} [{self.status}]"


class CircuitBreakerRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider_name = models.CharField(max_length=100, unique=True, default='Primary LLM Gateway')
    state = models.CharField(max_length=20, default='CLOSED') # CLOSED, OPEN, HALF_OPEN
    failure_count = models.IntegerField(default=0)
    last_state_change = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"CircuitBreaker: {self.provider_name} [{self.state}] (Failures: {self.failure_count})"


class TelemetryEventRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.CharField(max_length=100, default='default_tenant')
    service = models.CharField(max_length=100, default='Checkout & Order API')
    environment = models.CharField(max_length=50, default='production')
    event_type = models.CharField(max_length=50, default='METRIC') # LOG, METRIC, TRACE, EVENT, COST, LLMOPS
    trace_id = models.CharField(max_length=100, blank=True, default='')
    span_id = models.CharField(max_length=100, blank=True, default='')
    severity = models.CharField(max_length=30, default='INFO') # INFO, WARNING, ERROR, CRITICAL
    source = models.CharField(max_length=100, default='API Gateway')
    attributes_json = models.TextField(default='{}')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"TelemetryEvent: {self.event_type} [{self.service}] ({self.severity})"


class ServiceDefinitionRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_id = models.CharField(max_length=100, unique=True, default='svc_checkout_api')
    name = models.CharField(max_length=255, default='Checkout & Order API')
    owner = models.CharField(max_length=150, default='Anita Sharma (Staff SRE)')
    team = models.CharField(max_length=150, default='Commerce Core Platform')
    environment = models.CharField(max_length=50, default='production')
    criticality = models.CharField(max_length=30, default='TIER_0') # TIER_0, TIER_1, TIER_2
    status = models.CharField(max_length=30, default='HEALTHY') # HEALTHY, DEGRADED, CRITICAL
    latency_ms = models.IntegerField(default=112)
    error_rate = models.FloatField(default=0.08)
    traffic_rpm = models.IntegerField(default=4500)
    saturation_pct = models.FloatField(default=42.5)
    dependencies_json = models.TextField(default='[]')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ServiceDefinition: {self.name} [{self.status}]"


class SLORecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='Checkout Availability (99.9%)')
    service_name = models.CharField(max_length=150, default='Checkout & Order API')
    target_pct = models.FloatField(default=99.90)
    current_pct = models.FloatField(default=99.94)
    measurement_window = models.CharField(max_length=50, default='30d')
    error_budget_remaining_pct = models.FloatField(default=60.00)
    burn_rate = models.FloatField(default=0.8)
    status = models.CharField(max_length=30, default='MET') # MET, WARNING, BREACHED
    owner = models.CharField(max_length=150, default='Commerce Core Platform')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SLO: {self.name} [{self.status}] ({self.error_budget_remaining_pct}% Budget Left)"


class AlertRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='High P95 Latency Anomaly')
    service = models.CharField(max_length=150, default='Checkout & Order API')
    severity = models.CharField(max_length=30, default='HIGH') # LOW, MEDIUM, HIGH, CRITICAL
    category = models.CharField(max_length=50, default='LATENCY') # LATENCY, ERROR_RATE, CAPACITY, COST, LLM_QUALITY
    correlated_incident_id = models.CharField(max_length=100, blank=True, default='')
    deduplicated_count = models.IntegerField(default=1)
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, ACKNOWLEDGED, RESOLVED
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Alert: {self.title} [{self.severity}] (Deduplicated x{self.deduplicated_count})"


class SRETraceRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trace_id = models.CharField(max_length=100, default=uuid.uuid4)
    user_goal = models.CharField(max_length=255, default='Artisan Product AI Catalog Generation')
    flow_steps_json = models.TextField(default='[]')
    total_latency_ms = models.IntegerField(default=480)
    llm_token_count = models.IntegerField(default=14200)
    llm_cost_usd = models.FloatField(default=0.0426)
    tool_call_count = models.IntegerField(default=8)
    has_bottleneck = models.BooleanField(default=False)
    bottleneck_stage = models.CharField(max_length=100, default='NONE')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"SRETrace: {self.user_goal} ({self.total_latency_ms}ms, ${self.llm_cost_usd})"


class RunbookRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='Database Connection Contention Mitigation')
    service = models.CharField(max_length=150, default='Checkout & Order API')
    category = models.CharField(max_length=50, default='DATABASE')
    symptoms = models.TextField(default='Postgres connection pool exhaustion and elevated P95 latency.')
    safe_checks_json = models.TextField(default='["Inspect pg_stat_activity", "Check active pool usage"]')
    recovery_actions_json = models.TextField(default='["Switch read-traffic to read replicas", "Scale worker pool"]')
    requires_four_eyes_approval = models.BooleanField(default=False)
    usage_count = models.IntegerField(default=12)
    success_rate_pct = models.FloatField(default=98.5)
    version = models.CharField(max_length=20, default='v1.4')

    def __str__(self):
        return f"Runbook: {self.title} [{self.version}]"


class CodeEntityRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_id = models.CharField(max_length=100, unique=True, default='code_backend_models')
    name = models.CharField(max_length=255, default='artisan_api.models')
    entity_type = models.CharField(max_length=50, default='MODULE') # MODULE, CLASS, FUNCTION, SERVICE, COMPONENT
    filepath = models.CharField(max_length=255, default='backend/artisan_api/models.py')
    owner = models.CharField(max_length=150, default='Data Architecture Team')
    language = models.CharField(max_length=50, default='Python/Django')
    lines_of_code = models.IntegerField(default=2400)
    complexity_score = models.IntegerField(default=15)
    dependencies_json = models.TextField(default='[]')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CodeEntity: {self.name} [{self.entity_type}]"


class RequirementRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='Requirement Definition')
    raw_text = models.TextField(default='')
    acceptance_criteria_json = models.TextField(default='[]')
    affected_components_json = models.TextField(default='[]')
    implementation_plan_json = models.TextField(default='[]')
    risk_level = models.CharField(max_length=30, default='MEDIUM') # LOW, MEDIUM, HIGH
    status = models.CharField(max_length=30, default='PARSED') # PARSED, APPROVED, IMPLEMENTED
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Requirement: {self.title} [{self.status}]"


class EngineeringTaskRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal = models.CharField(max_length=255, default='Engineering Task Goal')
    assigned_agent = models.CharField(max_length=100, default='BackendEngineerAgent')
    status = models.CharField(max_length=30, default='IN_PROGRESS') # PLANNED, IN_PROGRESS, REVIEWING, COMPLETED
    affected_files_json = models.TextField(default='[]')
    risk_score = models.IntegerField(default=15)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"EngineeringTask: {self.goal} [{self.status}]"


class CodeChangeRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_file = models.CharField(max_length=255, default='backend/artisan_api/views.py')
    summary = models.TextField(default='Minimal diff patch applied for safe error handling.')
    diff_content = models.TextField(default='')
    minimality_score = models.FloatField(default=9.5)
    risk_score = models.IntegerField(default=15)
    status = models.CharField(max_length=30, default='DRAFT') # DRAFT, REVIEWED, MERGED, REJECTED
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"CodeChange: {self.target_file} (Risk: {self.risk_score})"


class CodeReviewRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_change = models.ForeignKey(CodeChangeRecord, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    reviewer_agent = models.CharField(max_length=100, default='AICodeReviewerAgent')
    findings_json = models.TextField(default='[]')
    security_passed = models.BooleanField(default=True)
    quality_score = models.FloatField(default=98.5)
    approval_status = models.CharField(max_length=30, default='APPROVED') # APPROVED, REJECTED, NEEDS_REVISION
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"CodeReview: {self.reviewer_agent} [{self.approval_status}] ({self.quality_score}%)"


class TestCaseRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='test_order_creation_with_null_discount')
    test_type = models.CharField(max_length=50, default='UNIT') # UNIT, INTEGRATION, REGRESSION, SECURITY
    filepath = models.CharField(max_length=255, default='backend/artisan_api/tests.py')
    code_body = models.TextField(default='')
    is_flaky = models.BooleanField(default=False)
    last_status = models.CharField(max_length=30, default='PASSED') # PASSED, FAILED, QUARANTINED
    duration_ms = models.IntegerField(default=140)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"TestCase: {self.name} [{self.last_status}]"


class BuildArtifactRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commit_sha = models.CharField(max_length=100, default='sha_a1b2c3d')
    artifact_name = models.CharField(max_length=255, default='artisan-core-build-v2.7')
    environment = models.CharField(max_length=50, default='staging') # dev, staging, canary, production
    checksum_sha256 = models.CharField(max_length=100, default='sha256_e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
    build_status = models.CharField(max_length=30, default='SUCCESS') # SUCCESS, FAILED
    test_pass_rate_pct = models.FloatField(default=100.0)
    security_scan_passed = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"BuildArtifact: {self.artifact_name} [{self.build_status}]"


class ReleaseRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.CharField(max_length=50, default='v2.7.0')
    environment = models.CharField(max_length=50, default='canary')
    release_readiness_score = models.FloatField(default=98.0)
    dora_metrics_json = models.TextField(default='{}')
    status = models.CharField(max_length=30, default='STAGING') # STAGING, CANARY, DEPLOYED, ROLLED_BACK
    released_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Release: {self.version} [{self.status}] ({self.environment})"


class TechnicalDebtRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='Refactor Duplicate View Logic')
    component = models.CharField(max_length=150, default='artisan_api.views')
    problem_description = models.TextField(default='Duplicate settlement reconciliation calculations.')
    risk_score = models.IntegerField(default=25)
    estimated_effort_hours = models.FloatField(default=3.0)
    owner = models.CharField(max_length=150, default='FinOps & Architecture Team')
    status = models.CharField(max_length=30, default='OPEN') # OPEN, IN_PROGRESS, RESOLVED

    def __str__(self):
        return f"TechnicalDebt: {self.title} [{self.status}]"


class ADRRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='ADR 027: Consolidate Settlement Reconciliation')
    status = models.CharField(max_length=30, default='PROPOSED') # PROPOSED, ACCEPTED, SUPERSEDED
    context = models.TextField(default='')
    decision = models.TextField(default='')
    consequences = models.TextField(default='')
    author = models.CharField(max_length=150, default='Software Architect Agent')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ADR: {self.title} [{self.status}]"


# --- PROMPT #28 AI DATA ENGINEERING, DATAOPS & AUTONOMOUS DATA PLATFORM OS MODELS ---

class DataSourceRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_id = models.CharField(max_length=100, unique=True, default='src_pg_main')
    organization_id = models.CharField(max_length=100, default='org_artisan_crafts')
    source_type = models.CharField(max_length=50, default='PostgreSQL') # PostgreSQL, MySQL, CSV, JSON, Excel, REST_API, GraphQL, Webhook, Marketplace_API, Payment_API, Logistics_API, IoT, CloudStorage
    source_name = models.CharField(max_length=255, default='Main ERP & Transactions DB')
    owner = models.CharField(max_length=150, default='Data Platform Team')
    connection_ref = models.CharField(max_length=255, default='postgresql://user:***@db.internal:5432/commerce_os')
    ingestion_mode = models.CharField(max_length=30, default='CDC') # BATCH, STREAMING, CDC
    schema_json = models.JSONField(default=dict, blank=True)
    freshness_expectation_mins = models.IntegerField(default=15)
    data_classification = models.CharField(max_length=50, default='CONFIDENTIAL') # PUBLIC, INTERNAL, CONFIDENTIAL, SENSITIVE
    quality_score = models.FloatField(default=95.0)
    status = models.CharField(max_length=30, default='HEALTHY') # HEALTHY, WARNING, FAILED, PAUSED
    last_successful_ingestion = models.DateTimeField(default=timezone.now)
    last_failure = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"DataSource: {self.source_name} ({self.source_type}) [{self.status}]"


class IngestionJobRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_id = models.CharField(max_length=100, unique=True, default='job_ingest_001')
    source_id = models.CharField(max_length=100, default='src_pg_main')
    organization_id = models.CharField(max_length=100, default='org_artisan_crafts')
    pipeline_id = models.CharField(max_length=100, default='pipe_orders_clean')
    mode = models.CharField(max_length=30, default='BATCH') # BATCH, STREAMING, CDC
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, default='COMPLETED') # RUNNING, COMPLETED, FAILED, RESUMED
    records_read = models.IntegerField(default=12500)
    records_written = models.IntegerField(default=12495)
    records_rejected = models.IntegerField(default=5)
    bytes_processed = models.BigIntegerField(default=4500000)
    checkpoint = models.CharField(max_length=255, default='ckpt_pos_12495')
    error_summary = models.TextField(blank=True, default='')
    retry_count = models.IntegerField(default=0)
    execution_version = models.CharField(max_length=30, default='v1.0')

    def __str__(self):
        return f"IngestionJob: {self.job_id} [{self.status}] ({self.records_written} recs)"


class SchemaRegistryRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_name = models.CharField(max_length=150, default='canonical_orders')
    version = models.CharField(max_length=30, default='v2.1')
    owner = models.CharField(max_length=150, default='Data Engineering Team')
    schema_json = models.JSONField(default=dict, blank=True)
    checksum = models.CharField(max_length=100, default='sha256_schema_ord_v2.1')
    detected_drift_json = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, DRIFT_DETECTED, PAUSED
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"SchemaRegistry: {self.table_name} ({self.version}) [{self.status}]"


class DataContractRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, default='OrderCreatedContract')
    source_service = models.CharField(max_length=100, default='MarketplaceAPI')
    target_service = models.CharField(max_length=100, default='FinanceEngine')
    schema_definition_json = models.JSONField(default=dict, blank=True)
    quality_rules_json = models.JSONField(default=dict, blank=True)
    freshness_sla_mins = models.IntegerField(default=10)
    owner = models.CharField(max_length=150, default='Data Governance Office')
    status = models.CharField(max_length=30, default='VERIFIED') # VERIFIED, VIOLATED, DEPRECATED
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"DataContract: {self.name} [{self.status}] ({self.source_service} -> {self.target_service})"


class DataQualityCheckRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset_name = models.CharField(max_length=150, default='canonical_inventory')
    check_type = models.CharField(max_length=50, default='COMPLETENESS') # COMPLETENESS, VALIDITY, UNIQUENESS, CONSISTENCY, FRESHNESS, ACCURACY, INTEGRITY
    passed = models.BooleanField(default=True)
    failed_records_count = models.IntegerField(default=0)
    score = models.FloatField(default=98.5)
    details_json = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"DataQualityCheck: {self.dataset_name} [{self.check_type}] Passed={self.passed} Score={self.score}%"


class DataLineageEdgeRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_entity = models.CharField(max_length=150, default='raw_marketplace_orders')
    destination_entity = models.CharField(max_length=150, default='curated_sales_analytics')
    transformation_rule = models.TextField(default='Join with Customer 360 & Normalize Currency to INR')
    version = models.CharField(max_length=30, default='v1.0')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"DataLineage: {self.source_entity} -> {self.destination_entity}"


class DataIncidentRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident_id = models.CharField(max_length=100, unique=True, default='INC_DATA_901')
    severity = models.CharField(max_length=30, default='HIGH') # LOW, MEDIUM, HIGH, CRITICAL
    affected_dataset = models.CharField(max_length=150, default='inventory_reconciliation_feed')
    pipeline_id = models.CharField(max_length=100, default='pipe_inv_sync')
    symptoms = models.TextField(default='Warehouse inventory (100 units) contradicts Marketplace inventory (82 units).')
    root_cause = models.TextField(default='Upstream API webhook dropped 18 cancellation events.')
    recovery_plan = models.TextField(default='Replay cancellation CDC stream and re-reconcile stock balances.')
    status = models.CharField(max_length=30, default='DETECTED') # DETECTED, INVESTIGATING, RESOLVED, AUTO_HEALED
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"DataIncident: {self.incident_id} [{self.severity}] - {self.affected_dataset}"


class DataProductRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, default='Artisan Commerce Customer 360')
    domain = models.CharField(max_length=50, default='Commerce') # Commerce, Finance, Customer, Supply, Market, Creator, Security, Operations
    owner = models.CharField(max_length=150, default='Customer Intelligence Lead')
    version = models.CharField(max_length=30, default='v3.0')
    freshness_sla_mins = models.IntegerField(default=30)
    trust_score = models.FloatField(default=96.2)
    schema_json = models.JSONField(default=dict, blank=True)
    usage_count = models.IntegerField(default=1420)
    status = models.CharField(max_length=30, default='PUBLISHED') # PUBLISHED, DEPRECATED

    def __str__(self):
        return f"DataProduct: {self.name} (v{self.version}) [{self.trust_score}% Trust]"


# --- PROMPT #29 AI RESEARCH, WEB INTELLIGENCE & DEEP RESEARCH OS MODELS ---

class ResearchSourceRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_id = models.CharField(max_length=100, unique=True, default='src_eurostat_01')
    url = models.URLField(max_length=500, default='https://ec.europa.eu/eurostat/handicrafts-market-2026')
    source_type = models.CharField(max_length=50, default='GOVERNMENT') # GOVERNMENT, ACADEMIC, INDUSTRY_REPORT, NEWS, CORPORATE, UNVERIFIED
    publisher = models.CharField(max_length=200, default='Eurostat Trade Directorate')
    domain = models.CharField(max_length=150, default='ec.europa.eu')
    authority_score = models.FloatField(default=95.0)
    freshness_score = models.FloatField(default=92.0)
    trust_classification = models.CharField(max_length=30, default='AUTHORITATIVE') # AUTHORITATIVE, SECONDARY, COMMUNITY, UNTRUSTED
    retrieved_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ResearchSource: {self.publisher} ({self.domain}) [{self.trust_classification}]"


class ResearchQuestionRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_id = models.CharField(max_length=100, unique=True, default='Q_EU_EXPANSION_001')
    objective = models.TextField(default='Should our artisan commerce platform expand into the European handmade gift market?')
    depth_mode = models.CharField(max_length=30, default='DEEP') # QUICK, STANDARD, DEEP, ENTERPRISE
    time_budget_sec = models.IntegerField(default=120)
    status = models.CharField(max_length=30, default='COMPLETED') # IN_PROGRESS, COMPLETED, SATURATED, FAILED
    answer_summary = models.TextField(default='European handmade gift market exhibits 14.2% YoY growth with high demand for Jaipur terracotta and handloom silk.')
    confidence_score = models.FloatField(default=94.5)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ResearchQuestion: {self.question_id} [{self.status}] Confidence={self.confidence_score}%"


class ClaimRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    claim_id = models.CharField(max_length=100, unique=True, default='CLM_001')
    question_id = models.CharField(max_length=100, default='Q_EU_EXPANSION_001')
    statement = models.TextField(default='EU market demand for artisan sustainable gifts is estimated at €4.2 Billion in 2026.')
    source_url = models.URLField(max_length=500, default='https://ec.europa.eu/eurostat/handicrafts-market-2026')
    evidence_snippet = models.TextField(default='Page 14, Table 3: Sustainable craft imports grew 14.2% YoY.')
    evidence_level = models.CharField(max_length=20, default='E4_PRIMARY') # E0_UNSUPPORTED, E1_WEAK, E2_SINGLE_CREDIBLE, E3_MULTIPLE_CREDIBLE, E4_PRIMARY, E5_DIRECT_INTERNAL
    confidence_score = models.FloatField(default=96.0)
    status = models.CharField(max_length=30, default='VERIFIED') # VERIFIED, CONTRADICTED, UNVERIFIED
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Claim: {self.statement[:60]}... [{self.evidence_level}]"


class EvidencePackRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pack_id = models.CharField(max_length=100, unique=True, default='EVP_EU_2026')
    question_id = models.CharField(max_length=100, default='Q_EU_EXPANSION_001')
    claims_json = models.JSONField(default=list, blank=True)
    corroboration_count = models.IntegerField(default=5)
    contradiction_count = models.IntegerField(default=0)
    trust_score = models.FloatField(default=95.2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"EvidencePack: {self.pack_id} ({self.corroboration_count} Claims, Trust={self.trust_score}%)"


class ResearchReportRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_id = models.CharField(max_length=100, unique=True, default='REP_EU_GIFTS_2026')
    title = models.CharField(max_length=255, default='European Handmade Gift Market Expansion Deep Research Report')
    topic = models.CharField(max_length=100, default='Market Expansion')
    executive_summary = models.TextField(default='High viability for European expansion with 14.2% demand growth in Germany and France.')
    findings_json = models.JSONField(default=dict, blank=True)
    contradictions_json = models.JSONField(default=dict, blank=True)
    unknowns_json = models.JSONField(default=dict, blank=True)
    version = models.CharField(max_length=30, default='v1.0')
    status = models.CharField(max_length=30, default='PUBLISHED') # DRAFT, PUBLISHED, ARCHIVED
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ResearchReport: {self.title} (v{self.version})"


class ResearchWatchlistRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic_or_competitor = models.CharField(max_length=150, default='EU Import Tariffs & Craft Regulations')
    frequency = models.CharField(max_length=30, default='DAILY') # HOURLY, DAILY, WEEKLY
    last_checked = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, default='ACTIVE')

    def __str__(self):
        return f"ResearchWatchlist: {self.topic_or_competitor} [{self.frequency}]"


# --- PROMPT #30 AI PROCESS INTELLIGENCE, WORKFLOW MINING & AUTONOMOUS BUSINESS OPERATIONS OS MODELS ---

class BusinessProcessRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    process_id = models.CharField(max_length=100, unique=True, default='proc_b2b_order_fulfillment')
    name = models.CharField(max_length=255, default='B2B Bulk Order Fulfillment & Settlement Process')
    category = models.CharField(max_length=50, default='Commerce') # Commerce, Finance, SupplyChain, Marketing, Support, Export, DevSecOps
    version = models.CharField(max_length=30, default='v2.0')
    happy_path_json = models.JSONField(default=list, blank=True)
    actual_variants_json = models.JSONField(default=list, blank=True)
    automation_level = models.CharField(max_length=50, default='Level 3 Bounded Automation')
    health_score = models.FloatField(default=92.5)
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, PAUSED, DEPRECATED

    def __str__(self):
        return f"BusinessProcess: {self.name} (v{self.version}) [{self.health_score}% Health]"


class ProcessStepRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step_id = models.CharField(max_length=100, default='step_supplier_confirm')
    process_id = models.CharField(max_length=100, default='proc_b2b_order_fulfillment')
    step_name = models.CharField(max_length=150, default='Supplier Confirmation & Raw Material Check')
    step_type = models.CharField(max_length=50, default='HUMAN') # HUMAN, AI_AGENT, SYSTEM, APPROVAL, DECISION
    avg_duration_sec = models.IntegerField(default=129600) # 36 hours
    risk_level = models.CharField(max_length=20, default='MEDIUM') # LOW, MEDIUM, HIGH
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ProcessStep: {self.step_name} [{self.step_type}] ({self.avg_duration_sec}s)"


class ProcessEventRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_id = models.CharField(max_length=100, default='CASE_B2B_901')
    process_id = models.CharField(max_length=100, default='proc_b2b_order_fulfillment')
    step_name = models.CharField(max_length=150, default='Supplier Confirmation')
    actor = models.CharField(max_length=100, default='Jaipur Supplier Network')
    timestamp = models.DateTimeField(default=timezone.now)
    duration_sec = models.IntegerField(default=115200)
    status = models.CharField(max_length=30, default='COMPLETED') # COMPLETED, DELAYED, FAILED, RETRIED

    def __str__(self):
        return f"ProcessEvent: {self.case_id} -> {self.step_name} [{self.status}]"


class ProcessBottleneckRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    process_id = models.CharField(max_length=100, default='proc_b2b_order_fulfillment')
    bottleneck_step = models.CharField(max_length=150, default='Supplier Confirmation & Raw Material Check')
    avg_wait_time_sec = models.IntegerField(default=115200) # 32 hours wait
    failure_rate_pct = models.FloatField(default=14.5)
    cost_impact_inr = models.FloatField(default=45000.0)
    root_cause_summary = models.TextField(default='Manual phone follow-ups and lack of automated SMS/WhatsApp reminders.')
    status = models.CharField(max_length=30, default='ACTIVE') # ACTIVE, MITIGATED, RESOLVED

    def __str__(self):
        return f"ProcessBottleneck: {self.bottleneck_step} (Wait: {self.avg_wait_time_sec}s)"


class WorkflowOptimizationProposalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='Automate Supplier Reminders & Parallelize QC Checkpoint')
    process_id = models.CharField(max_length=100, default='proc_b2b_order_fulfillment')
    current_cycle_time_mins = models.IntegerField(default=2880) # 48 hours
    proposed_cycle_time_mins = models.IntegerField(default=840) # 14 hours
    estimated_roi_inr = models.FloatField(default=185000.0)
    risk_assessment = models.CharField(max_length=50, default='LOW_RISK_REVERSIBLE')
    status = models.CharField(max_length=30, default='APPROVED') # PROPOSED, APPROVED, CANARY_TESTING, DEPLOYED

    def __str__(self):
        return f"WorkflowOptimization: {self.title} [{self.status}]"


class ProcessDecisionReceiptRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_id = models.CharField(max_length=100, default='CASE_B2B_901')
    decision = models.TextField(default='Deployed bounded automated supplier reminder and parallel inventory validation workflow.')
    evidence_json = models.JSONField(default=dict, blank=True)
    policy_version = models.CharField(max_length=30, default='POL_BOUNDED_WORKFLOW_v2')
    actor = models.CharField(max_length=100, default='Process Intelligence Agent')
    approved_by = models.CharField(max_length=100, default='Operations Manager')
    status = models.CharField(max_length=30, default='VERIFIED')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ProcessDecisionReceipt: {self.case_id} [{self.status}]"

















