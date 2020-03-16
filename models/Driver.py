from odoo import fields, models, api


class Driver (models.Model):
    _inherit = 'hr.employee'

    waybill_ids = fields.One2many(comodel_name='shipping.waybill',
                                      inverse_name='driver_id',
                                      string='Waybill',
                                      required=False)