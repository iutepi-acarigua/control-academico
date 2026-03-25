from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class UniversitySubject(models.Model):
    # Subject Catalog Model
    _name = 'university.subject'
    _description = 'University Subject'

    name = fields.Char(string="Subject Name", required=True)
    code = fields.Char(string="Subject Code", required=True)
    credits = fields.Integer(string="Credits", default=3)
    
    prerequisite_ids = fields.Many2many(
        'university.subject', 
        'subject_prerequisite_rel', 
        'subject_id', 
        'prerequisite_id', 
        string="Prerequisites"
    )
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The subject code must be unique!'),
    ]
    
    @api.constrains('prerequisite_ids')
    def _check_prerequisites(self):
        """Prevents a subject from being its own prerequisite"""
        for record in self:
            if record in record.prerequisite_ids:
                raise ValidationError(_("A subject cannot be a prerequisite for itself."))

class UniversityCareerLine(models.Model):
    # Career Subject Lines (Subjects assigned to periods)
    _name = 'university.career.line'
    _description = 'Career Subject Line'
    _order = 'period, subject_id'

    career_id = fields.Many2one('university.career', string="Career", ondelete='cascade', required=True)
    subject_id = fields.Many2one('university.subject', string="Subject", required=True)
    period = fields.Integer(string="Period (Semester/Year)", required=True, default=1)
    is_elective = fields.Boolean(string="Elective?", default=False)

    @api.constrains('career_id', 'subject_id', 'period')
    def _check_unique_subject_per_period(self):
        """Prevents a subject from being duplicated in the same career and period"""
        for record in self:
            domain = [
                ('career_id', '=', record.career_id.id),
                ('subject_id', '=', record.subject_id.id),
                ('period', '=', record.period),
                ('id', '!=', record.id),
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(_("The subject '%s' is already assigned to this career in period %s.") % (record.subject_id.name, record.period))
