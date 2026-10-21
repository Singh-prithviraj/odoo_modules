from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcademyEnrollment(models.Model):
    _name = 'academy.enrollment'
    _description = 'Academy Enrollment'

    student_id = fields.Many2one(
        'academy.student',
        string='Student',
        required=True
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

    enrollment_date = fields.Date(
        string='Enrollment Date',
        required=True,
        default=fields.Date.today
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

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='State',
        default='draft',
        required=True
    )

    # RELATED FIELDS

    course_fees = fields.Float(
        string='Course Fees',
        related='course_id.course_fees',
        store=True
    )

    batch_name = fields.Char(
        string='Batch Name',
        related='batch_id.name',
        store=True
    )

    trainer_name = fields.Char(
        string='Trainer Name',
        related='batch_id.trainer_id.name',
        store=True
    )

    # COMPUTE

    @api.depends('fees', 'paid')
    def _compute_remaining(self):
        for enrollment in self:
            enrollment.remaining = enrollment.fees - enrollment.paid

    # INVERSE

    def _inverse_remaining(self):
        for enrollment in self:
            enrollment.paid = enrollment.fees - enrollment.remaining

    # ONCHANGE

    @api.onchange('course_id')
    def _onchange_course_id(self):
        if self.course_id:
            self.fees = self.course_id.course_fees

            if (
                self.batch_id
                and self.batch_id.course_id != self.course_id
            ):
                self.batch_id = False

    @api.onchange('batch_id')
    def _onchange_batch_id(self):
        if self.batch_id:
            self.course_id = self.batch_id.course_id
            self.fees = self.batch_id.course_id.course_fees

    @api.onchange('fees', 'paid')
    def _onchange_fees_paid(self):
        self.remaining = self.fees - self.paid

    # PYTHON CONSTRAINTS

    @api.constrains('paid', 'fees')
    def _check_paid(self):
        for enrollment in self:
            if enrollment.paid < 0:
                raise ValidationError(
                    'Paid amount cannot be negative.'
                )

            if enrollment.paid > enrollment.fees:
                raise ValidationError(
                    'Paid amount cannot be greater than Fees.'
                )

    @api.constrains('remaining')
    def _check_remaining(self):
        for enrollment in self:
            if enrollment.remaining < 0:
                raise ValidationError(
                    'Remaining amount cannot be negative.'
                )

    @api.constrains('enrollment_date', 'student_id')
    def _check_enrollment_date(self):
        for enrollment in self:
            if (
                enrollment.enrollment_date
                and enrollment.student_id
                and enrollment.enrollment_date
                < enrollment.student_id.admission_date
            ):
                raise ValidationError(
                    'Enrollment Date cannot be before Student Admission Date.'
                )

    @api.constrains('course_id', 'batch_id')
    def _check_course_batch(self):
        for enrollment in self:
            if (
                enrollment.course_id
                and enrollment.batch_id
                and enrollment.batch_id.course_id
                != enrollment.course_id
            ):
                raise ValidationError(
                    'Selected Batch must belong to the selected Course.'
                )

    @api.constrains('student_id', 'course_id', 'batch_id')
    def _check_student_course_batch(self):
        for enrollment in self:
            if enrollment.student_id:
                if (
                    enrollment.student_id.course_id
                    != enrollment.course_id
                ):
                    raise ValidationError(
                        'Enrollment Course must match the Student Course.'
                    )

                if (
                    enrollment.student_id.batch_id
                    != enrollment.batch_id
                ):
                    raise ValidationError(
                        'Enrollment Batch must match the Student Batch.'
                    )
