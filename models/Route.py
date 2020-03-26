from odoo import fields, models, api


class RLC(models.Model):
    _name = 'shipping.route.rlc'
    route_id = fields.Many2one(comodel_name='shipping.route',
                               string='Route')
    location_id = fields.Many2one(comodel_name='asset.asset',
                               string='Location')
    index = fields.Integer(string='Index')

class Route(models.Model):
    _name = 'shipping.route'

    location_ids = fields.Many2many(comodel_name='asset.asset',
                                    string='Location',
                                    )
    operation_ids = fields.One2many(comodel_name='shipping.schedule.operation',
                                    inverse_name='route_id',
                                    string='Operation',
                                    required=False)