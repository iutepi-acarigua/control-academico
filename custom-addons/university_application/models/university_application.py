from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Application(models.Model):
    # Modelo principal para las solicitudes de inscripción
    _name = 'university.application'
    _description = 'University Enrollment Application'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Habilita el chatter del backend
    _inherits = {'res.partner': 'partner_id'}
    
    # Relación obligatoria con res.partner (Delegación de herencia)
    partner_id = fields.Many2one(
        'res.partner',
        string='Personal Information',
        required=True,
        ondelete='cascade',
        auto_join=True,
        help='Stores student personal details like name and address'
    )
    
    # Flujo de estados para la vista Kanban
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', copy=False, required=True, tracking=True)

    # Datos adicionales del estudiante
    birth_date = fields.Date(string='Birth Date', required=True, default=fields.Date.today)
    inscription_date = fields.Date(string='Inscription Date', required=True, default=fields.Date.today)
    nationality = fields.Char(string='Nationality', required=True, default='Venezuelan')
    discapacity = fields.Boolean(string='Disability', default=False)
    discapacity_description = fields.Char(string='Disability Description')
    room_phone = fields.Char(string='Room Phone')

    # Información de contacto de emergencia
    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone')
    emergency_contact_relationship = fields.Selection([
        ('father', 'Father'), ('mother', 'Mother'), ('brother', 'Brother'),
        ('sister', 'Sister'), ('friend', 'Friend'), ('other', 'Other')
    ], string='Emergency Contact Relationship')
    emergency_contact_direction = fields.Char(string='Emergency Contact Direction')

    # Documentos adjuntos (Almacenados en filestore mediante attachment=True)
    user_dni = fields.Binary(string="DNI Attachment", required=True, attachment=True)
    user_diploma = fields.Binary(string="Diploma Attachment", required=True, attachment=True)
    user_academic_record = fields.Binary(string="Academic Record Attachment", required=True, attachment=True)
    
    user_passport_photo = fields.Image(related='partner_id.image_1920', readonly=False, string="Passport Photo")
    
    # Relación con el catálogo de carreras y modalidades
    modality_id = fields.Many2one('university.modality', string='Modality', required=True)
    career_id = fields.Many2one('university.career', string='Career', required=True)
    
    # Métodos de acción para el flujo de trabajo
    def action_submit(self):
        """Pasa la solicitud de Borrador a Enviado tras validar documentos"""
        for record in self:
            if not record.user_dni or not record.user_diploma:
                 raise ValidationError("Please attach all required documents.")
            record.state = 'sent'

    def action_validate(self):
        """Valida la solicitud enviada"""
        for record in self:
            record.state = 'validated'

    def action_reject(self):
        """Rechaza la solicitud"""
        for record in self:
            record.state = 'rejected'

    def action_reset_to_draft(self):
        """Permite al administrador resetear una solicitud rechazada"""
        for record in self:
            if record.state == 'rejected':
                record.state = 'draft'
