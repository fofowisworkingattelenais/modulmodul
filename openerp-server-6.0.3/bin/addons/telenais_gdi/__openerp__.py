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
    'name': 'Telenais - GDI',
    'version': '1.0',
    'category': 'Telenais/GDI',
    'description': """

    """,
    'author': 'Telenais Aset Tangguh',
    'website': 'www.telenais.com',
    'depends': ['purchase','purchase_requisition','mrp','hr','product_manufacturer'],
    'init_xml': [],
    'update_xml': ['report_purchase_order.xml',
                    'security/ir.model.access.csv',
                    'data/data_DocumentType.xml',
                   'wizard/wizard_import_product.xml',
                   'wizard/wizard_konversi_harga_produk.xml',
                   'wizard/wizard_purchase_requisition.xml',
                   'wizard/wizard_split_purchase_requisition.xml',
                   'wizard/wizard_cetak_rekap_pemasukan_barang.xml',
                   'wizard/wizard_cetak_rekap_pengeluaran_barang.xml',
                   'view/view_ProductProduct.xml',
                   'view/view_InternalMove.xml',
                   'view/view_IncomingShipment.xml',
                   'view/view_PurchaseOrders.xml',
                   'view/view_mrpBom.xml',
                   'view/view_PurchaseRequisition.xml',
                   'view/view_PurchaseRequisitionLine.xml',
                   'view/view_DeliveryOrder.xml',
                   'menu/menu_PurchaseRequisition.xml',
                   'menu/menu_product.xml',
                   'menu/menu_Warehouse.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
