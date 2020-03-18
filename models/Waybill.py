# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Waybill(models.Model):
    _name = 'shipping.waybill'
    _rec_name = 'serial'

    serial_format = 4

    def _generate_serial(self, id):
        return str(id).rjust(self.serial_format, '0')

    def _generate_number(self, id):
        return str(id)

    def _generate_name(self, number):
        return "WAYBILL OF THE CAR #" + str(number)

    name = fields.Char(string='Name', readonly=True)
    serial = fields.Char(string='Serial number', readonly=True)
    number = fields.Char(string='Waybill number', readonly=True)
    # Attributes=   :type= Time
    start_time_planned = fields.Datetime(string='Start time',
                                         readonly=True,
                                         help="Time of the start of the shipping mission, according to schedule")
    end_time_planned = fields.Datetime(string='End time',
                                       readonly=True,
                                       help="Time of the end of the shipping mission, according to schedule")
    start_time_actual = fields.Datetime(string='End time',
                                        readonly=True,
                                        help="Time of the end of the shipping mission")
    end_time_actual = fields.Datetime(string='End time',
                                      readonly=True,
                                      help="Time of the end of the shipping mission")
    # Attributes=   :type= Objects
    customer_id = fields.Many2one(comodel_name='res.partner',
                                  string='Customer',
                                  required=True)
    vehicle_id = fields.Many2one(string='Vehicle', comodel_name='fleet.vehicle', required=True)
    driver_id = fields.Many2one(string='Driver', comodel_name='hr.employee')
    # Attributes=   :type= Related params
    odometer_before = fields.Float(string='Odometer before', related='vehicle_id.odometer', readonly=True)
    odometer_after = fields.Float(string='Odometer after', related='vehicle_id.odometer', readonly=True)
    odometer_unit = fields.Selection(string='Odometer unit', related='vehicle_id.odometer_unit', readonly=True)
    license_plate = fields.Char(string='License plate', related='vehicle_id.license_plate', readonly=True)
    driver_identification = fields.Char(string='Driver\'s ID', related='driver_id.identification_id', readonly=True)

    @api.model
    def create(self, vals):
        wb = super(Waybill, self).create(vals_list=vals)
        number = self._generate_number(wb.id)
        values = {'serial': self._generate_serial(wb.id),
                  'number': number,
                  'name'  : self._generate_name(number)}
        wb.update(values=values)
        return wb
