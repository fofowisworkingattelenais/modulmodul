# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : "Custom Report PT. FD INDUSTRI",
    "version" : "1.0",
    "author" : 'Faris Bassam',
    "description": """
                    Custom Report Include ::
                        1. Purchase Order report FD
                        2. Delivery Order report FD
                        3. Customer Invoice report FD
                        4. Quotation / Sale Order FD
                    """,
    "category" : "Purchase Management",
    "website" : "http://wopopwopop.wordpress.com",
    'depends': ['stock', 'process', 'procurement', 'purchase'],
    "update_xml" : [

        "menu/stock_menu.xml",
        "menu/invoice_menu.xml",
        "menu/sale_menu.xml",
        "menu/purchase_menu.xml",

        "view/purchase_view.xml",
        "view/sale_order_view.xml",
        "view/stock_view.xml",
        "view/invoice_view.xml",

    ],
    "active": False,
    "installable": True,
}
