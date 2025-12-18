from odoo import models, fields


class InvoiceProductReport(models.TransientModel):
    _name = 'market.invoice.product.report.wizard'
    _description = 'Invoice Product report wizard'

    product_ids = fields.Many2many(comodel_name='market.product', string='Product')
    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', required=True)

    def print_report(self):
        self.ensure_one()
        data = {
            "product_ids": self.product_ids.ids,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        return self.env.ref('market.action_report_invoice_product').report_action(None, data=data)
