from odoo import fields, models, api


class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(selection=[('consu', 'Goods'),
                                       ('service', 'Service')])


class ProductInherited(models.Model):
    _inherit = 'product.product'

    route = fields.Many2one(comodel_name='shipping.route',
                            string='Route',
                            required=True)
    waybill_ids = fields.One2many(comodel_name='shipping.waybill',
                                  inverse_name='product_id',
                                  string='Waybill',
                                  required=False)
