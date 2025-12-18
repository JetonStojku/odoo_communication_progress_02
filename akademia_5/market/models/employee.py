# -*- coding: utf-8 -*-
from odoo import fields, models


class MarketEmployee(models.Model):
    """ This model represents employee."""
    _name = 'market.employee'
    _description = 'Employee'

    name = fields.Char(string='Employee Name', required=True)
    surname = fields.Char(string='Employee Surname', required=True)
    position = fields.Selection(selection=[
        ('seller', 'Seller'),
        ('admin', 'Admin')
    ], string='Position', default='seller', required=True)
    salary = fields.Float(string='Salary', digits=(12, 4))
    rate = fields.Float(string='Rate')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    description = fields.Text(string='Description')
    user_id = fields.Many2one(comodel_name='res.users', string='User', required=True)


class ResUsers(models.Model):
    _inherit = 'res.users'

    employee_ids = fields.One2many(comodel_name='market.employee', string='Employee', inverse_name='user_id')
