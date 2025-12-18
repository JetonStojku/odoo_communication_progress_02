from odoo import models, fields


class InvoiceReport(models.TransientModel):
    _name = 'market.invoice.report.wizard'
    _description = 'Invoice report wizard'

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
        return self.env.ref('market.action_report_invoice').report_action(None, data=data)
