from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SellingStoreInvoice(models.Model):
    _name = 'selling_store.invoice'

    code = fields.Char(string="Invoice Number")
    employee_id = fields.Many2one(comodel_name='selling_store.employee', string='Employee', required=True)
    client_id = fields.Many2one(comodel_name='selling_store.client', string='Client')
    invoice_date = fields.Datetime(string='Invoice date', required=True, default=lambda self: fields.Datetime.now())
    total = fields.Float(string='Total', compute='_calc_total', store=True)
    # total = fields.Float(string='Total')
    state = fields.Selection(string='State', required=True, default='draft',
                             selection=[('draft', 'Draft'),
                                        ('done', 'Done'),
                                        ('paid', 'Paid'),
                                        ], )
    type = fields.Selection(string='Type', required=True, default='out',
                            selection=[('in', 'Purchase'),
                                       ('out', 'Sell')])
    invoice_line_ids = fields.One2many(
        comodel_name='selling_store.invoice.line',
        inverse_name='invoice_id',
        string='Invoice Line')

    @api.depends('invoice_line_ids')
    def _calc_total(self):
        for invoice in self:
            #     s = 0
            #     for invoice_line in invoice.invoice_line_ids:
            #         s += invoice_line.total
            #     invoice.total = s
            invoice.total = sum(self.invoice_line_ids.mapped('total'))

    def done_invoice(self):
        for invoice_line in self.invoice_line_ids:
            if invoice_line.product_id.quantity < invoice_line.quantity:
                return ValueError('URI connections not allowed')
            invoice_line.product_id.quantity -= invoice_line.quantity
        self.state = 'done'

    def pay_invoice(self):
        self.state = 'paid'

    @api.model
    def create(self, values):
        if values.get('type') == 'in':
            values['code'] = self.env['ir.sequence'].next_by_code('in.invoice.cp')
        else:
            values['code'] = self.env['ir.sequence'].next_by_code('out.invoice.cp')

        invoice = super(SellingStoreInvoice, self).create(values)
        # invoice -> new object created
        return invoice


class SellingStoreInvoiceLine(models.Model):
    _name = 'selling_store.invoice.line'

    product_id = fields.Many2one(comodel_name='selling_store.product', string='Product')
    invoice_id = fields.Many2one(comodel_name='selling_store.invoice', string='Invoice')
    quantity = fields.Float(string='Quantity', default=1)
    price = fields.Float(string='Price')
    total = fields.Float(string='Total', compute='_calc_total')

    _sql_constraints = [
        ('quantity', 'CHECK(quantity>=0)', 'Quantity must be positive'),
        ('price', 'CHECK(price>=0)', 'Price must be positive'),
    ]

    # @api.constrains('quantity')
    # def _check_quantity(self):
    #     for line in self:
    #         if line.quantity < 0:
    #             raise ValidationError('Quantity must be positive')

    @api.onchange('product_id')
    def _onchange_method(self):
        if self.invoice_id.type == 'in':
            self.price = self.product_id.buy_price
        else:
            self.price = self.product_id.sell_price

    @api.depends('price', 'quantity')
    def _calc_total(self):
        for invoice_line in self:
            invoice_line.total = invoice_line.quantity * invoice_line.price
