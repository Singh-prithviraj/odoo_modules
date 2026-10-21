from odoo import fields, models


class AIService(models.Model):
    _name = 'ai.business.service'
    _description = 'Business Service'

    name = fields.Char(
        string='Service Name',
        required=True
    )

    description = fields.Text(
        string='Description'
    )

    duration = fields.Integer(
        string='Duration (Minutes)',
        default=30
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )
