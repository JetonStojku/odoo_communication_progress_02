from odoo import models, fields


class InvoiceReport(models.TransientModel):
    _name = 'shop.invoice.report.wizard'
    _description = 'Invoice report wizard'

    product_ids = fields.Many2many(comodel_name='shop.product', string='Product')
    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', required=True)
