# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Route(models.Model):
    _name = 'shipping.route'

    name = fields.Char(string='Route name', readonly=True)
    locations = fields.Many2many(string='Locations', required=True, )
    customer = fields.Many2one(strign='Customer', required=True, comodel_name='res.partner')
    distance = fields.Integer(string='Distance', readonly=True, compute='_compute_distance')
    gps_dist_to_real = 1

    def _geospatial_dif(self, points_left):
        x = int(self.locations[points_left - 1].longitude) - int(self.locations[points_left - 2].longitude)
        y = int(self.locations[points_left - 1].latitude) - int(self.locations[points_left - 2].latitude)
        dist = (x * x + y * y) ** 0.5
        if points_left > 2:
            return dist + self._geospatial_dif(points_left - 1)
        else:
            return dist

    @api.depends('locations')
    @api.one
    def _compute_distance(self):

        points_left = len(self.locations)
        geospatial_distance = self._geospatial_dif(points_left=points_left)
        self.distance = geospatial_distance * self.gps_dist_to_real

    @api.model
    def create(self, values):
        name = values['name'] = self.locations[0].name + ' - ' + self.locations[len(self.locations) - 1]
        if self.env["waybill.route"].search([('name', '=', name)]) is True:
            values['name'] = name + f" ({self.client.name})"
        return super(Route, self).create(values)
