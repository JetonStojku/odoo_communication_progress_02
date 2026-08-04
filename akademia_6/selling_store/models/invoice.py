from odoo import fields, models, api


class SellingStoreInvoice(models.Model):
    _name = 'selling_store.invoice'

    code = fields.Char(string="Invoice Number")
    employee_id = fields.Many2one(comodel_name='selling_store.employee', string='Employee', required=True)
    client_id = fields.Many2one(comodel_name='selling_store.client', string='Client_id')
    invoice_date = fields.Datetime(string='Invoice date', required=True, default=lambda self: fields.Datetime.now())
