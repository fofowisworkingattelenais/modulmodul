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
    'name': 'Report SCP',
    'version': '1.1',
    'author': 'PT. Telenais Tangguh(Faris Bassam)',
    'category': 'Telenais/Base',
    'complexity': 'easy',
    'website': 'http://telenais.com',
    'description': """
    Modul untuk kustomisasi untuk implementasi di PT. Titis Sampurna
    
    6.0.3, 6.0.4, dan 6.1 compability
    """,
    'images': [],
    'depends': [
                            # 'ar_base_perusahaan',
                            'account_accountant', 
                            'account_voucher', 
                            'account_analytic_plans', 
                            'account_budget', 
                            'purchase',
                            'project',
                            'product_manufacturer',
                            'purchase_requisition',
                            # 'ar_account_taxform'
    ],
    'init_xml': [],
    'update_xml': [ 
                    # 'security/data_Group.xml',
                    # 'security/ir.model.access.csv',
                    # 'data/data_CompanyHeader.xml',
                    # 'data/data_VoucherType.xml',
                    # 'workflow/workflow_PurchaseOrder.xml',
                    # 'workflow/workflow_AccountVoucher.xml',
                    'ajlb_report.xml',
                    # 'wizard/wizard_import_perbaikan_data_product.xml',
                    # 'wizard/wizard_laporan_cashflow_direct.xml',
                    # 'wizard/wizard_sales_report.xml',
                    # 'wizard/wizard_department_report.xml',
                    'wizard/wizard_ledger.xml',
                    # 'wizard/wizard_income_statement.xml',
                    # 'wizard/wizard_indirect_cashflow.xml',
                    # 'wizard/wizard_report_actual_vs_budget.xml',
                    # 'wizard/wizard_sales_report_customer.xml',
                    # 'wizard/wizard_report_account_payable_aging.xml',
                    # 'wizard/wizard_report_account_receivable.xml',
                    'wizard/wizard_kartu_stock.xml',
                    # 'wizard/wizard_stok_total.xml',
                    # 'wizard/wizard_report_account_payable_aging_by_vendor.xml',
                    # 'wizard/wizard_report_account_receivable_by_customer.xml',
                    # 'wizard/wizard_balance_sheet.xml',
                    'wizard/wizard_trial_balance.xml',
                    # 'wizard/wizard_batch_product_change.xml',
                    # 'wizard/wizard_import_move_line.xml',
                    # 'wizard/wizard_purchase_requisition_line.xml',

                    # 'view/view_ResPartner.xml',
                    # 'view/view_AccountMove.xml',
                    # 'view/view_PerusahaanLaporanKeuangan.xml',
                    # 'view/view_ProjectProject.xml',
                    # 'view/view_ProductProduct.xml',
                    # 'view/view_OtherReceived.xml',
                    # 'view/view_OtherPayment.xml',
                    # 'view/view_PurchaseOrder.xml',
                    # 'view/view_PurchaseOrderLine.xml',
                    # 'view/view_PurchaseRequisition.xml',
                    # 'view/view_VoucherType.xml',
                    # 'view/view_invoice.xml',
                    # 'view/view_BankPayment.xml',
                    # 'view/view_CashPayment.xml',
                    # 'view/view_BankReceipt.xml',
                    # 'view/view_CashReceipt.xml',

                    # 'window_action/waction_ProjectProject.xml',
                    # 'window_action/waction_OtherReceived.xml',
                    # 'window_action/waction_OtherPayment.xml',
                    # 'window_action/waction_VoucherType.xml',
                    # 'window_action/waction_BankPayment.xml',
                    # 'window_action/waction_CashPayment.xml',
                    # 'window_action/waction_BankReceipt.xml',
                    # 'window_action/waction_CashReceipt.xml',


                    # 'board/purchase_board.xml',
                    # 'board/board_Voucher.xml',
                    # 'menu/menu_account.xml',
                    # 'menu/menu_stock.xml',
                    # 'menu/menu_sale.xml',
                    # 'menu/menu_purchase.xml',
                    # 'menu/menu_administration.xml',
                    # 'menu/menu_board.xml',
                    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
