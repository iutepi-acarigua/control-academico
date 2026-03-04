from odoo import models, fields

class Inscription(models.Model):
    _name = 'registration.inscription'
    _description = 'Inscription Model for Registration Module'
    _inherits = {'res.partner': 'partner_id'}
    
    # Campo obligatorio para la delegación
    partner_id = fields.Many2one(
        'res.partner',
        string='Datos personales (nombre, dirección, etc.)',
        required=True,
        ondelete='cascade',           # Borra el partner si borras la inscripción
        auto_join=True,
    )
    
    partner_id = fields.Many2one('res.partner', string='Personal Information', required=True, ondelete='cascade') # ID persona
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled') #
    ], string='Status', default='draft', copy=False, required=True)
    birth_date = fields.Date(string='Birth Date', required=True, default=fields.Date.today)
    inscription_date = fields.Date(string='Inscription Date', required=True, default=fields.Date.today)
    number_phone = fields.Char(string='Phone Number', required=True, default='00000000000', size=11, copy=False, help='Enter a valid phone number with 11 digits')
    nationality = fields.Char(string='Nationality', required=True, default='Venezuelan', copy=False)
    birth_direction = fields.Char(string='Birth Direction', default='Unknown', copy=False, required=True)
    discapacity = fields.Boolean(string='Disability', default=False)
    discapacity_description = fields.Char(string='Disability Description', copy=False)
    room_phone = fields.Char(string='Room Phone', copy=False)
    person_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('employee', 'Employee')
    ], string='Person Type', default='student', copy=False, required=True)
    emergency_contact_name = fields.Char(string='Emergency Contact Name', copy=False)
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone', copy=False)
    emergency_contact_relationship = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('friend', 'Friend'),
        ('other', 'Other'),
        ('aunt', 'Aunt'),
        ('uncle', 'Uncle'),
        ('grandfather', 'Grandfather'),
        ('grandmother', 'Grandmother'),
        ('cousin', 'Cousin'),
        ('neighbor', 'Neighbor'),
        ('colleague', 'Colleague'),
        ('partner', 'Partner'),
        ('guardian', 'Guardian'),
        ('other', 'Other')
    ], string='Emergency Contact Relationship', copy=False)
    emergency_contact_direction = fields.Char(string='Emergency Contact Direction', copy=False)
    user_dni = fields.Binary(string="DNI Attachment", required=True, attachment=True)
    user_diploma = fields.Binary(string="Diploma Attachment", required=True, attachment=True)
    user_academic_record = fields.Binary(string="Academic Record Attachment", required=True, attachment=True)
    user_passport_photo = fields.Binary(string="Passport Photo", required=True, attachment=True)
    
    
    # Relación Many2one con el modelo Academic Condition, estas seran las condiciones academicas del estudiante, como por ejemplo: Regular, Sabatino, etc.
    # academic_condition = fields.Many2one('registration.academic_condition', string='Academic Condition', required=True)
    
    # Relación Many2one con el modelo Course, estas seran las materias a las que se inscribira el estudiante, osea las carreras
    # course_id = fields.Many2one('registration.course', string='Course', required=True)
    
    
    
    
    