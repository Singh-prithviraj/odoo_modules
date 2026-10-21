from odoo import models, fields, api


class AcademyCourse(models.Model):
    _name = 'academy.course'
    _description = 'Academy Course'

    name = fields.Char(
        string='Course Name',
        required=True
    )

    course_code = fields.Char(
        string='Course Code',
        required=True
    )

    course_fees = fields.Float(
        string='Course Fees',
        required=True
    )

    duration = fields.Integer(
        string='Duration'
    )

    description = fields.Text(
        string='Description'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    total_students = fields.Integer(
        string='Total Students',
        compute='_compute_total_students',
        store=True
    )

    student_ids = fields.One2many(
        'academy.student',
        'course_id',
        string='Students'
    )

    @api.depends('student_ids')
    def _compute_total_students(self):
        for course in self:
            course.total_students = len(course.student_ids)

    # SQL Constraints 
    _course_code_unique = models.Constraint(
        'UNIQUE(course_code)',
        'Course Code must be unique.'
    )

    _course_fees_positive = models.Constraint(
        'CHECK(course_fees >= 0)',
        'Course Fees cannot be negative.'
    )
