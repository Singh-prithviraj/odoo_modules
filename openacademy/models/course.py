from odoo import fields, models


class OpenAcademyCourse(models.Model):
    _name = "openacademy.course"
    _description = "Open Academy Course"

    # This is the display name of the Course
    name = fields.Char(
        string="Course Title",
        required=True,
    )

    md_subject = fields.Char(
        string="Subject",
    )

    md_dob = fields.Date(
        string="Date Of Birth",
    )

    md_contact = fields.Char(
        string="Contact Number",
    )

    md_email = fields.Char(
        string="Email",
    )

    md_address = fields.Text(
        string="Address",
    )

    md_notes = fields.Text(
        string="Notes",
    )

    # One Course can have many Sessions
    session_ids = fields.One2many(
        "openacademy.session",
        "course_id",
        string="Sessions",
    )