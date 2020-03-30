from odoo import fields, models, api


class OpenWaybill(models.TransientModel):
    _name = 'shipping.open_waybill'
    _description = ''

    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle')
    operation_id = fields.Many2one(comodel_name='shipping.schedule.operation', readonly=True)
    driver_id = fields.Many2one(comodel_name='hr.employee')
    fuel_start = fields.Float()

    @api.onchange('vehicle_id')
    def _onchange_fuel_start(self):
        self.fuel_start = self.vehicle_id.fuel_in_the_tank

    def create_waybill(self):
        op = self.operation_id
        driver = self.driver_id
        vehicle = self.vehicle_id
        data = {
            'customer_id' : op.customer_id.id,
            'schedule_id' : op.schedule_id.id,
            'operation_id': op.id,
            'route_id'    : op.route_id.id,
            'driver_id'   : driver.id,
            'vehicle_id'  : vehicle.id,
            }
        waybill = self.env['shipping.waybill'].create(data)
        waybill.write({'fuel_start': self.fuel_start})
        self.env['shipping.schedule.operation'].search([('id', '=', op.id)]).write({'active_waybill': waybill.id})
        # waybill.write({'fuel_start': self.fuel_start})


class CloseWaybill(models.TransientModel):
    _name = 'shipping.close_waybill'

    waybill_id = fields.Many2one(comodel_name='shipping.waybill', readonly=True)
    fuel_end = fields.Float()
    odometer_after = fields.Float()

    def close_waybill(self):
        waybill = self.env['shipping.waybill'].search([('id', '=', self.waybill_id.id)], limit=1)
        data = {
            'fuel_end'      : self.fuel_end,
            'odometer_after': float(self.odometer_after)
            }
        print(data)
        waybill.write(data)
        self.env['shipping.schedule.operation'].search([('active_waybill', '=', waybill.id)]).write(
            {'active_waybill': False})
