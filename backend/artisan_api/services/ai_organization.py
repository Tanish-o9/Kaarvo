import uuid
from artisan_api.models import AITask, ApprovalInboxItem, SmartSupportTicket, EventExhibitionMode, Product

class AIOrganizationEngine:
    """
    AI Supervisor Engine coordinating:
    1. Product Team (Catalog, Content, Image, Research)
    2. Business Team (Analytics, Pricing, Marketing, Inventory)
    3. Commerce Team (Order, Payment, Logistics, Marketplace)
    """

    TEAMS = {
        'PRODUCT_TEAM': ['Catalog Agent', 'Content Agent', 'Image Agent', 'Research Agent'],
        'BUSINESS_TEAM': ['Analytics Agent', 'Pricing Agent', 'Marketing Agent', 'Inventory Agent'],
        'COMMERCE_TEAM': ['Order Agent', 'Payment Agent', 'Logistics Agent', 'Marketplace Agent']
    }

    def dispatch_task(self, title: str, team: str, agent: str, priority: str = 'NORMAL', payload: dict = None, organization=None) -> dict:
        """Create and queue a generic AI task with role boundaries and approval rules."""
        requires_approval = priority in ['HIGH', 'URGENT'] or 'PRICE' in title.upper() or 'PAYMENT' in title.upper() or 'CAMPAIGN' in title.upper()

        task = AITask.objects.create(
            title=title,
            assigned_team=team,
            assigned_agent=agent,
            priority=priority,
            status='WAITING_APPROVAL' if requires_approval else 'RUNNING',
            payload=payload or {},
            organization=organization,
            requires_approval=requires_approval
        )

        if requires_approval:
            ApprovalInboxItem.objects.create(
                task=task,
                action_type=title,
                summary=f"Agent '{agent}' from '{team}' requests authorization for: {title}",
                reason=f"High operational priority ({priority}) or financial impact action.",
                expected_impact="Automation rate +15%, expected revenue increase or catalog synchronization.",
                preview_data=payload or {}
            )
            return {
                'status': 'WAITING_APPROVAL',
                'task_id': str(task.id),
                'message': f"Task '{title}' queued. Requires human approval in Approval Inbox."
            }
        else:
            # Simulate autonomous execution for safe low-risk tasks
            task.status = 'COMPLETED'
            task.result = {
                'executed_by': agent,
                'team': team,
                'status': 'SUCCESS',
                'details': f"Task '{title}' processed autonomously under Level 2/3 autonomy rules."
            }
            task.save()
            return {
                'status': 'COMPLETED',
                'task_id': str(task.id),
                'result': task.result
            }

class ApprovalInboxService:
    """Central Approval Inbox Manager for agentic commerce actions."""
    
    @staticmethod
    def approve_item(item_id: str) -> dict:
        try:
            item = ApprovalInboxItem.objects.get(pk=item_id)
            item.status = 'APPROVED'
            item.save()

            if item.task:
                task = item.task
                task.status = 'COMPLETED'
                task.result = {
                    'status': 'EXECUTED_AFTER_APPROVAL',
                    'approved_by': 'Human Merchant / Organization Admin',
                    'action': item.action_type,
                    'details': item.preview_data
                }
                task.save()

            return {
                'message': f"Action '{item.action_type}' approved and executed cleanly.",
                'item_id': str(item.id),
                'status': 'APPROVED'
            }
        except ApprovalInboxItem.DoesNotExist:
            return {'error': 'Approval item not found'}

    @staticmethod
    def reject_item(item_id: str, feedback: str = '') -> dict:
        try:
            item = ApprovalInboxItem.objects.get(pk=item_id)
            item.status = 'REJECTED'
            item.save()

            if item.task:
                task = item.task
                task.status = 'CANCELLED'
                task.result = {
                    'status': 'REJECTED_BY_HUMAN',
                    'feedback': feedback or 'Rejected by merchant policy'
                }
                task.save()

            return {
                'message': f"Action '{item.action_type}' rejected.",
                'item_id': str(item.id),
                'status': 'REJECTED'
            }
        except ApprovalInboxItem.DoesNotExist:
            return {'error': 'Approval item not found'}
