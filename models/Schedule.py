from odoo import fields, models, api

class Schedule(models.Model):
    _name = 'shipping.schedule'
    _description = 'A part of the shipping module, which will be controlling generation of the waybills'

    name = fields.Char(string='Name', required=True)
    operation_ids = fields.One2many(string='Missions', comodel_name='shipping.schedule.operation',
                                  inverse_name='schedule_id')
    operation_count = fields.Integer(string='Mission count', compute='_compute_operation_count')
    waybill_ids = fields.One2many(string='Waybills', comodel_name='shipping.waybill', inverse_name='schedule_id')

    @api.one
    @api.depends('operation_ids')
    def _compute_operation_count(self):
        self.operation_count = len(self.operation_ids)


class Operation(models.Model):
    _name = 'shipping.schedule.operation'
    _description = 'A mission model, which will generate waybills'

    def _get_number(self):
        return self.schedule_id.operation_count + 1

    name = fields.Char(string='Mission name')
    schedule_id = fields.Many2one(string='Schedule', comodel_name='shipping.schedule')
    number = fields.Integer(string='Number', default=_get_number)
    waybill_ids = fields.One2many(string='Waybills', comodel_name='shipping.waybill', inverse_name='operation_id')
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    route_id = fields.Many2one(comodel_name='shipping.route', string='Route')
    """todo 
    operation_source = fields.Many2one(comodel_name='asset.asset', string='Operation Source Location', required=True)
    operation_destination = fields.Many2one(comodel_name='asset.asset', string='Operation Destination Location', required=True)
    operation_source_name = fields.Char(string="Route Source Name", compute='get_operation_name')

    @api.one
    @api.depends('operation_source')
    def get_operation_name(self):
        if self.operation_source:
            self.operation_source_name = self.operation_source.name
    """