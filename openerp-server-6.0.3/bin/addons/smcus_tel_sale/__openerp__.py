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
    "name" : "Telenais Custom Sale Order",
    "version" : "1.1",
    "author" : 'Siti Mawadah',
    "description": """
1. Penambahan field di Sales Order Line (tree): address_allotment_id (string=Expatriate)
2. Pemindahan field address_allotment_id di sale.order.form dari “Extra Info” ke “Order Line”
4. Ganti string Description menjadi Job Index
5. Field di Sales Order Line (tree) setelah kustomisasi:
    a. Job Index
    b. Expatriate
    c. Qty
    d. UoM
    e. Unit Price
    f. SubTotal
    """,
    "category" : "SMCUS Modul/Sales",
    "website" : "http://www.telenais.com",
    "depends" : ["sale"],
    "update_xml" : [
        "sale_view.xml",
    ],
    "active": False,
    "installable": True,
}
