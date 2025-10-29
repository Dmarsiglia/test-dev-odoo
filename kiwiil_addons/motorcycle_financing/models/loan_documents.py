from odoo import models, fields

class LoanDocuments(models.Model):
    _name = 'motorcycle.loan.documents'
    _description = 'Motorcycle Loan Documents Model'

    name = fields.Char(string='Document Name', required=True)
    attachment = fields.Text(string='attachment')
    type = fields.Many2one('motorcycle.loan.document.type', string='Document Type')
    aplication_id = fields.Many2one('motorcycle.loan', string='Loan Application')
    state = fields.Selection(
        selection=[
            ('review', 'Review'), 
            ('approved', 'Approved'), 
            ('rejected', 'Rejected'), 
        ], 
         default='review', copy=False

    )