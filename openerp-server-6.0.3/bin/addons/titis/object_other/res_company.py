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

class res_company(osv.osv):
	_name = 'res.company'
	_inherit = 'res.company'
	
	_columns = 	{
				# LAPORAN KEUANGAN
				'account_neraca_id' : fields.many2one('account.account', 'Akun Neraca'),
				'account_laba_rugi_id' : fields.many2one('account.account', 'Akun Laba Rugi'),
				'account_aktiva_id' : fields.many2one('account.account', 'Akun Aktiva'),
				'account_kewajiban_id' : fields.many2one('account.account', 'Akun Kewajiban'),
				'account_ekuitas_id' : fields.many2one('account.account', 'Akun Ekuitas'),
				'account_pendapatan_id' : fields.many2one('account.account', 'Akun Pendapatan'),
				'account_hpp_id' : fields.many2one('account.account', 'Akun HPP'),
				'account_beban_id' : fields.many2one('account.account', 'Akun Beban'),
				'account_pendapatan_dll_id' : fields.many2one('account.account', 'Akun Pendapatan Lain'),
				'account_beban_dll_id' : fields.many2one('account.account', 'Akun Beban Lain'),
				
				# APPROVAL
				'purchase_approval_ids' : fields.one2many(string='Purchase Approval', obj='titis.company_purchase_approval', fields_id='company_id'),
				'requisition_approval_ids' : fields.one2many(string='Purchase Requisition Approval', obj='titis.company_requisition_approval', fields_id='company_id'),
				'voucher_approval_ids' : fields.one2many(string='Voucher Approval', obj='titis.company_voucher_approval', fields_id='company_id'),
				'bank_payment_approval_ids' : fields.one2many(string='Bank Payment Approval', obj='titis.company_voucher_approval', fields_id='company_id', domain=[('voucher_type_id.name','=','Bank Payment')]),
				'bank_receipt_approval_ids' : fields.one2many(string='Bank Receipt Approval', obj='titis.company_voucher_approval', fields_id='company_id', domain=[('voucher_type_id.name','=','Bank Receipt')]),
				'cash_payment_approval_ids' : fields.one2many(string='Cash Payment Approval', obj='titis.company_voucher_approval', fields_id='company_id', domain=[('voucher_type_id.name','=','Cash Payment')]),
				'cash_receipt_approval_ids' : fields.one2many(string='Cash Receipt Approval', obj='titis.company_voucher_approval', fields_id='company_id', domain=[('voucher_type_id.name','=','Cash Receipt')]),
				'invoice_approval_ids' : fields.one2many(string='Invoice Approval', obj='titis.company_invoice_approval', fields_id='company_id'),
				'customer_invoice_approval_ids' : fields.one2many(string='Customer Invoice Approval', obj='titis.company_invoice_approval', fields_id='company_id', domain=[('type','=','out_invoive')]),
				'supplier_invoice_approval_ids' : fields.one2many(string='Supplier Invoice Approval', obj='titis.company_invoice_approval', fields_id='company_id', domain=[('type','=','in_invoive')]),
				'customer_refund_approval_ids' : fields.one2many(string='Customer Refund Approval', obj='titis.company_invoice_approval', fields_id='company_id', domain=[('type','=','out_refund')]),
				'supplier_refund_approval_ids' : fields.one2many(string='Supplier Refund Approval', obj='titis.company_invoice_approval', fields_id='company_id', domain=[('type','=','in_refund')]),
				
				'sequence_penghargaan_karyawan_id' : fields.many2one(obj='ir.sequence', string='Sequence Penghargaan Karyawan'),
				'sequence_peringatan_karyawan_id' : fields.many2one(obj='ir.sequence', string='Sequence Peringatan Karyawan'),				
				}

	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(res_company, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(res_company, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(res_company, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			

res_company()




