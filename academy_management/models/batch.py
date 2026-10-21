from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcademyBatch(models.Model):
    _name = 'academy.batch'
    _description = 'Academy Batch'

    name = fields.Char(
        string='Batch Name',
        required=True
    )

    course_id = fields.Many2one(
        'academy.course',
        string='Course',
        required=True
    )

    course_name = fields.Char(
        string='Course Name',
        related='course_id.name',
        store=True
    )

    course_fees = fields.Float(
        string='Course Fees',
        related='course_id.course_fees',
        store=True
    )

    trainer_id = fields.Many2one(
        'res.partner',
        string='Trainer',
        domain=[('is_trainer', '=', True)],
        required=True
    )

    start_date = fields.Date(
        string='Start Date',
        required=True
    )

    end_date = fields.Date(
        string='End Date',
        required=True
    )

    capacity = fields.Integer(
        string='Capacity',
        required=True
    )

    student_ids = fields.One2many(
        'academy.student',
        'batch_id',
        string='Students'
    )

    current_students = fields.Integer(
        string='Current Students',
        compute='_compute_current_students',
        store=True
    )

    available_seats = fields.Integer(
        string='Available Seats',
        compute='_compute_available_seats',
        store=True
    )

    status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('running', 'Running'),
            ('completed', 'Completed'),
        ],
        string='Status',
        default='draft',
        required=True
    )

    @api.depends('student_ids')
    def _compute_current_students(self):
        for batch in self:
            batch.current_students = len(batch.student_ids)

    @api.depends('capacity', 'current_students')
    def _compute_available_seats(self):
        for batch in self:
            batch.available_seats = (
                batch.capacity - batch.current_students
            )

    @api.constrains('capacity')
    def _check_capacity(self):
        for batch in self:
            if batch.capacity <= 0:
                raise ValidationError(
                    'Batch Capacity must be greater than 0.'
                )

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for batch in self:
            if (
                batch.start_date
                and batch.end_date
                and batch.end_date < batch.start_date
            ):
                raise ValidationError(
                    'End Date cannot be before Start Date.'
                )

    _batch_name_unique = models.Constraint(
        'UNIQUE(name)',
        'Batch Name must be unique.'
    )

    _batch_capacity_positive = models.Constraint(
        'CHECK(capacity > 0)',
        'Batch Capacity must be greater than 0.'
    )
