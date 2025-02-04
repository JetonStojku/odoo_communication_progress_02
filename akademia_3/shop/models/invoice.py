from odoo import fields, models


class ShopInvoice(models.Model):
    _name = 'shop.invoice'
    _rec_name = 'invoice_nr'

    invoice_nr = fields.Char(string='Invoice Number', required=True)
    date = fields.Datetime(string='Date', required=True, default=lambda self: fields.Datetime.now())
    client_id = fields.Many2one(comodel_name='shop.client', string='Client', required=True)
    employee_id = fields.Many2one(comodel_name='shop.employee', string='Employee', required=True)
    total = fields.Float(string='Total')
    invoice_line_ids = fields.One2many(comodel_name='shop.invoice.line', inverse_name='invoice_id')
    selling_invoice = fields.Boolean(string='Selling Invoice', default=True)
    state = fields.Selection(string='State', default='draft',
                             selection=[('draft', 'Draft'),
                                        ('done', 'Done'),
                                        ('paid', 'Paid')])


class ShopInvoiceLine(models.Model):
    _name = 'shop.invoice.line'

    product_id = fields.Many2one(comodel_name='shop.product', string='Product', required=True)
    invoice_id = fields.Many2one(comodel_name='shop.invoice', string='Invoice', required=True)
    quantity = fields.Float(string='Quantity', default=1)
    price = fields.Float(string='Price')
    total = fields.Float(string='Total')
