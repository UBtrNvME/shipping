from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    waybill_ids = fields.One2many(comodel_name='shipping.waybill',
                                  inverse_name='customer_id',
                                  string='Waybill',
                                  required=False)