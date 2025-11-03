from odoo import models, fields

class LoanCategory(models.Model):
    _name = 'motorcycle.loan.tag'
    _description = 'Motorcycle Loan Tag Model'
    _order = 'sequence asc'

    sequence = fields.Integer(string='Sequence', default=1)
    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string='Color', help='Color code for the category')
    #loan_id = fields.Many2one('motorcycle.loan', string='Loan')

    _check_name_unique = models.Constraint(
        "UNIQUE(name)",
        'Category name must be unique.'
    )