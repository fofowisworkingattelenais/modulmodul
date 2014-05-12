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
    "name" : "Telenais Cash Advance - Purchase Invoice",
    "version" : "1.0",
    "author" : 'Siti Mawadah',
    "description": """
Implementasi proses CA - validasi CA membuat draft supplier invoice
- cancel CA juga delete Supplier Invoice (jika masih draft)
- saat pay invoice default amount pembayaran adalah cash advance
- jika cash advance sudah dibayar, maka default amount adalah residual
    """,
    "category" : "SMCUS Modul/Purchase",
    "website" : "http://www.telenais.com",
    "depends" : ["smcus_tel_cash_advance","account"],
    "update_xml" : [
        'purchase_invoice_view.xml'
    ],
    "active": False,
    "installable": True,
}
