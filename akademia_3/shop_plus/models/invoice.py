from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ShopInvoice(models.Model):
    _inherit = 'shop.invoice'

    points = fields.Integer(related='client_id.points', readonly=True)
    payment_method = fields.Selection(
        string='Payment method', required=True, default='cash',
        selection=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('points', 'Points'),
            ('mobile', 'Mobile')])

    def pay_invoice(self):
        if self.selling_invoice:
            if self.payment_method == 'points':
                if self.client_id.points < self.total:
                    raise ValidationError('You have less points that required!')
                self.client_id.points -= self.total
            else:
                self.client_id.points += self.total / 80
        self.state = 'paid'

    def confirm_invoice(self):
        if self.payment_method == 'mobile':
            # for line in self.invoice_line_ids:
            #     line.discount = 0.05
            self.invoice_line_ids.write({'discount': 0.05})
        super(ShopInvoice, self).confirm_invoice()


class ShopInvoiceLine(models.Model):
    _inherit = 'shop.invoice.line'

    discount = fields.Float(string='Discount', default=0, readonly=True)
    total = fields.Float(string='Total', compute='_compute_total')

    @api.depends('price', 'quantity', 'discount')
    def _compute_total(self):
        for line in self:
            line.total = (1 - line.discount) * line.price * line.quantity
