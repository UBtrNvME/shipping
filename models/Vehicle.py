from odoo import fields, models, api


class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    waybill_ids = fields.One2many(comodel_name='shipping.waybill',
                                  inverse_name='vehicle_id',
                                  string='Waybill',
                                  required=False)
    driver_ids = fields.One2many(comodel_name='hr.employee',
                                 inverse_name='vehicle_id',
                                 string='Driver',
                                 required=False)
    fuel_in_the_tank = fields.Float(string='Fuel in the tank')