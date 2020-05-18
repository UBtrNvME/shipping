from odoo import fields, models, api


class Driver(models.Model):
    _inherit = 'hr.employee'

    waybill_ids = fields.One2many(comodel_name='shipping.waybill',
                                  inverse_name='driver_id',
                                  string='Waybill',
                                  required=False)
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle',
                                 string='Vehicle',
                                 required=False)
    #TODO connect driver class with vehicle class, in the way that we have constant driver team