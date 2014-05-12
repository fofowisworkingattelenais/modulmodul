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
    'name': 'Telenais - Candika',
    'version': '1.0',
    'category': 'Telenais/Candika',
    'description': """

    """,
    'author': 'Telenais Aset Tangguh',
    'website': 'www.telenais.com',
    'depends': ['sale','purchase','account_accountant','mrp','account', 'partner_credit_limit'],
    'init_xml': [],
    'update_xml': [ 'security/candika_security.xml',
                    'workflow/workflow_SaleOrder.xml',
                    'wizard/wizard_penjualan_15_cust_terbaik.xml',
                    'wizard/wizard_penjualan_customer.xml',
                    'wizard/wizard_penjualan_salesman.xml',
                    'wizard/wizard_penjualan_produk.xml',
                    'wizard/wizard_pareto_salesman_brand.xml',
                    'wizard/wizard_pareto_customer_brand.xml',
                    'wizard/wizard_pareto_branch_brand.xml',
                    'wizard/wizard_pareto_salesman_customer.xml',
                    'wizard/wizard_pareto_ntr_branch.xml',                    
                    'view/view_Perusahaan.xml',
                    'view/view_Product.xml',
                    'view/view_SaleOrder.xml',
                    'view/view_CashRegister.xml',
                    'view/view_ManufactureOrder.xml',
                    'view/view_SaleShop.xml',
                    'menu/menu_BankStatements.xml',
                    'menu/menu_CashRegister.xml',
                    'menu/menu_Sales.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
