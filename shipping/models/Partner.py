from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    operation_ids = fields.One2many(comodel_name='shipping.schedule.operation',
                                    inverse_name='customer_id',
                                    string='Waybill',
                                    required=False)
    waybill_ids = fields.One2many(comodel_name='shipping.waybill',
                                  inverse_name='customer_id',
                                  string='Waybill',
                                  required=False)
    #TODO need to prepare product model, as well as its views