from odoo import models, _, fields
from odoo.exceptions import UserError

class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    def action_create_budget_estimate(self):
        self.ensure_one()
        
        # Validate budget lines exist
        expense_lines = self.crossovered_budget_line.filtered(lambda l: l.general_budget_id.name == 'Expenses')
        revenue_lines = self.crossovered_budget_line.filtered(lambda l: l.general_budget_id.name == 'Revenue')
        
        if not expense_lines and not revenue_lines:
            raise UserError(_("No budget lines found with 'Expenses' or 'Revenue' category. Please verify budget line classifications."))

        # Compute core values
        total_project_expenses = -sum(expense_lines.mapped('planned_amount'))
        project_value = sum(revenue_lines.mapped('planned_amount'))
        actual_expenses_incurred = -sum(expense_lines.mapped('practical_amount'))
        actual_invoiced_amount = sum(revenue_lines.mapped('practical_amount'))

        # Calculate percentages and derived values
        project_completed_percentage = 0.0
        if total_project_expenses > 0:
            project_completed_percentage = (actual_expenses_incurred / total_project_expenses) * 100.0

        estimated_revenue = project_value * (project_completed_percentage / 100.0)

        gross_margin = estimated_revenue - actual_expenses_incurred
        gross_margin_percentage = 0.0
        if estimated_revenue > 0:
            gross_margin_percentage = (gross_margin / estimated_revenue) * 100.0

        # Round values for clean storage
        vals = {
            'budget_id': self.id,
            'budget_name': self.name,
            'company_id': self.company_id.id,
            'total_project_expenses': round(total_project_expenses, 2),
            'project_value': round(project_value, 2),
            'actual_expenses_incurred': round(actual_expenses_incurred, 2),
            'actual_invoiced_amount': round(actual_invoiced_amount, 2),
            'project_completed_percentage': round(project_completed_percentage, 4),
            'estimated_revenue': round(estimated_revenue, 2),
            'gross_margin': round(gross_margin, 2),
            'gross_margin_percentage': round(gross_margin_percentage, 4),
        }

        # Create snapshot
        estimate = self.env['budget.estimate'].create(vals)
        
        # Open the created record
        return {
            'type': 'ir.actions.act_window',
            'name': _('Budget Estimate'),
            'res_model': 'budget.estimate',
            'res_id': estimate.id,
            'view_mode': 'form',
            'target': 'current',
            'context': self.env.context,
        }