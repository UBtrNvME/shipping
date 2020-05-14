from odoo import fields, models, api


class NewModule(models.Model):
    _inherit = 'product.product'

    name = fields.Char()



