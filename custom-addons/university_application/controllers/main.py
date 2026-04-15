import base64
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class UniversityController(http.Controller):
    # Endpoint para la Landing Page (Página Raíz)
    @http.route('/', type='http', auth="public", website=True, sitemap=True)
    def university_index(self, **kwargs):
        careers = request.env['university.career'].sudo().search([])
        return request.render('university_application.landing_page_template', {'careers': careers})

    @http.route('/enrollment', type='http', auth="user", website=True)
    def enrollment_form(self, **kwargs):
        careers = request.env['university.career'].sudo().search([])
        modalities = request.env['university.modality'].sudo().search([])
        return request.render('university_application.enrollment_page_template', {
            'careers': careers,
            'modalities': modalities,
            'errors': kwargs.get('errors', []),
            'values': kwargs.get('values', {}),
        })

    @http.route('/enrollment/submit', type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def submit_enrollment(self, **kwargs):
        # 1. Usar el partner del usuario logueado directamente
        partner = request.env.user.partner_id
        
        person_type = kwargs.get('person_type', 'student')
        name = kwargs.get('name', '').strip()
        email = kwargs.get('email', '').strip()
        vat = kwargs.get('vat', '').strip()
        
        # 2. Extraer archivos
        def _read_file(file_obj):
            return base64.b64encode(file_obj.read()) if file_obj and hasattr(file_obj, 'read') else False

        user_dni_b64 = _read_file(kwargs.get('user_dni'))
        user_diploma_b64 = _read_file(kwargs.get('user_diploma'))
        user_academic_record_b64 = _read_file(kwargs.get('user_academic_record'))

        # 3. Validaciones
        errors = []
        if not name or not vat: errors.append("Nombre y DNI son obligatorios.")
        if person_type == 'student' and (not kwargs.get('career_id') or not user_dni_b64):
            errors.append("Faltan datos o documentos de la carrera.")

        if errors:
            return self.enrollment_form(errors=errors, values=kwargs)

        # 4. Actualizar el perfil del usuario actual
        partner.sudo().write({
            'name': name,
            'vat': vat,
            'email': email,
            'person_type': person_type,
        })

        # 5. Crear solicitud vinculada al usuario
        if person_type == 'student':
            request.env['university.application'].sudo().create({
                'partner_id': partner.id,
                'birth_date': kwargs.get('birth_date'),
                'modality_id': int(kwargs.get('modality_id')),
                'career_id': int(kwargs.get('career_id')),
                'user_dni': user_dni_b64,
                'user_diploma': user_diploma_b64,
                'user_academic_record': user_academic_record_b64,
                'state': 'sent',
            })

        return request.redirect('/enrollment/success')

    @http.route('/enrollment/success', type='http', auth="user", website=True)
    def enrollment_success(self, **kwargs):
        application = request.env['university.application'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ], order='create_date desc', limit=1)
        return request.render('university_application.success_page_template', {'application': application})

class UniversityPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        # Sudo necesario para contar correctamente en el portal
        values['application_count'] = request.env['university.application'].sudo().search_count([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        return values

    @http.route(['/my/applications', '/my/applications/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_applications(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        # Usamos sudo para asegurar que el portal pueda LEER sus registros
        domain = [('partner_id', '=', request.env.user.partner_id.id)]
        applications = request.env['university.application'].sudo().search(domain)
        
        values.update({
            'applications': applications,
            'page_name': 'application',
            'default_url': '/my/applications',
        })
        return request.render("university_application.portal_my_applications", values)
