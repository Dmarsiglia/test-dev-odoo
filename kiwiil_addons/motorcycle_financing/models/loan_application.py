from odoo import models, fields

class Loan(models.Model):
    _name = 'motorcycle.loan'
    _description = 'Motorcycle Loan Model'

    name = fields.Char(string='Aplication Number', required=True)
    currency_id = fields.Many2one(comodel_name='res.currency', default=lambda self: self.env.company.currency_id, string='Currency')
    date_application = fields.Date(string='Application Date', default=fields.Date.context_today)
    date_approval = fields.Date(string='Approval Date', readonly=True, copy=False)
    date_rejection = fields.Date(string='Rejection Date', readonly=True, copy=False)
    date_signed = fields.Date(string='Signed On', readonly=True, copy=False)
    down_payment = fields.Monetary(string='Downpayment', currency_field='currency_id')
    interest_rate = fields.Float(string='Interest Rate (%)', digits=(5, 4))
    loan_amount = fields.Monetary(string='Loan Amount', currency_field='currency_id')
    loan_term = fields.Integer(string='Loan Term (Months)', required=True, default=36)
    rejection_reason = fields.Text(string='Rejection Reason', copy=False)
    tags = fields.Many2many(
        comodel_name='motorcycle.loan.tag',
        string='Categories',
        help='Tags for categorizing loan applications'
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'), 
            ('sent', 'Sent'), 
            ('review', 'Credit Check'), 
            ('approved', 'Approved'), 
            ('rejected', 'Rejected'), 
            ('signed', 'Signed'), 
            ('cancel', 'Canceled')
        ], 
         default='draft', copy=False

    )
    notes = fields.Html(string='Notes', copy=False)
