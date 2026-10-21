from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    academy_reference = fields.Char(
        string='Academy Reference'
    )
