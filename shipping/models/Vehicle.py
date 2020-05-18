from odoo import fields, models, api
from ..scripts import gps_api_loader as gal
import json


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
    digital_id = fields.Char(string='Vehicle\' ID in GPS system')

    latitude = fields.Float()
    longitude = fields.Float()
    geo_position = fields.Char(string='Geo Position', compute="_compute_geo_position")

    # Changing default fields
    def _get_default_driver(self):
        default_driver = self.env['res.partner'].search([('name', '=', 'Default Driver')])
        if not default_driver:
            dr = self.env['res.partner'].create({'name': 'Default Driver'})
            return dr.id
        return default_driver.id

    driver_id = fields.Many2one(default=_get_default_driver)

    @api.one
    @api.depends('latitude', 'longitude')
    def _compute_geo_position(self):
        geo = {u'position': {u'lat': self.latitude, u'lng': self.longitude}, u'zoom': 12}
        self.geo_position = json.dumps(geo)

    def get_state_from_gps(self):
        # print("state of %s vehicle received" % (self.digital_id))
        result = gal.RequestWithRetry(lambda: gal.get_vehicle_state(self.digital_id))
        self.latitude = result.json()['lastGPS']['latitude']
        self.longitude = result.json()['lastGPS']['longitude']
        # print(result.json())
        return result

    def get_statistics_from_gps(self, time_start, time_end):
        start, end = time_start.timestamp(), time_end.timestamp()
        # print(f"statistics on period ({start} - {end}) received for {self.digital_id}")
        result = gal.RequestWithRetry(
            lambda: gal.get_vehicle_statistic_on_period(self.digital_id, time_start, time_end))
        # print(result.json())
        return result

    def import_vehicles_from_gps(self):
        result = gal.RequestWithRetry(lambda: gal.get_list_of_vehicles())
        # childrens = result.json()['children']
        # objects, i = {}, 0
        # for info in childrens:
        #     objects[i] = info['objects']
        #     i += 1
        # from_gps, j = {}, 0
        # for i in range(0, i):
        #     for vehicle in objects[i]:
        #         from_gps[j] = [vehicle['terminal_id'], vehicle['name']]
        #         j += 1
        # in_odoo = self.env['fleet.vehicle'].search([('digital_id', '!=', False)])
        # vehicle_models = self.env['fleet.vehicle.model']
        # vehicle_brands = self.env['fleet.vehicle.model.brand']
        # for vehicle in from_gps:
        #     if vehicle[0] not in in_odoo.digital_id:
        #         s1 = vehicle[1]
        #         s2 = s1
        #         s2.split()
        #         brand = s2.pop(0)
        #         model = s2.join()
        #         new_model = False
        #         if s1 not in vehicle_models.name:
        #             if brand not in vehicle_brands:
        #                 cr_brand = vehicle_brands.create({'name': brand})
        #             else:
        #                 cr_brand = vehicle_brands.search([('name', '=', brand)])
        #             new_model = vehicle_models.create({'brand_id': cr_brand,
        #                                                'name'    : model})
        #         data = {
        #             'model_id'  : new_model,
        #             'digital_id': vehicle[0]
        #             }
        #         self.env['fleet.vehicle'].create(data)
