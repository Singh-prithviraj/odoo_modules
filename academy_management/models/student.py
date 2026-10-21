from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcademyStudent(models.Model):
    _name = 'academy.student'
    _description = 'Academy Student'

    name = fields.Char(
        string='Student Name',
        required=True
    )

    student_code = fields.Char(
        string='Student Code',
        required=True
    )

    email = fields.Char(
        string='Email'
    )

    phone = fields.Char(
        string='Phone'
    )

    dob = fields.Date(
        string='Date of Birth'
    )

    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        string='Gender'
    )

    admission_date = fields.Date(
        string='Admission Date',
        required=True,
        default=fields.Date.today
    )

    course_id = fields.Many2one(
        'academy.course',
        string='Course',
        required=True
    )

    batch_id = fields.Many2one(
        'academy.batch',
        string='Batch',
        required=True
    )

    course_name = fields.Char(
        string='Course Name',
        related='course_id.name',
        store=True
    )

    batch_name = fields.Char(
        string='Batch Name',
        related='batch_id.name',
        store=True
    )

    fees = fields.Float(
        string='Fees',
        required=True
    )

    paid = fields.Float(
        string='Paid'
    )

    remaining = fields.Float(
        string='Remaining',
        compute='_compute_remaining',
        inverse='_inverse_remaining',
        store=True
    )

    age = fields.Integer(
        string='Age',
        compute='_compute_age'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    # COMPUTE

    @api.depends('fees', 'paid')
    def _compute_remaining(self):
        for student in self:
            student.remaining = student.fees - student.paid

    @api.depends('dob')
    def _compute_age(self):
        today = fields.Date.today()

        for student in self:
            if student.dob:
                student.age = (
                    today.year - student.dob.year
                    - (
                        (today.month, today.day)
                        < (student.dob.month, student.dob.day)
                    )
                )
            else:
                student.age = 0

    # INVERSE

    def _inverse_remaining(self):
        for student in self:
            student.paid = student.fees - student.remaining

    # ONCHANGE

    @api.onchange('course_id')
    def _onchange_course_id(self):
        if self.course_id:
            self.fees = self.course_id.course_fees

            if self.batch_id and self.batch_id.course_id != self.course_id:
                self.batch_id = False

    @api.onchange('batch_id')
    def _onchange_batch_id(self):
        if self.batch_id:
            self.course_id = self.batch_id.course_id
            self.fees = self.batch_id.course_id.course_fees

            if (
                self.batch_id.current_students
                >= self.batch_id.capacity
            ):
                return {
                    'warning': {
                        'title': 'Batch Full',
                        'message': 'This batch has reached its capacity.'
                    }
                }

    @api.onchange('fees', 'paid')
    def _onchange_fees_paid(self):
        self.remaining = self.fees - self.paid

    # PYTHON CONSTRAINTS

    @api.constrains('dob')
    def _check_dob(self):
        today = fields.Date.today()

        for student in self:
            if student.dob and student.dob > today:
                raise ValidationError(
                    'Date of Birth cannot be in the future.'
                )

    @api.constrains('fees')
    def _check_fees(self):
        for student in self:
            if student.fees < 0:
                raise ValidationError(
                    'Fees cannot be negative.'
                )

    @api.constrains('paid', 'fees')
    def _check_paid(self):
        for student in self:
            if student.paid < 0:
                raise ValidationError(
                    'Paid amount cannot be negative.'
                )

            if student.paid > student.fees:
                raise ValidationError(
                    'Paid amount cannot be greater than Fees.'
                )

    @api.constrains('remaining')
    def _check_remaining(self):
        for student in self:
            if student.remaining < 0:
                raise ValidationError(
                    'Remaining amount cannot be negative.'
                )

    @api.constrains('course_id', 'batch_id')
    def _check_course_batch(self):
        for student in self:
            if (
                student.course_id
                and student.batch_id
                and student.batch_id.course_id != student.course_id
            ):
                raise ValidationError(
                    'Selected Batch must belong to the selected Course.'
                )
    # SQL CONSTRAINTS

    _student_code_unique = models.Constraint(
        'UNIQUE(student_code)',
        'Student Code must be unique.'
    )
