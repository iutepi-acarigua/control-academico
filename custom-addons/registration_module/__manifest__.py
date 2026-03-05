{
    'name': 'Registration Module',
    'version': '19.0.0.1',
    'description': 'Registration module for Odoo from study case',
    'summary': 'Registration module for Odoo from study case',
    'author': '5to Semestre PR25-3',    
    'website': 'None',
    'license': 'LGPL-3',
    'category': 'Education',
    'depends': [
        'base',
        'contacts'
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/backend/registration_inscription_views.xml",
        "views/backend/registration_menus.xml",
        "views/frontend/templates.xml"
        "views/frontend/pages/landing_page.xml",
        "views/frontend/pages/success_page.xml",
        'views/frontend/pages/enrollment_form.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True
    
}