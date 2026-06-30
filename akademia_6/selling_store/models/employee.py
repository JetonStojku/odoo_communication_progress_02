from odoo import fields, models, api


class SellingStoreEmployee(models.Model):
    _name = 'selling_store.employee'
    _description = 'Employee'

    name = fields.Char(string='Name')
    surname = fields.Char(string='Surname')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Char(string='Address')
    birthday = fields.Date(string='Birthday')
    role = fields.Selection(string='Role', required=True,
                            selection=[('cashier', 'Cashier'),
                                       ('manager', 'Manager'),
                                       ('admin', 'Admin')])
    salary = fields.Float(string='Salary', digits=(12, 4))
    start_day = fields.Date(string='Start Day', required=True)
