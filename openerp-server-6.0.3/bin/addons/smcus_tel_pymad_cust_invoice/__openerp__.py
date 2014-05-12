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
    "name" : "Telenais PYMAD - Customer Invoice",
    "version" : "1.2",
    "author" : 'Siti Mawadah',
    "description": """
3. Muncul tombol “Create Invoice” bila PYMAD sudah divalidasi.
- di customer invoice juga ditambahkan pymad_id untuk membedakan customer invoice
yang digenerate dari pymad atau bukan

- cancel PYMAD maka cancel invoice (jika dalam posisi draft)
1.1.1
bugs:
account nya harusnya receivable bukan payable

1.2
account di line langsung aja account pymad (bukan penjualan lagi) jika memang digenerate dr pymad
    """,
    "category" : "SMCUS Modul/Accounting",
    "website" : "http://www.telenais.com",
    "depends" : ["smcus_tel_pymad", "account"],
    "update_xml" : [
        "account_invoice_view.xml",
        "pymad_view.xml",
    ],
    "active": False,
    "installable": True,
}
