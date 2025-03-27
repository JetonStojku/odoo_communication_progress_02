from odoo import fields, models


class ShopEmployee(models.Model):
    _name = 'shop.employee'

    name = fields.Char(string='Employee name', required=True)
    surname = fields.Char(string='Surname', required=True)
    wage = fields.Integer(string='Wage', default=35_000)
    position = fields.Selection(string='Position', required=True,
                                selection=[('seller', 'Seller'),
                                           ('manager', 'Manager')])
    start_date = fields.Date(string='Start Date', required=False, default=lambda self: fields.Date.today())
    user_id = fields.Many2one(comodel_name='res.users', string='User')
