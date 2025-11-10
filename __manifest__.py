{
    'name': 'Project Estimate Run',
    'version': '17.0',
    'category': 'Accounting/Accounting',
    'summary': 'Create read-only budget estimate snapshots',
    'description': """
        Adds an "Estimate Run" button to budgets to capture financial 
        snapshots based on Revenue/Expenses budget lines.
    """,
    'author': 'Chandika Rathnayake',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/budget_estimate_views.xml',
        'views/crossovered_budget_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}