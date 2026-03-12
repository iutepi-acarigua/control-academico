import base64
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class InscriptionController(http.Controller):

    # --- RUTA GET: Formulario (público, sin login)
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
        name = kwargs.get('name', '').strip()
        email = kwargs.get('email', '').strip()
        phone = kwargs.get('number_phone', '').strip()  # ← usa 'phone' en partner
        birth_date = kwargs.get('birth_date')
        inscription_date = kwargs.get('inscription_date') or fields.Date.today()
        nationality = kwargs.get('nationality', 'Venezuelan').strip()
        discapacity = kwargs.get('discapacity') == 'on'
        discapacity_description = kwargs.get('discapacity_description', '').strip()
        room_phone = kwargs.get('room_phone', '').strip()

        emergency_contact_name = kwargs.get('emergency_contact_name', '').strip()
        emergency_contact_phone = kwargs.get('emergency_contact_phone', '').strip()
        emergency_contact_relationship = kwargs.get('emergency_contact_relationship')
        emergency_contact_direction = kwargs.get('emergency_contact_direction', '').strip()

        modality_id = kwargs.get('modality_id')
        career_id = kwargs.get('career_id')

        # 2. Extraer archivos (deben coincidir con name en el <input>)
        user_dni_file = kwargs.get('user_dni')
        user_diploma_file = kwargs.get('user_diploma')
        user_academic_record_file = kwargs.get('user_academic_record')
        user_passport_photo_file = kwargs.get('user_passport_photo')

        # Helper para procesar archivos
        def _read_file(file_obj):
            if file_obj:
                try:
                    return base64.b64encode(file_obj.read())
                except Exception as e:
                    raise ValidationError(f"Error al leer el archivo: {file_obj.filename} → {str(e)}")
            return False

        try:
            user_dni_b64 = _read_file(user_dni_file)
            user_diploma_b64 = _read_file(user_diploma_file)
            user_academic_record_b64 = _read_file(user_academic_record_file)
            user_passport_photo_b64 = _read_file(user_passport_photo_file)

        except ValidationError as e:
            return request.render('university_application.error_page', {
                'message': e.name
            })

        # 3. Validaciones obligatorias (según modelo)
        errors = []
        if not name:
            errors.append("Nombre es obligatorio.")
        if not email:
            errors.append("Correo electrónico es obligatorio.")
        if not phone:
            errors.append("Teléfono es obligatorio.")
        if not modality_id:
            errors.append("Modalidad es obligatoria.")
        if not career_id:
            errors.append("Carrera es obligatoria.")
        if not user_dni_b64:
            errors.append("DNI (PDF) es obligatorio.")
        if not user_diploma_b64:
            errors.append("Diploma (PDF) es obligatorio.")
        if not user_academic_record_b64:
            errors.append("Historial académico (PDF) es obligatorio.")

        if errors:
            return request.render('university_application.error_page', {
                'errors': errors
            })

        # 4. Crear partner (datos personales)
        partner_vals = {
            'name': name,
            'email,
            'phone': phone,
            'image_1920': user_passport_photo_b64,  # asigna foto directamente al partner
        }
        partner = request.env['res.partner'].sudo().create(partner_vals)

        # 5. Crear solicitud
        try:
            application = request.env['university.application'].sudo().create({
                'partner_id': partner.id,
                'birth_date': birth_date,
                'inscription_date': inscription_date,
                'nationality': nationality,
                'discapacity': discapacity,
                'discapacity_description': discapacity_description,
                'room_phone': room_phone,
                'emergency_contact_name': emergency_contact_name,
                'emergency_contact_phone': emergency_contact_phone,
                'emergency_contact_relationship': emergency_contact_relationship,
                'emergency_contact_direction': emergency_contact_direction,
                'modality_id': int(modality_id),
                'career_id': int(career_id),
                'user_dni': user_dni_b64,
                'user_diploma': user_diploma_b64,
                'user_academic_record': user_academic_record_b64,
                'state': 'sent',
            })
        except Exception as e:
            return request.render('university_application.error_page', {
                'message': f"Error al crear la solicitud: {str(e)}"
            })

        # 6. Redirigir a página de éxito (o renderizarla)
        return request.redirect('/enrollment/success')