# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from osv import fields, osv
from datetime import datetime

class project_project(osv.osv):
    _name = 'project.project'
    _inherit = 'project.project'
    _columns = {
        'reg_date' : fields.date(string='Reg. Date'),
        'or_num' : fields.char(string='O.R No.', size=100),
        'or_date' : fields.date(string='O.R Date'),
        'contract_num' : fields.char(string='SP/PO/Contract No.', size=100),
        'contract_date' : fields.date(string='SP/PO/Contract Date'),
        'ipc_num' : fields.char(string='IPC No.', size=100),
        'ipc_date' : fields.date(string='IPC Date'),
        'purchase_sequence_id' : fields.many2one(string='PO Sequence', obj='ir.sequence', required=True),
        'requisition_sequence_id' : fields.many2one(string='Requisition Sequence', obj='ir.sequence', required=True),
        'purchase_approval_ids' : fields.one2many(stirng='Purchase Order Approval', obj='titis.project_purchase_approval', fields_id='project_id'),
        'requisition_approval_ids' : fields.one2many(stirng='Requisition Order Approval', obj='titis.project_requisition_approval', fields_id='project_id'),
        'bank_payment_approval_ids' : fields.one2many(string='Bank Payment Approval', obj='titis.project_voucher_approval', fields_id='project_id', domain=[('voucher_type_id.name','=','Bank Payment')]),
        'bank_receipt_approval_ids' : fields.one2many(string='Bank Receipt Approval', obj='titis.project_voucher_approval', fields_id='project_id', domain=[('voucher_type_id.name','=','Bank Receipt')]),
        'cash_payment_approval_ids' : fields.one2many(string='Cash Payment Approval', obj='titis.project_voucher_approval', fields_id='project_id', domain=[('voucher_type_id.name','=','Cash Payment')]),
        'cash_receipt_approval_ids' : fields.one2many(string='Cash Receipt Approval', obj='titis.project_voucher_approval', fields_id='project_id', domain=[('voucher_type_id.name','=','Cash Receipt')]),
        'invoice_approval_ids' : fields.one2many(string='Invoice Approval', obj='titis.company_invoice_approval', fields_id='company_id'),
        'customer_invoice_approval_ids' : fields.one2many(string='Customer Invoice Approval', obj='titis.company_invoice_approval', fields_id='company_id', domain=[('type','=','out_invoive')]),
        'supplier_invoice_approval_ids' : fields.one2many(string='Supplier Invoice Approval', obj='titis.company_invoice_approval', fields_id='company_id', domain=[('type','=','in_invoive')]),
        'customer_refund_approval_ids' : fields.one2many(string='Customer Refund Approval', obj='titis.company_invoice_approval', fields_id='company_id', domain=[('type','=','out_refund')]),
        'supplier_refund_approval_ids' : fields.one2many(string='Supplier Refund Approval', obj='titis.company_invoice_approval', fields_id='company_id', domain=[('type','=','in_refund')]),
    }
project_project()






