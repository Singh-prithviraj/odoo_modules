from odoo import models, fields


class Subject(models.Model):
    _name = 'student.subject'
    _description = 'Student Subject'

    name = fields.Char(
        string='Subject Name',
        required=True
    )

    code = fields.Char(
        string='Subject Code'
    )

    description = fields.Text(
        string='Description'
    )

    student_ids = fields.Many2many(
        'student.student',
        string='Students'
    )
