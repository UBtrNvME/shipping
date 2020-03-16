from odoo import fields, models, api


class Contract (models.Model):
    _name = 'shipping.contract'
    _description = 'Contract between customer and supplier'

    name = fields.Char()
    


