from odoo import models, fields

class UniversityCareer(models.Model):
    # Model for the available careers catalog
    _name = 'university.career'
    _description = 'University Career'

    name = fields.Char(string="Career Name", required=True, copy=False)
    description = fields.Text(string="Career Description")
    
    # Relation with subjects and periods
    subject_ids = fields.One2many('university.career.line', 'career_id', string="Subject Lines")
