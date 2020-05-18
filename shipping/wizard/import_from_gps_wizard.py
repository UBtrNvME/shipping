from odoo import fields, models, api
from ..scripts import gps_api_loader as gal


class ImportFromGPS(models.Model):
    _name = 'shipping.import_from_gps'
    _description = 'imports vehicles from gps server'
    # imported_count = fields.Integer(string='Imported', default=0)
    # in_gps_count = fields.Integer(string='In gps system', default=0)
    # not_imported_count = fields.Integer(string='Not imported', compute='compute_not_imported')
    # models = []
    # brands = []
    # objects = []
    # not_imported = []
    # @api.multi
    # @api.depends('imported_count', 'in_gps_count')
    # def compute_not_imported(self):
    #     self.not_imported_count = self.in_gps_count - self.imported_count
    #
    # def get_models_and_brands(self):
    #     print("get_models_and_brands(self)")
    #     self.models = self.env['fleet.vehicle.model']
    #     self.brands = self.env['fleet.vehicle.model.brand']
    #
    # def get_not_imported_ids(self):
    #     print("get_not_imported_ids(self)")
    #     in_odoo = self.env['fleet.vehicle'].search([('digital_id', '!=', False)])
    #     self.models = self.env['fleet.vehicle.model']
    #     self.brands = self.env['fleet.vehicle.model.brand']
    #     for vehicle in self.objects:
    #         self.in_gps_count += 1
    #         if vehicle[0] not in in_odoo.digital_id:
    #             self.not_imported_count += 1
    #             s1 = vehicle[1]
    #             s2 = s1
    #             s2.split()
    #             brand = s2.pop(0)
    #             model = s2.join()
    #             new_model = False
    #             if s1 not in self.models.name:
    #                 if brand not in self.brands:
    #                     cr_brand = self.brands.create({'name': brand})
    #                 else:
    #                     cr_brand = self.brands.search([('name', '=', brand)])
    #                 new_model = self.models.create({'brand_id': cr_brand,
    #                                                 'name'    : model})
    #             data = {
    #                 'model_id'  : new_model,
    #                 'digital_id': vehicle[0]
    #                 }
    #             self.not_imported.append(data)
    #
    # def get_objects(self):
    #     print("get_objects(self)")
    #     result = gal.RequestWithRetry(lambda: gal.get_list_of_vehicles())
    #     childrens = result.json()['children']
    #     i = 0
    #     buf = []
    #     for info in childrens:
    #         buf.append(info['objects'])
    #         i += 1
    #     for i in range(0, i):
    #         for vehicle in buf[i]:
    #             self.objects.append([vehicle['terminal_id'], vehicle['name']])
    #
    # def import_vehicles_from_gps(self):
    #     for data in self.not_imported:
    #         self.env['fleet.vehicle'].create(data)
    #
    # def create(self):
    #     self.get_models_and_brands()
    #     print(self.models)
    #     self.get_objects()
    #     self.get_not_imported_ids()
    #     return super(ImportFromGPS, self).create()

    def import_vehicles_from_gps(self):
        result = gal.RequestWithRetry(lambda: gal.get_list_of_vehicles())
        childrens = result.json()['children']
        objects, i = {}, 0
        in_odoo = self.env['fleet.vehicle']
        vehicle_models = self.env['fleet.vehicle.model']
        vehicle_brands = self.env['fleet.vehicle.model.brand']
        for info in childrens:
            objects[i] = info['objects']
            i += 1
        from_gps, j = {}, 0
        for i in range(0, i):
            for vehicle in objects[i]:
                from_gps[j] = [vehicle['terminal_id'], vehicle['name']]
                j += 1
        for vehicle in from_gps:
            if in_odoo.search([('digital_id', '=', vehicle[0])]):
                s1 = vehicle[1]
                s2 = s1
                s2.split()
                brand = s2.pop(0)
                model = s2.join()
                new_model = False
                if s1 not in vehicle_models.name:
                    if brand not in vehicle_brands:
                        cr_brand = vehicle_brands.create({'name': brand})
                    else:
                        cr_brand = vehicle_brands.search([('name', '=', brand)])
                    new_model = vehicle_models.create({'brand_id': cr_brand,
                                                    'name'    : model})
                data = {
                    'model_id'  : new_model,
                    'digital_id': vehicle[0]
                    }
                self.env['fleet.vehicle'].create(data)
