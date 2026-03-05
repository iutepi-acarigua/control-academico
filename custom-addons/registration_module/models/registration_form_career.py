from odoo import models, fields, _ 

class InscriptionFormCareer(models.Model):

    _name = 'registration.form.career'
    _description = 'Registration Form Career'

    career_name = fields.Char(string="Career Name", required=True, copy=False)
    description = fields.Char(string="Career Description", required=True, copy=False)
