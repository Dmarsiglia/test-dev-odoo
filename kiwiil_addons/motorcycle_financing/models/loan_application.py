from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class Loan(models.Model):
    _name = 'motorcycle.loan'
    _description = 'Motorcycle Loan Model'
    _order = 'date_application desc, name desc'

    name = fields.Char(string='Aplication Number', required=True)
    date_application = fields.Date(string='Application Date', default=fields.Date.context_today)
    date_approval = fields.Date(string='Approval Date', readonly=True, copy=False)
    date_rejection = fields.Date(string='Rejection Date', readonly=True, copy=False)
    date_signed = fields.Date(string='Signed On', readonly=True, copy=False)
    down_payment = fields.Monetary(string='Downpayment', currency_field='currency_id')
    interest_rate = fields.Float(string='Interest Rate (%)', digits=(5, 4))
    loan_term = fields.Integer(string='Loan Term (Months)', required=True, default=36)
    rejection_reason = fields.Text(string='Rejection Reason', copy=False)
    tags = fields.Many2many(
        comodel_name='motorcycle.loan.tag',
        string='Categories',
        help='Tags for categorizing loan applications'
    )
    documents_ids = fields.One2many(
        comodel_name='motorcycle.loan.documents',
        inverse_name = 'aplication_id',
        string='Loan Documents'
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
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Related Sale Order')
    product_template_id = fields.Many2one(comodel_name='product.product', string='Motorcycle', required=True)
    sale_order_total = fields.Monetary(
        string='Sale Order Total', 
        #currency_field='currency_id', 
        related='sale_order_id.amount_total')
    currency_id = fields.Many2one(
    #comodel_name='res.currency', 
    #default=lambda self: self.env.company.currency_id, string='Currency'
    string='Currency',
    related='sale_order_id.currency_id', readonly=True
    )
    parther_id = fields.Many2one(
        #comodel_name='res.partner', 
        string='Customer', 
        related='sale_order_id.partner_id',
        readonly=True
        #required=True
    )
    user_id = fields.Many2one(
        #comodel_name='res.users',
        string='Salesperson', 
        related='sale_order_id.user_id',
        readonly=True
        #default=lambda self: self.env.user
    )
    loan_amount = fields.Monetary(
        string='Loan Amount', 
        currency_field='currency_id',
        compute='_compute_loan_amount',
        inverse='_inverse_loan_amount')

    display_name = fields.Char(
        string='Display Name',  
        compute='_compute_display_name',
        store=True
    )

    @api.depends('sale_order_total', 'down_payment')
    def _compute_loan_amount(self):
        for record in self:
            record.loan_amount = record.sale_order_total - record.down_payment

    def _inverse_loan_amount(self):
        for record in self:
            record.down_payment = record.sale_order_total - record.loan_amount

    def action_change_state_approved(self):
        for record in self:
            if record.state != 'approved':
                record.state = 'approved'
                record.date_approval = fields.Date.context_today(record)
            else:
                raise UserError(_("The application is already approved."))
    
    def action_change_state_rejected(self):
        for record in self:
            if not record.rejection_reason:
                raise UserError(_("Rejection reason is required to reject the application."))
            record.state = 'rejected'
            record.date_rejection = fields.Date.context_today(record)

    def action_sent(self):
        for record in self:
            # pending_docs = self.env['motorcycle.loan.documents'].search([
            #     ('id', 'in', record.documents_ids.ids),
            #     ('state', '!=', 'approved')
            # ])
            if record.documents_ids.filtered(lambda doc: doc.state != 'approved'):
                raise UserError(_("All documents must be approved before sending the application."))
            else:
                record.state = 'sent'
                record.date_application = fields.Date.context_today(record)

    @api.constrains('loan_amount', 'sale_order_total')
    def _check_loan_amount(self):
        for record in self:
            if record.loan_amount < 0 or record.loan_amount > record.sale_order_total:
                raise ValidationError(_('Loan amount must be between 0 and the sale order total.'))

    _check_down_payment = models.Constraint(
        "CHECK(down_payment >= 0)", 
        'Downpayment must be less than Sale Order Total.'
    )

    @api.depends('product_template_id', 'parther_id')
    def _compute_display_name(self):
        for record in self:
            if record.parther_id and record.product_template_id:
                record.display_name = f"{record.parther_id.name} - {record.product_template_id.name}"
            # else:
            #     raise ValidationError(_('Customer and Motorcycle must be set to compute display name.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            for record in self.env["motorcycle.loan.document.type"].search([("active", "=", True)]):
                vals.setdefault('documents_ids', []).append((0, 0, {
                    'name': record.name,
                    'type': record.id,
                    'state': 'pending'
                }))
        return super().create(vals_list)