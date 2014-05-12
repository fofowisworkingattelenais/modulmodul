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
    "name" : "Telenais Custom Purchase Order",
    "version" : "1.0",
    "author" : 'Siti Mawadah',
    "description": """
1. Penambahan field di Purchase Order Line (tree): Expatriate dan Customer Name. Apabila PO di-create dari SO, maka data Expatriate dan Customer di Sales Order juga muncul di PO.
2. Ganti string Description menjadi Job-Index
3. Field di Purchase Order Line (tree) setelah kustomisasi:
    a. Due Date 
    b.Job Index
    c. Expatriate
    d. Customer
    e. Qty
    f. UoM
    g. Unit Price
    h. SubTotal
    """,
    "category" : "SMCUS Modul/Purchase",
    "website" : "http://www.telenais.com",
    "depends" : ["purchase", "sale"],
    "update_xml" : [
        "purchase_view.xml",
    ],
    "active": False,
    "installable": True,
}
