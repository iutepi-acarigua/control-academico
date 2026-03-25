from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class Application(models.Model):
    # Main model for enrollment applications
    _name = 'university.application'
    _description = 'University Enrollment Application'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Enables backend chatter
    _inherits = {'res.partner': 'partner_id'}
    
    # Mandatory relation with res.partner (Inheritance delegation)
    partner_id = fields.Many2one(
        'res.partner',
        string='Personal Information',
        required=True,
        ondelete='cascade',
        auto_join=True,
        help='Stores student personal details like name and address'
    )
    
    # State flow for Kanban view
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', copy=False, required=True, tracking=True)

    # Additional student data
    birth_date = fields.Date(string='Birth Date', required=True, default=fields.Date.today)
    inscription_date = fields.Date(string='Inscription Date', required=True, default=fields.Date.today)
    nationality = fields.Char(string='Nationality', required=True, default='Venezuelan')
    discapacity = fields.Boolean(string='Disability', default=False)
    discapacity_description = fields.Char(string='Disability Description')
    room_phone = fields.Char(string='Room Phone')

    # Emergency contact information
    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone')
    emergency_contact_relationship = fields.Selection([
        ('father', 'Father'), ('mother', 'Mother'), ('brother', 'Brother'),
        ('sister', 'Sister'), ('friend', 'Friend'), ('other', 'Other')
    ], string='Emergency Contact Relationship')
    emergency_contact_direction = fields.Char(string='Emergency Contact Direction')

    # Attached documents (Stored in filestore via attachment=True)
    user_dni = fields.Binary(string="DNI Attachment", attachment=True)
    user_diploma = fields.Binary(string="Diploma Attachment", attachment=True)
    user_academic_record = fields.Binary(string="Academic Record Attachment", attachment=True)
    cv_attachment = fields.Binary(string="CV Attachment", attachment=True)
    
    user_passport_photo = fields.Image(related='partner_id.image_1920', readonly=False, string="Passport Photo")
    
    # Relation with career and modality catalogs
    modality_id = fields.Many2one('university.modality', string='Modality')
    career_id = fields.Many2one('university.career', string='Career')
    
    # Constraints and Validations
    @api.constrains('partner_id', 'career_id', 'state')
    def _check_unique_application(self):
        """Prevents duplicates: a student cannot have more than one active application per career"""
        for record in self:
            if record.state != 'rejected' and record.person_type == 'student' and record.career_id:
                domain = [
                    ('partner_id', '=', record.partner_id.id),
                    ('career_id', '=', record.career_id.id),
                    ('state', '!=', 'rejected'),
                    ('id', '!=', record.id),
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(_("This student already has an active application for this career."))

    @api.constrains('birth_date')
    def _check_birth_date(self):
        """Validates that the student is at least 15 years old"""
        for record in self:
            if record.birth_date:
                today = date.today()
                age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
                if age < 15:
                    raise ValidationError(_("The student must be at least 15 years old to apply."))

    # Action methods for workflow
    def action_submit(self):
        """Transitions application from Draft to Sent after document validation"""
        for record in self:
            if record.person_type == 'student':
                if not record.user_dni or not record.user_diploma or not record.user_academic_record:
                     raise ValidationError(_("Please attach all required documents (DNI, Diploma, and Academic Record)."))
                if not record.career_id or not record.modality_id:
                     raise ValidationError(_("Career and Modality must be selected for Student applications."))
            elif record.person_type == 'teacher':
                if not record.user_dni or not record.cv_attachment:
                     raise ValidationError(_("Please attach all required documents (DNI and CV)."))
            else:
                if not record.user_dni:
                    raise ValidationError(_("Please attach the DNI document."))
            record.state = 'sent'

    def action_validate(self):
        """Validates the sent application"""
        for record in self:
            record.state = 'validated'

    def action_reject(self):
        """Rejects the application"""
        for record in self:
            record.state = 'rejected'

    def action_reset_to_draft(self):
        """Allows administrator to reset a rejected application to draft"""
        for record in self:
            if record.state == 'rejected':
                record.state = 'draft'
