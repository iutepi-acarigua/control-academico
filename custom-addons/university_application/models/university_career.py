from odoo import models, fields, _ 

class UniversityCareer(models.Model):

    _name = 'university.career'
    _description = 'University Form Career'

    career_name = fields.Char(string="Career Name", required=True, copy=False)
    description = fields.Char(string="Career Description", required=True, copy=False)
