from odoo import fields, models

class UniversityModality(models.Model):
    # Unified technical name for enrollment modality
    _name = 'university.modality'
    _description = 'University Inscription Modality'

    name = fields.Char(string="Modality Name", required=True)
    description = fields.Char(string="Modality Description", required=True)
