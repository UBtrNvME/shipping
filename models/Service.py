from odoo import fields, models, api


class Service(models.Model):
    _name = 'shipping.service'
    _description = 'Shipping Service'

    name = fields.Char()
    route = fields.Many2one(comodel_name='shipping.route',
                            string='Route',
                            required=True)
    type = fields.Selection(string='Type',
                            selection=[('type1', 'Type 1'),
                                       ('type2', 'Type 2'), ],
                            required=True)
    amount = fields.Integer(string='Amount',required=True)

