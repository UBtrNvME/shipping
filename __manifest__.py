# -*- coding: utf-8 -*-
{
    'name': "waybill",

    'summary': """
        Model which introduces a new concept of the waybills to the fleet module""",

    'description': """
        Model which introduces a new entities to the fleet module, such as waybill, route and so far and so on.
        Those things make it possible to manage movement of your fleet, and its optimization
    """,

    'author': ["QZHub", "UBtrNvME"],
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Fleet Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}