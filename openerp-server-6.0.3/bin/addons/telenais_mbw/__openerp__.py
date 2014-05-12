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
    'name': 'Telenais - MBW',
    'version': '1.0',
    'category': 'Telenais/MBW',
    'description': """

    """,
    'author': 'Telenais Aset Tangguh',
    'website': 'www.telenais.com',
    'depends': ['account','account_accountant','account_voucher','analytic','base','base_setup','board',
                'decimal_precision','hr','mrp','process','procurement','product','purchase','purchase_requisition',
                'resource','sale','stock','web_livechat', 'project'],
    'init_xml': [],
    'update_xml': ['security/mbw_group_security.xml',
                   'security/account_menu_security.xml',
                   'security/account_voucher_menu_security.xml',
                   'security/decimal_precision_menu_security.xml',
                   'security/hr_menu_security.xml',
                   'security/mrp_menu_security.xml',
                   'security/product_menu_security.xml',
                   'security/base_menu_security.xml',
                   'security/board_menu_security.xml',
                   'security/process_menu_security.xml',
                   'security/procurement_menu_security.xml',
                   'security/sale_menu_security.xml',
                   'security/purchase_menu_security.xml',
                   'security/purchase_requsition_menu_security.xml',
                   'security/resource_menu_security.xml',
                   'security/stock_menu_security.xml',
                   'security/project_menu_security.xml',
                   'security/dir_security.xml',
                   'security/usr_warehouse_security.xml',
                   'security/usr_purchase_security.xml',
                   'security/usr_sale_security.xml',
                   'security/usr_mrp_security.xml',
                   'security/usr_hrd_security.xml',
                   'security/usr_project_security.xml',
                   'security/mgr_acc_security.xml',
                   'security/mgr_hrd_security.xml',
                   'security/mgr_security.xml',
                   'view/view_SaleOrder.xml',
                   'view/view_PurchaseOrders.xml',],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
