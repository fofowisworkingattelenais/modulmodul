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
    "name" : "Telenais Cash Advance",
    "version" : "1.3",
    "author" : 'Siti Mawadah',
    "description": """
1. Field pada form page CA:
    a. Reference : CA/xyzd
    b. Supplier: Supplier1
    c. Origin: POxyz:SOabc
    d. PO No: POxyz
    e. Tanggal CA
    f. Tanggal PO
    g. User: PIC/Sales

2. Field pada CA line:
a.Job Index
    b. Expatriate
    c. Customer
    d. Qty
    e. UoM
    f. Unit Price
    g. SubTotal

3. Field pada footer
    a. Jumlah Cash Advance : 50% dari SubTotal (default)
    b. Tombol validasi CA

1.3
Cash advance tidak mencantumkan tax
Only delete Draft Cash Advance
    """,
    "category" : "SMCUS Modul/Purchase",
    "website" : "http://www.telenais.com",
    "depends" : ["purchase", "sale"],
    "update_xml" : [
        "cash_advance_view.xml",
        "ca_report.xml",
    ],
    "active": False,
    "installable": True,
}
