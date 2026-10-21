from odoo import api, fields, models
from odoo.exceptions import ValidationError


class OpenAcademySession(models.Model):
    _name = "openacademy.session"
    _description = "Details for each session of all the courses"

    name = fields.Char(
        string="Title",
        required=True,
    )

    md_start_date = fields.Date(
        string="Start Date",
        default=fields.Date.today,
    )

    md_end_date = fields.Date(
        string="End Date",
    )

    md_duration = fields.Float(
        string="Duration",
    )

    seats = fields.Integer(
        string="Number of Seats",
    )

    # Computed Field
    md_taken_seats = fields.Float(
        string="Taken Seats",
        compute="_compute_taken_seats",
        store=True,
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    md_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
        ],
        string="State",
        default="draft",
        required=True,
    )

    # Many2one
    course_id = fields.Many2one(
        "openacademy.course",
        string="Course",
        required=True,
        ondelete="cascade",
    )

    course_subject = fields.Char(
        string="Course Subject",
        related="course_id.md_subject",
        store=True,
    )

    # Many2many
    md_attendee_id = fields.Many2many(
        "res.partner",
        string="Attendees",
    )

    md_instructor_id = fields.Many2one(
        "res.partner",
        string="Instructor",
    )

    md_session_ids = fields.One2many(
        "openacademy.session",
        "md_instructor_id",
        string="Sessions"
    )

    @api.depends("seats", "md_attendee_id")
    def _compute_taken_seats(self):
        for record in self:
            if not record.seats:
                record.md_taken_seats = 0.0
            else:
                record.md_taken_seats = (
                    100 * len(record.md_attendee_id) / record.seats
                )

    @api.constrains("md_attendee_id", "md_instructor_id", "seats")
    def _validate_attendees(self):

        if self.md_instructor_id in self.md_attendee_id:
            raise ValidationError("Instructor {} cannot join course as attendee!!!!".format(
                self.md_instructor_id.name))
        if len(self.md_attendee_id) > self.seats:
            raise ValidationError(
                "No. of attendees can not exceed more than no. of seats")

    _check_seats = models.Constraint(
        'CHECK(seats > 0)',
        'Number of Seats must be at least 1'
    )
