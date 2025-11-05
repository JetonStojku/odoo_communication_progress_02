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

