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
    "name" : "Kartu Stock report v7",
    "version" : "1.2",
    "author" : 'Faris Bassam',
    "description": """
Custom Report::
    1.Custom laporan kartu stock""",
    "category" : "SMCUS Modul/Warehouse",
    "website" : "http://wopopwopop.wordpress.com",
    "depends" : ["stock"],
    "update_xml" : [

        "wizard/wizard_kartu_stock.xml",
        "wizard/wizard_mutasi_barang.xml",
        "wizard/wizard_mutasi_barang_gb.xml",
        "wizard/wizard_posisi_barang.xml",
        "wizard/wizard_laporan_posisi_barang_wip.xml",
        "wizard/wizard_saldo_inventory.xml",

    ],
    "active": False,
    "installable": True,
}
