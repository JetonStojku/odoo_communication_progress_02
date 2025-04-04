{
    'name': 'CP Shop',
    'version': '1.0',
    'summary': 'CP Shop Summery',
    'description': 'CP Shop Description',
    'category': 'Sales',
    'author': 'Jeton',
    'website': 'Website',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/invoice_sequence.xml',
        'views/client_view.xml',
        'views/employee_view.xml',
        'views/product_view.xml',
        'views/category_view.xml',
        'views/invoice_view.xml',
        'report/invoice_report_view.xml',
        'wizard/invoice_report_wizard_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
