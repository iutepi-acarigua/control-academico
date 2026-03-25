from odoo import models, fields

class UniversityCareer(models.Model):
    # Modelo para el catálogo centralizado de carreras 
    _name = 'university.career'
    _description = 'University Career'
    _order = 'name'

    name = fields.Char(string="Nombre de la Carrera", required=True, copy=False)
    code = fields.Char(string="Código de Carrera", required=True)
    
    # Información Administrativa
    faculty = fields.Selection([
        ('engineering', 'Ingeniería / Tecnología'),
        ('business', 'Ciencias Administrativas')
    ], string='Facultad', required=True)
    
    active = fields.Boolean(
        string='Disponible para Registro', 
        default=True,
        help="Si está marcado, se mostrará en el formulario de inscripción."
    )

    # Información Técnica
    description = fields.Html(string="Perfil de la Carrera")
    duration_semesters = fields.Integer(string="Duración (Semestres)", default=6)