# -*- coding: utf-8 -*-
from odoo import http

# class Waybill(http.Controller):
#     @http.route('/waybill/waybill/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/waybill/waybill/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('waybill.listing', {
#             'root': '/waybill/waybill',
#             'objects': http.request.env['waybill.waybill'].search([]),
#         })

#     @http.route('/waybill/waybill/objects/<model("waybill.waybill"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('waybill.object', {
#             'object': obj
#         })