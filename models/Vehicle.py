from odoo import fields, models, api


class Vehicle (models.Model):
    _inherit = 'fleet.vehicle'

    waybill_ids = fields.One2many(comodel_name='shipping.waybill',
                                      inverse_name='vehicle_id',
                                      string='Waybill',
                                      required=False)
    


