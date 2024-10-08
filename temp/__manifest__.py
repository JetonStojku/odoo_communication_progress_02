{
    'name': 'Communication Progress Temp',
    'version': '1.0',
    'summary': 'Summery',
    'description': 'Description',
    'category': 'Category',
    'author': 'Author',
    'website': 'Website',
    'depends': ['base'],
    'data': [
        'security\security.xml',
        'data\invoice_sequence.xml',
        'views\client_view.xml',
        'views\employee_view.xml',
        'views\product_view.xml',
        'views\category_view.xml',
        'views\invoice_view.xml',
        'wizard\invoice_report_view.xml',
        'wizard\product_report_view.xml',
        'report\invoice_report.xml',
        'report\product_report.xml',
        'security\ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
