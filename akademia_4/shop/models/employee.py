# -*- coding: utf-8 -*-
from odoo import fields, models


class ShopEmployee(models.Model):
    _name = 'shop.employee'
    _description = 'Employee'

    name = fields.Char(string='Employee Name', required=True)
    surname = fields.Char(string='Employee Surname', required=True)
    position = fields.Selection([
        ('seller', 'Seller'),
        ('manager', 'Manager')
    ], string='Status', default='seller')
    salary = fields.Integer(string='Salary', required=True, default=0)
    email = fields.Char(string='Email')
    points = fields.Integer(string='Points')
