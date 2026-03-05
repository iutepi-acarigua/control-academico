from odoo import fields, models, _

class InscriptionFormCondition(models.Model):
    _name = 'registration.form.condition'
    _description = 'Inscription Form Condition'

    name = fields.Char(string="Modality Name", required=True)
    description = fields.Char(string="Modality Description", required=True)
       