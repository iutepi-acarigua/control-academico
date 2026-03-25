import base64
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class UniversityController(http.Controller):
    # Endpoint para la Landing Page
    @http.route('/university', type='http', auth="public", website=True)
    def university_index(self, **kwargs):
        # Buscamos todas las carreras para el catálogo de la landing
        careers = request.env['university.career'].sudo().search([])
        return request.render('university_application.landing_page_template', {
            'careers': careers
        })

    # Endpoint para renderizar el formulario de inscripción
    @http.route('/enrollment', type='http', auth="public", website=True)
    def enrollment_form(self, **kwargs):
        careers = request.env['university.career'].sudo().search([])
        modalities = request.env['university.modality'].sudo().search([])
        return request.render('university_application.enrollment_page_template', {
            'careers': careers,
            'modalities': modalities,
        })

    # --- RUTA POST: Procesar inscripción (REQUIERE LOGIN → auth="user")
    @http.route('/enrollment/submit', type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def submit_enrollment(self, **kwargs):
        # 1. Extraer datos del formulario
        person_type = kwargs.get('person_type', 'student')
        name = kwargs.get('name', '').strip()
        email = kwargs.get('email', '').strip()
        vat = kwargs.get('vat', '').strip()
        phone = kwargs.get('number_phone', '').strip()
        birth_date = kwargs.get('birth_date')
        
        # Datos académicos (solo para estudiantes)
        modality_id = kwargs.get('modality_id') if person_type == 'student' else False
        career_id = kwargs.get('career_id') if person_type == 'student' else False

        # Datos profesionales (solo para profesores)
        specialty = kwargs.get('specialty', '').strip() if person_type == 'teacher' else False
        degree_level = kwargs.get('degree_level') if person_type == 'teacher' else False

        # 2. Extraer archivos
        user_dni_file = kwargs.get('user_dni')
        user_diploma_file = kwargs.get('user_diploma')
        user_academic_record_file = kwargs.get('user_academic_record')
        user_passport_photo_file = kwargs.get('user_passport_photo')
        cv_attachment_file = kwargs.get('cv_attachment')

        def _read_file(file_obj):
            if file_obj:
                try:
                    return base64.b64encode(file_obj.read())
                except Exception:
                    return False
            return False

        user_dni_b64 = _read_file(user_dni_file)
        user_diploma_b64 = _read_file(user_diploma_file)
        user_academic_record_b64 = _read_file(user_academic_record_file)
        user_passport_photo_b64 = _read_file(user_passport_photo_file)
        cv_attachment_b64 = _read_file(cv_attachment_file)

        # 3. Validaciones condicionales
        errors = []
        if not name or not email or not phone or not vat:
            errors.append("Datos personales incompletos.")
        
        if not user_dni_b64:
            errors.append("El DNI es obligatorio para todos los registros.")

        if person_type == 'student':
            if not career_id or not modality_id:
                errors.append("Debe seleccionar Carrera y Modalidad.")
            if not user_diploma_b64 or not user_academic_record_b64:
                errors.append("Los documentos académicos son obligatorios para estudiantes.")
        
        if person_type == 'teacher':
            if not cv_attachment_b64:
                errors.append("El Curriculum Vitae es obligatorio para profesores.")

        if errors:
            return request.render('university_application.error_page', {'errors': errors})

        # Check if vat already exists to prevent SQL Unique Constraint error
        existing_partner = request.env['res.partner'].sudo().search([('vat', '=', vat)], limit=1)
        if existing_partner and existing_partner.email != email:
             errors.append("El Documento de Identidad (RIF/Cedula) ya está registrado con otro correo electrónico.")
             return request.render('university_application.error_page', {'errors': errors})

        # 4. Partner
        partner = request.env['res.partner'].sudo().search([('vat', '=', vat)], limit=1)
        if not partner:
            partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            
        partner_vals = {
            'name': name,
            'email': email,
            'vat': vat,
            'number_phone': phone,
            'person_type': person_type,
            'image_1920': user_passport_photo_b64,
            'specialty': specialty,
            'degree_level': degree_level,
            'cv_attachment': cv_attachment_b64,
        }
        if partner:
            partner.sudo().write(partner_vals)
        else:
            partner = request.env['res.partner'].sudo().create(partner_vals)

        # 5. Solicitud (Si es estudiante)
        if person_type == 'student':
            try:
                request.env['university.application'].sudo().create({
                    'partner_id': partner.id,
                    'birth_date': birth_date,
                    'modality_id': int(modality_id),
                    'career_id': int(career_id),
                    'user_dni': user_dni_b64,
                    'user_diploma': user_diploma_b64,
                    'user_academic_record': user_academic_record_b64,
                    'state': 'sent',
                })
            except Exception as e:
                return request.render('university_application.error_page', {'message': str(e)})

        return request.redirect('/enrollment/success')

        # 6. Redirigir a página de éxito (o renderizarla)
        return request.redirect('/enrollment/success')