from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'

    number_phone = fields.Char(string='Phone Number', size=11, help='11 digits valid phone number')
    birth_direction = fields.Char(string='Birth Direction')
    person_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('employee', 'Employee')
    ], string='Person Type', default='student')

    # Fields for Teachers
    cv_attachment = fields.Binary(string='Curriculum Vitae', attachment=True)
    specialty = fields.Char(string='Specialty/Area of Expertise')
    degree_level = fields.Selection([
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
        ('other', 'Other')
    ], string='Degree Level')

    _sql_constraints = [
        ('vat_unique', 'unique(vat)', 'The Identity Document (VAT) must be unique!'),
    ]

    @api.constrains('number_phone')
    def _check_number_phone(self):
        for record in self:
            if record.number_phone:
                if not record.number_phone.isdigit():
                    raise ValidationError(_("The phone number must contain only digits."))
                if len(record.number_phone) != 11:
                    raise ValidationError(_("The phone number must be exactly 11 digits long."))
