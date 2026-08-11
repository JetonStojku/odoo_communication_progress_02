from odoo import fields, models, api


class SellingStoreInvoice(models.Model):
    _name = 'selling_store.invoice'

    code = fields.Char(string="Invoice Number")
    employee_id = fields.Many2one(comodel_name='selling_store.employee', string='Employee', required=True)
    client_id = fields.Many2one(comodel_name='selling_store.client', string='Client_id')
    invoice_date = fields.Datetime(string='Invoice date', required=True, default=lambda self: fields.Datetime.now())
    total = fields.Float(string='Total')
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


class SellingStoreInvoiceLine(models.Model):
    _name = 'selling_store.invoice.line'

    product_id = fields.Many2one(comodel_name='selling_store.product', string='Product')
    invoice_id = fields.Many2one(comodel_name='selling_store.invoice', string='Invoice')
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')
