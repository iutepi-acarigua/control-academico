{
    'name': 'University Enrollment Management',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage university applications, careers, and modalities.',
    'description': """
        University Enrollment System
        ============================
        * Public enrollment form for students.
        * Kanban management for applications.
        * Document management (PDF attachments).
        * Career and modality catalogs.
    """,
    'author': 'CachapaGroup',
    'depends': ['base', 'website', 'mail', 'portal', 'auth_signup'],
    'data': [
        # Seguridad (Cargar primero)
        'security/ir.model.access.csv',

        # Vistas del Backend (Administradores)
        'views/backend/university_subject_views.xml',
        'views/backend/university_career_views.xml',
        'views/backend/university_application_reports.xml',
        'views/backend/university_application_report_template.xml',
        'views/backend/university_application_views.xml',
        'views/backend/res_partner_views.xml',
        'views/backend/menus_views.xml',

        # Vistas del Frontend (Estudiantes / QWeb)
        'views/frontend/pages/landing_page.xml',
        'views/frontend/pages/enrollment.xml',
        'views/frontend/pages/success_page.xml',
        'views/frontend/portal_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'university_application/static/src/scss/styles.scss',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
