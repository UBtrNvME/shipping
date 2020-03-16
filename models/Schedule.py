from odoo import fields, models, api


class Schedule (models.Model):
    _name = 'shipping.schedule'
    _description = 'Schedule of the shipping tasks'

    name = fields.Char()
    


