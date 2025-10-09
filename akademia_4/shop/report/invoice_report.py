from odoo import models, api


class ShopReportInvoice(models.AbstractModel):
    _name = 'report.shop.report_invoice'
    _description = 'Invoice report'

    @api.model
    def _get_report_values(self, docids, data=None):

        domain = [('invoice_id.date', '>=', data['start_date']), ('invoice_id.date', '<', data['end_date'])]

        if not data['product_ids']:
            name = 'All products'
        else:
            domain.append(('product_id', 'in', data['product_ids']))
            produktet = self.env['shop.product'].browse(data['product_ids']).mapped("name")
            name = f'Products: {", ".join(produktet)}.'

        invoice_line_object = self.env['shop.invoice.line'].search(domain)
        invoice_lines = []

        for invoice_line in invoice_line_object:
            invoice_lines.append({
                'product': invoice_line.product_id.name,
                'date': invoice_line.invoice_id.date,
                'quantity': invoice_line.quantity,
                'price': invoice_line.price,
                'total': invoice_line.total,
                'type': 'OUT' if invoice_line.invoice_id.selling_invoice else 'IN',
            })

        return {
            'docs': invoice_lines,
            'r_name': name,
        }
