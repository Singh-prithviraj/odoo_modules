from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_trainer = fields.Boolean(
        string='Is Trainer',
        default=False
    )

    trainer_specialization = fields.Char(
        string='Trainer Specialization'
    )

    trainer_experience = fields.Integer(
        string='Trainer Experience'
    )

    trainer_joining_date = fields.Date(
        string='Trainer Joining Date'
    )
