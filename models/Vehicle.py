from odoo import fields, models, api
from ..scripts import gps_api_loader as gal


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
    tank_value = fields.Float(string='Tank Volume')
    digital_id = fields.Integer(string='Vehicle\' ID in GPS system', default=336007258)


    def get_state_from_gps(self):
        result = gal.RequestWithRetry(lambda: gal.get_vehicle_state(self.digital_id))
        return result

    def get_statistics_from_gps(self, time_start, time_end):
        result = gal.RequestWithRetry(
            lambda: gal.get_vehicle_statistic_on_period(self.digital_id, time_start, time_end))
        return result
