from odoo import models, api


class marketReportInvoice(models.AbstractModel):
    _name = 'report.market.report_invoice_product'
    _description = 'Invoice Group by product report'

    @api.model
    def _get_report_values(self, docids, data=None):

        domain = [('invoice_id.date', '>=', data['start_date']), ('invoice_id.date', '<', data['end_date'])]

        if not data['product_ids']:
            name = 'All products'
        else:
            domain.append(('product_id', 'in', data['product_ids']))
            products = self.env['market.product'].browse(data['product_ids']).mapped("product")
            name = f'Products: {", ".join(products)}.'

        invoice_line_object = self.env['market.invoice.line'].search(domain)
        products_report = {}

        for invoice_line in invoice_line_object:
            if invoice_line.product_id.id in products_report:
                if invoice_line.invoice_id.invoice_type == 'in':
                    products_report[invoice_line.product_id.id]['qty_in'] += invoice_line.quantity
                    products_report[invoice_line.product_id.id]['total_in'] += invoice_line.total
                else:
                    products_report[invoice_line.product_id.id]['qty_out'] += invoice_line.quantity
                    products_report[invoice_line.product_id.id]['total_out'] += invoice_line.total
            else:
                if invoice_line.invoice_id.invoice_type == 'in':
                    products_report[invoice_line.product_id.id] = {
                        'product': invoice_line.product_id.product,
                        'qty_in': invoice_line.quantity,
                        'total_in': invoice_line.total,
                        'qty_out': 0,
                        'total_out': 0,
                    }
                else:
                    products_report[invoice_line.product_id.id] = {
                        'product': invoice_line.product_id.product,
                        'qty_out': invoice_line.quantity,
                        'total_out': invoice_line.total,
                        'qty_in': 0,
                        'total_in': 0,
                    }
        return {
            'docs': products_report,
            'report_name': name,
        }
