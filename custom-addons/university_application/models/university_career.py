from odoo import models, fields

class UniversityCareer(models.Model):
    # Modelo para el catálogo de carreras disponibles
    _name = 'university.career'
    _description = 'University Career'

    name = fields.Char(string="Career Name", required=True, copy=False)
    description = fields.Text(string="Career Description")
