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
    vehicle_id = fields.Many2one(string='Vehicle',
                                 comodel_name='fleet.vehicle',
                                 required=True)
    driver_id = fields.Many2one(string='Driver',
                                comodel_name='hr.employee')
    route_id = fields.Many2one(comodel_name='shipping.route',
                               string='Route',
                               required=False)
    operation_id = fields.Many2one(comodel_name='shipping.schedule.operation',
                                   string='Operation')
    schedule_id = fields.Many2one(comodel_name='shipping.schedule',
                                  string='Schedule')
    # log_fuel = fields.Many2one(comodel_name='vehicle_id.log.fuel')
    # Attributes=   :type= Related params
    odometer_before = fields.Float(string='Odometer before', related='vehicle_id.odometer', readonly=True)
    odometer_after = fields.Float(string='Odometer after')
    odometer_unit = fields.Selection(string='Odometer unit', related='vehicle_id.odometer_unit', readonly=True)
    license_plate = fields.Char(string='License plate', related='vehicle_id.license_plate', readonly=True)
    driver_identification = fields.Char(string='Driver\'s ID', related='driver_id.identification_id', readonly=True)
    fuel_start = fields.Float(string='Fuel mission start')
    fuel_end = fields.Float(string='Fuel mission end')
    fuel_type = fields.Selection(string='Fuel type', related='vehicle_id.log_fuel.cost_type')
    garage_id = fields.Char(string='Garage id')
    active_operation = fields.Many2one(comodel_name='shipping.schedule.operation')

    # @api.depends('vehicle_id')
    # @api.one
    # def _compute_fuel_start(self):
    #     self.fuel_start = self.vehicle_id.fuel_in_the_tank
    #
    # def _inverse_fuel_start(self):
    #     in_the_tank = self.vehicle_id.fuel_in_the_tank
    #     start = self.fuel_start
    #     if in_the_tank is not start:
    #         refilled = start - in_the_tank
    #         if refilled > 0:
    #             data = {
    #                 'vehicle_id': self.vehicle_id,
    #                 'liter'     : refilled,
    #                 'date'      : self.create_date
    #                 }
    #             self.env['fleet.vehicle.log.fuel'].sudo().write(data)
    #         else:
    #             raise ArithmeticError

    @api.model
    def create(self, vals):
        wb = super(Waybill, self).create(vals_list=vals)
        number = self._generate_number(wb.id)
        values = {
            'serial': self._generate_serial(wb.id),
            'number': number,
            'name'  : self._generate_name(number),
            }
        wb.update(values=values)
        return wb

    @api.multi
    def write(self, vals):
        if 'fuel_start' in vals and vals['fuel_start'] > 0:
            in_tank = self.vehicle_id.fuel_in_the_tank
            at_start = vals['fuel_start']
            refilled = at_start - in_tank
            if refilled:
                self._create_fuel_log(refilled)
                self.vehicle_id.fuel_in_the_tank = at_start
            #FIXME find a way to make this constraints work
            else:
                raise ValueError('Your value is lower than in the tank value!')
        else:
            vals['fuel_start'] = self.vehicle_id.fuel_in_the_tank
        if vals.get('fuel_end'):
            self.vehicle_id.fuel_in_the_tank = vals['fuel_end']
        if vals.get('odometer_after'):
            self._create_odometer_log(vals['odometer_after'])
        return super(Waybill, self).write(vals=vals)

    def _create_fuel_log(self, refilled):
        fuel_log = self.env['fleet.vehicle.log.fuel']
        for waybill in self:
            data = {
                'vehicle_id': waybill.vehicle_id.id,
                'liter'     : refilled,
                'date'      : waybill.create_date
                }
            fuel_log.create(data)

    def _create_odometer_log(self, odometer):
        data = {
            'date'      : fields.Date.today(),
            'vehicle_id': self.vehicle_id.id,
            'driver_id' : self.driver_id.id,
            'value'     : odometer,
            'unit'      : self.vehicle_id.odometer_unit
            }
        self.env['fleet.vehicle.odometer'].create(data)
