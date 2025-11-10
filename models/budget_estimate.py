from odoo import models, fields, api, _

class BudgetEstimate(models.Model):
    _name = 'budget.estimate'
    _description = 'Budget Estimate Snapshot'
    _order = 'create_date desc'

    name = fields.Char(string='Estimate Reference', required=True, copy=False, readonly=True, index=True, default='New')
    budget_id = fields.Many2one('crossovered.budget', string='Source Budget', required=True, readonly=True, index=True)
    budget_name = fields.Char(string='Budget Name', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, 
                                 default=lambda self: self.env.company)

    # Financial snapshot values
    actual_expenses_incurred = fields.Float(string='Actual Expenses Incurred', readonly=True, 
                                           help="Sum of practical amounts for Expense lines")
    actual_invoiced_amount = fields.Float(string='Actual Invoiced Amount', readonly=True, 
                                         help="Sum of practical amounts for Revenue lines")
    total_project_expenses = fields.Float(string='Total Project Expenses', readonly=True, 
                                         help="Sum of planned amounts for Expense lines")
    project_value = fields.Float(string='Project Value', readonly=True, 
                                help="Sum of planned amounts for Revenue lines")
    project_completed_percentage = fields.Float(string='Project Completed %', readonly=True, digits=(16, 4),
                                               help="(Actual Expenses / Total Expenses) × 100")
    estimated_revenue = fields.Float(string='Estimated Revenue', readonly=True, 
                                    help="Project Value × (Completion % / 100)")
    gross_margin = fields.Float(string='Gross Margin', readonly=True, 
                               help="Estimated Revenue - Actual Expenses")
    gross_margin_percentage = fields.Float(string='Gross Margin %', readonly=True, digits=(16, 4),
                                          help="(Gross Margin / Estimated Revenue) × 100")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                seq_code = 'budget.estimate'
                vals['name'] = self.env['ir.sequence'].next_by_code(seq_code) or 'New'
        return super().create(vals_list)

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = 'New'  # Triggers new sequence generation
        return super().copy(default)