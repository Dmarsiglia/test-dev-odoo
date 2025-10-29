from odoo import models, fields

class LoanDocumentType(models.Model):
    _name = 'motorcycle.loan.document.type'
    _description = 'Motorcycle Loan Document Type Model'

    name = fields.Char(string='Document Type Name', required=True)
    active = fields.Boolean(string='Active', default=True)