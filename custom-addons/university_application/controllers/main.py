import base64
from odoo import http
from odoo.http import request

class InscriptionController(http.Controller):
    # Endpoint para renderizar el formulario de inscripción
    @http.route('/enrollment', type='http', auth="public", website=True)
    def enrollment_form(self, **kwargs):
        careers = request.env['university.career'].sudo().search([])
        modalities = request.env['university.modality'].sudo().search([])
        return request.render('university_application.enrollment_page_template', {
            'careers': careers,
            'modalities': modalities
        })

    # Endpoint para procesar el envío del formulario (POST)
    @http.route('/enrollment/submit', type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def submit_enrollment(self, **kwargs):
        # 1. Extraer archivos y convertirlos a Base64 para guardarlos en Odoo
        dni_file = kwargs.get('user_dni')
        diploma_file = kwargs.get('user_diploma')
        
        # 2. Crear el registro en university.application
        # Se usa .sudo() porque el usuario del sitio web suele ser público
        vals = {
            'name': kwargs.get('name'),
            'email': kwargs.get('email'),
            'number_phone': kwargs.get('number_phone'),
            'birth_date': kwargs.get('birth_date'),
            'career_id': int(kwargs.get('career_id')),
            'modality_id': int(kwargs.get('modality_id')),
            'user_dni': base64.b64encode(dni_file.read()) if dni_file else False,
            'user_diploma': base64.b64encode(diploma_file.read()) if diploma_file else False,
            'state': 'sent' # Al enviar desde el formulario web, queda en estado 'Enviado'
        }
        
        new_application = request.env['university.application'].sudo().create(vals)
        return request.render('university_application.success_page_template', {'application': new_application})
