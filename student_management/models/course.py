from odoo import models, fields


class StudentCourse(models.Model):
    _name = 'student.course'
    _description = 'Student Course'

    name = fields.Char(
        string='Course Name',
        required=True
    )

    description = fields.Text(
        string='Description'
    )

    duration = fields.Integer(
        string='Duration'
    )

    student_ids = fields.One2many(
        'student.student',
        'course_id',
        string='Students'
    )
