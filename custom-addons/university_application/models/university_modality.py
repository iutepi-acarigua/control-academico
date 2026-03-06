from odoo import fields, models

class UniversityModality(models.Model):
    # Nombre técnico unificado para la modalidad de inscripción
    _name = 'university.modality'
    _description = 'University Inscription Modality'

    name = fields.Char(string="Modality Name", required=True)
    description = fields.Char(string="Modality Description", required=True)
