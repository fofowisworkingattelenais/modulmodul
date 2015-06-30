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
    "name" : "Stock Move Varience",
    "version" : "1.0",
    "author" : 'Faris Bassam',
    "description": """
    add new field cost price, total cost price, on stock move view
    and add report calculation varience
    """,
    "category" : "SMCUS Modul/Warehouse",
    "website" : "http://wopopwopop.wordpress.com",
    "depends" : ["stock"],
    "update_xml" : [

        "view/stock_view.xml",
        "wizard/wizard_stock_variance.xml",


    ],
    "active": False,
    "installable": True,
}
