from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    number_phone = fields.Char(string='Phone Number', size=11, help='11 digits valid phone number')
    birth_direction = fields.Char(string='Birth Direction')
    person_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('employee', 'Employee')
    ], string='Person Type', default='student')
