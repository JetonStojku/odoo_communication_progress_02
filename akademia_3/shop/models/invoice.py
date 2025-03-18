from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class ShopInvoice(models.Model):
    _name = 'shop.invoice'
    _rec_name = 'invoice_nr'

    invoice_nr = fields.Char(string='Invoice Number', default='New', required=True)
    date = fields.Datetime(string='Date', required=True, default=lambda self: fields.Datetime.now())
    client_id = fields.Many2one(comodel_name='shop.client', string='Client', required=True)
    employee_id = fields.Many2one(comodel_name='shop.employee', string='Employee', required=True)
    total = fields.Float(string='Total', compute='_calc_total', store=True)
    invoice_line_ids = fields.One2many(comodel_name='shop.invoice.line', inverse_name='invoice_id')
    selling_invoice = fields.Boolean(string='Selling Invoice', default=True)
    state = fields.Selection(string='State', default='draft',
                             selection=[('draft', 'Draft'),
                                        ('done', 'Done'),
                                        ('paid', 'Paid')])
    payment_method = fields.Selection(
        string='Payment method', required=True, default='cash',
        selection=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('points', 'Points')])

    @api.depends('invoice_line_ids')
    def _calc_total(self):
        for invoice in self:
            # s = 0
            # for line in invoice.invoice_line_ids:
            #     s += line.price * line.quantity
            # invoice.total = s
            invoice_line_totals = invoice.invoice_line_ids.mapped('total')
            invoice.total = sum(invoice_line_totals)

    @api.model
    def create(self, values):
        if values['selling_invoice']:
            code = self.env['ir.sequence'].next_by_code('out.invoice.cp')
        else:
            code = self.env['ir.sequence'].next_by_code('in.invoice.cp')
        values['invoice_nr'] = code
        res = super(ShopInvoice, self).create(values)
        return res

    def write(self, values):
        res = super(ShopInvoice, self).write(values)
        return res

    def unlink(self):
        for invoice in self:
            if invoice.state != 'draft':
                raise UserError('Invoice can not be deleted')
        res = super(ShopInvoice, self).unlink()
        return res

    def confirm_invoice(self):
        # if self.selling_invoice:
        #     for invoice_line in self.invoice_line_ids:
        #         invoice_line.product_id.quantity -= invoice_line.quantity
        # else:
        #     for invoice_line in self.invoice_line_ids:
        #         invoice_line.product_id.quantity += invoice_line.quantity
        # if self.selling_invoice:
        #     koef = -1
        # else:
        #     koef = 1
        koef = -1 if self.selling_invoice else 1
        for invoice_line in self.invoice_line_ids:
            invoice_line.product_id.quantity += koef * invoice_line.quantity
        self.state = 'done'
        if self.selling_invoice:
            self.pay_invoice()

    def pay_invoice(self):
        if self.selling_invoice:
            if self.payment_method == 'points':
                if self.client_id.points < self.total:
                    raise ValidationError('You have less points that required!')
                self.client_id.points -= self.total
            else:
                self.client_id.points += self.total / 100
        self.state = 'paid'


class ShopInvoiceLine(models.Model):
    _name = 'shop.invoice.line'

    product_id = fields.Many2one(comodel_name='shop.product', string='Product', required=True)
    invoice_id = fields.Many2one(comodel_name='shop.invoice', string='Invoice', required=True, ondelete='cascade')
    quantity = fields.Float(string='Quantity', default=1)
    price = fields.Float(string='Price')
    total = fields.Float(string='Total', compute='_compute_total')

    @api.depends('price', 'quantity')
    def _compute_total(self):
        for line in self:
            line.total = line.price * line.quantity

    @api.onchange('product_id')
    def onchange_method(self):
        if self.invoice_id.selling_invoice:
            self.price = self.product_id.selling_price
        else:
            self.price = self.product_id.purchase_price
