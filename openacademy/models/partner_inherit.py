from odoo import fields, models


class OpenacademyPartnerInherit(models.Model):
    _inherit = "res.partner"

    md_qualification = fields.Char(
        string="Qualification",
        required=True,
        default="Graduate"
    )

    md_experience = fields.Float(
        string="Experience",
        digits=(12, 1)
    )

    md_session_ids = fields.One2many(
        "openacademy.session",
        "md_instructor_id",
        string="Sessions"
    )

    md_is_instructor = fields.Boolean(
        string="Is Instructor"
    )