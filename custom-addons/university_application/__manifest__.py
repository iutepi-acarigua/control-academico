{
    'name': 'University Academic Management',
    'version': '19.0.1.0.0',
    'category': 'Education/Administration',
    'summary': 'Management of university applications, careers, and student enrollment.',
    'description': """
        University Academic Management System
        =====================================
        This module allows students to submit enrollment applications through the website.
        University administrators can review, approve, and manage these applications using a backend Kanban board.
    """,
    'author': 'CachapaGroup',
    'website': 'https://www.youruniversity.edu',
    'depends': [
        'base',
        'website',  # Required for QWeb pages, controllers, and routing
        'portal',   # Required for external user management and security roles
        'mail',     # Required to add the chatter (messaging/history) to the backend
    ],
    'data': [
        # 1. Security (Must be loaded first)
        'security/ir.model.access.csv',
        'security/rules.xml',

        # 2. Backend Views (Administrators)
        'views/backend/university_career_views.xml',
        'views/backend/university_application_views.xml',
        'views/backend/menu_views.xml',

        # 3. Frontend Views (Students / QWeb)
        'views/frontend/pages/landing_page.xml',
        'views/frontend/pages/enrollment_form.xml',
        'views/frontend/pages/success_page.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}