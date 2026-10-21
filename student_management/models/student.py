from odoo import models, fields


class Student(models.Model):
    _name = 'student.student'
    _description = 'Student'

    name = fields.Char(
        string='Name',
        required=True
    )

    email = fields.Char(
        string='Email'
    )

    phone = fields.Char(
        string='Phone'
    )

    age = fields.Integer(
        string='Age'
    )

    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        string='Gender'
    )

    course_id = fields.Many2one(
        'student.course',
        string='Course'
    )


subject_ids = fields.Many2many(
    'student.subject',
    string='Subjects'
)
