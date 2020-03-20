from odoo import fields, models, api


class Location(models.Model):
    _inherit = 'asset.asset'

    route_id = fields.Many2many(comodel_name='shipping.route',
                               string='Route',
                               required=False)