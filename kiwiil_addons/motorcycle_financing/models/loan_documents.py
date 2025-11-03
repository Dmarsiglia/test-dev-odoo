from odoo import models, fields, api

class LoanDocuments(models.Model):
    _name = 'motorcycle.loan.documents'
    _description = 'Motorcycle Loan Documents Model'
    _order = 'sequence asc, name asc'

    sequence = fields.Integer(string='Sequence', default=1)
    name = fields.Char(string='Document Name', required=True)
    attachment = fields.Binary(string='attachment')
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

    def action_change_state_approved(self):
        for record in self:
            record.state = 'approved'

    def action_change_state_rejected(self):
        for record in self:
            record.state = 'rejected'

    @api.onchange('attachment')
    def _onchange_state_new(self):
        for record in self:
            record.state = 'review'