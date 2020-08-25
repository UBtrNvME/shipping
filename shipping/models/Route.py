from odoo import fields, models, api
from odoo.exceptions import ValidationError

"""
class RLC(models.Model):
    _name = 'shipping.route.rlc'
    route_id = fields.Many2one(comodel_name='shipping.route',
                               string='Route')
    location_id = fields.Many2one(comodel_name='asset.asset',
                               string='Location')
    index = fields.Integer(string='Index')
"""


class Route(models.Model):
    _name = 'shipping.route'
    _rec_name = 'route_name'

    operation_ids = fields.Many2many(comodel_name='shipping.schedule.operation',
                                    #inverse_name='route_id',
                                    string='Operation',
                                    required=False)
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    """todo
    route_source_name = fields.Char(string="Route Source Name", compute='get_route_name')
    route_destination_name = fields.Char(string="Route Destination Name", compute='get_route_name')
    """
    route = fields.One2many(comodel_name="shipping.route.line", string="Line", inverse_name='route_ids')
    route_name = fields.Char(string="Route Name", compute='get_route_name')

    @api.one
    @api.depends('route')
    def get_route_name(self):
        name = ""
        if self.route:
            for point in self.route:
                name += point.source_location.name + " - "
            name += point.destination_location.name
            self.route_name = name


    @api.one
    @api.constrains('route')
    def check_route(self):
        for i in range(len(self.route)-1):
            if self.route[i].destination_location != self.route[i+1].source_location:
                raise ValidationError('Added Route is invalid')


class Line(models.Model):
    _name = 'shipping.route.line'
    route_ids = fields.Many2one(comodel_name='shipping.route',
                                    string='Route',
                                    required=False)
    source_location = fields.Many2one(comodel_name='asset.asset', string='Source Location', required=True)
    destination_location = fields.Many2one(comodel_name='asset.asset', string='Destination Location', required=True)

    """line_name = fields.Char(string="Route Name", compute='get_line_name')


    @api.one
    @api.depends('source_location', 'destination_location')
    def get_route_name(self):
        if self.source_location and self.destination_location:
            self.line_name = self.source_location.name + " -> " \
                                   + self.destination_location.name"""