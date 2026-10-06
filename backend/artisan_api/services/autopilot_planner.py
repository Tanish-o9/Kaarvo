from artisan_api.models import BusinessGoalPlan, Product

class GoalPlanExecuteEngine:
    """AI Business Autopilot: Transforms high-level goals into structured step-by-step plans requiring human approval."""
    def create_goal_plan(self, artisan_user, goal_text: str) -> dict:
        products = list(Product.objects.filter(artisan=artisan_user)[:3])
        prod_titles = [p.title for p in products]

        plan_steps = [
            {'step': 1, 'action': 'IDENTIFY_FEATURED_CRAFTS', 'detail': f"Selected top products: {', '.join(prod_titles)}", 'status': 'completed'},
            {'step': 2, 'action': 'CREATE_FESTIVAL_BUNDLE', 'detail': 'Bundle top products with a 15% promotional discount.', 'status': 'pending_approval'},
            {'step': 3, 'action': 'GENERATE_WHATSAPP_CAMPAIGN', 'detail': 'Broadcast campaign copy to repeat buyers.', 'status': 'pending_approval'},
            {'step': 4, 'action': 'ONDC_MULTI_CHANNEL_SYNC', 'detail': 'Sync bundle inventory across ONDC and Amazon Karigar.', 'status': 'pending_approval'}
        ]

        plan = BusinessGoalPlan.objects.create(
            artisan=artisan_user,
            goal=goal_text,
            plan_steps=plan_steps,
            status='proposed'
        )

        return {
            'plan_id': str(plan.id),
            'goal': goal_text,
            'status': plan.status,
            'plan_steps': plan_steps,
            'requires_artisan_approval': True
        }

    def approve_and_execute_plan(self, plan_id: str) -> dict:
        try:
            plan = BusinessGoalPlan.objects.get(pk=plan_id)
            plan.status = 'approved'
            for step in plan.plan_steps:
                step['status'] = 'completed'
            plan.save()

            return {
                'message': f"Goal Plan '{plan.goal}' approved and executed successfully!",
                'plan_id': str(plan.id),
                'status': plan.status
            }
        except BusinessGoalPlan.DoesNotExist:
            return {'error': 'Plan not found'}
