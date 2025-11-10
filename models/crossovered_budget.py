from odoo import models, _, fields
from odoo.exceptions import UserError

class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    def action_create_budget_estimate(self):
        self.ensure_one()
        
        expense_lines = self.crossovered_budget_line.filtered(lambda l: l.general_budget_id.name == 'Expenses')
        revenue_lines = self.crossovered_budget_line.filtered(lambda l: l.general_budget_id.name == 'Revenue')
        
        if not expense_lines and not revenue_lines:
            raise UserError(_("No budget lines found with 'Expenses' or 'Revenue' category. Please verify budget line classifications."))

        # Compute core values
        total_project_expenses = -sum(expense_lines.mapped('planned_amount'))
        project_value = sum(revenue_lines.mapped('planned_amount'))
        actual_expenses_incurred = -sum(expense_lines.mapped('practical_amount'))
        actual_invoiced_amount = sum(revenue_lines.mapped('practical_amount'))

        # CORRECTED: Store as decimal (0.45), not percentage (45.0)
        project_completed_percentage = 0.0
        if total_project_expenses > 0:
            project_completed_percentage = actual_expenses_incurred / total_project_expenses  # Removed * 100

        estimated_revenue = project_value * project_completed_percentage

        gross_margin = estimated_revenue - actual_expenses_incurred
        
        # CORRECTED: Store as decimal (0.45), not percentage (45.0)
        gross_margin_percentage = 0.0
        if estimated_revenue > 0:
            gross_margin_percentage = gross_margin / estimated_revenue  # Removed * 100

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

        estimate = self.env['budget.estimate'].create(vals)
        
        # CORRECTED: Return proper action with breadcrumbs support
        return {
            'type': 'ir.actions.act_window',
            'name': _('Budget Estimate'),
            'res_model': 'budget.estimate',
            'res_id': estimate.id,
            'view_mode': 'form',
            'target': 'current',
            'views': [(False, 'form')],
            'context': self.env.context,
        }