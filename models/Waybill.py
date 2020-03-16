# -*- coding: utf-8 -*-

from odoo import models, fields, api

serial_format = 5


class Waybill(models.Model):
    _name = 'shipping.waybill'
    _rec_name = 'serial'

    @api.one
    def _generate_serial(self):
        return str(self.id).rjust(self.serial_format, '0')

    @api.one
    def _generate_number(self):
        return str(self.id)
    @api.one
    def _generate_name(self):
        return "Waybill #" + str(self.number)

    name = fields.Char(string='Name', readonly=True, default=_generate_name)
    serial = fields.Char(string='Serial number', readonly=True, default=_generate_serial)
    number = fields.Char(string='Waybill number', readonly=True, default=_generate_number)
    customer_id = fields.Many2one(comodel_name='res.partner',
                                  string='Customer',
                                  required=True)
    service_ids = fields.Many2many(comodel_name='shipping.service',
                                   string='Service',
                                   relation='waybill_service_rel',
                                   column1='waybill_id',
                                   column2='service_id')
    vehicle_id = fields.Many2one(string='Vehicle', comodel_name='fleet.vehicle', required=True)
    driver_id = fields.Many2one(string='Driver', comodel_name='hr.employee', onchnage='_onchange_vehicle')
    route1_ids = fields.Many2many(comodel_name='shipping.route',
                                  string='Route',
                                  relation='route_waybill_rel',
                                  column1='route_id',
                                  column2='waybill_id')

    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        self.fuel_type = 'Diesel' if self.vehicle.type is 'Heavy' else 'Gasoline'
        if len(self.vehicle.driver) < 1:
            self.vehicle = False
        else:
            # TODO: make a logic that will make it possible to automoate process of choosing driver
            self.driver = self.vehicle.driver[1]
