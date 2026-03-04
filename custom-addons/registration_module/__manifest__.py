{
    'name': 'Registration Module',
    'version': '19.0.0.1',
    'description': 'Registration module for Odoo from study case',
    'summary': 'Registration module for Odoo from study case',
    'author': '5to Semestre PR25-3',
    'website': 'None',
    'license': 'LGPL-3',
    'category': 'Others',
    'depends': [
        'base',
        'contacts'
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/registration_inscription_views.xml",
        "views/registration_menus.xml"
    ],
    'installable': True,
    'auto_install': False,
    'application': True
    
}