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
    "name" : "Telenais PYMAD",
    "version" : "1.1",
    "author" : 'Siti Mawadah',
    "description": """
Pembuatan menu dasay PYMAD
Field pada form page PYMAD:
a. Reference : PYMAD/xyzd
    b. Customer: Customera
    c. Origin: SOabc
    d. SO No: SOxyz
    e. Tanggal PYMAD
    f. Tanggal SO
    g. User: PIC/Sales

3. Field pada PYMAD line: 
a.Job Index
    b. Expatriate
    c. Customer
    d. Qty
    e. UoM
    f. Unit Price
    g. SubTotal

    """,
    "category" : "SMCUS Modul/Accounting",
    "website" : "http://www.telenais.com",
    "depends" : ["account", "sale"],
    "update_xml" : [
        "pymad_view.xml",
    ],
    "active": False,
    "installable": True,
}
