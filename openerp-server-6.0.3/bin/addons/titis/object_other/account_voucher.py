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

class account_voucher(osv.osv):
	_name = 'account.voucher'
	_inherit = 'account.voucher'

	def default_voucher_type_id(self, cr, uid, context=None):
		obj_account_voucher_type = self.pool.get('titis.voucher_type')
		voucher_type = []

		if context.get('voucher_type', False):
			kriteria = [('name', '=', context['voucher_type'])]

			voucher_type_ids = obj_account_voucher_type.search(cr, uid, kriteria)
			if voucher_type_ids : voucher_type = voucher_type_ids[0]

		return voucher_type

	def default_type(self, cr, uid, context=None):
		obj_account_voucher_type = self.pool.get('titis.voucher_type')

		voucher_type_id = self.default_voucher_type_id(cr, uid, context)

		if not voucher_type_id : return False

		voucher_type = obj_account_voucher_type.browse(cr, uid, [voucher_type_id])[0]

		return voucher_type.default_header_type

	_columns =	{
			            'voucher_type_id' : fields.many2one(obj='titis.voucher_type', string='Voucher Type', readonly=True, states={'draft':[('readonly',False)]}),
			            'payment_method' : fields.selection(string='Payment Method', selection=[('bank_transfer','Bank Transfer'),('cheque','Cheque'),('giro','Giro')], readonly=True, states={'draft':[('readonly',False)]}),
			            'cheque_number' : fields.char(string='Cheque Number', size=50, readonly=True, states={'draft':[('readonly',False)]}),
			            'cheque_date' : fields.date(string='Cheque Date', readonly=True, states={'draft':[('readonly',False)]}),
			            'cheque_partner_bank_id' : fields.many2one(obj='res.partner.bank', string='Destination Bank Account', readonly=True, states={'draft':[('readonly',False)]}),
			            'cheque_bank_id' : fields.related('cheque_partner_bank_id', 'bank', type='many2one', relation='res.bank', string='Bank', store=True, readonly=True),
			            'cheque_recepient' : fields.char(string='Cheque Recepient', size=100, readonly=True, states={'draft':[('readonly',False)]}),
			            'cheque_is_giro' : fields.boolean('Is Giro?')
			            }

	_defaults =	{
			            'voucher_type_id' : default_voucher_type_id,
			            'type' : default_type,
			            }
			            
	def first_move_line_get(self, cr, uid, voucher_id, move_id, company_currency, current_currency, context=None):
		'''
		Override untuk menyesuaikan field yang berkaitan dengan cek/giro
		'''
		voucher = self.browse(cr, uid, [voucher_id])[0]

		res =	{
					'payment_method' : voucher.payment_method,
					'cheque_number' : voucher.cheque_number,
					'cheque_date' : voucher.cheque_date,
					'cheque_partner_bank_id' : voucher.cheque_partner_bank_id.id,
					'cheque_recepient' : voucher.cheque_recepient
					}

		move_line = super(account_voucher, self).first_move_line_get(cr, uid, voucher_id, move_id, company_currency, current_currency)

		move_line.update(res)

		return move_line
		
	def check_total_voucher(self, cr, uid, id):
		"""
		Method untuk melakukan pengecekan agar total voucher == sum amount semua voucher line
		"""
		
		voucher = self.browse(cr, uid, [id])[0]
		
		total = 0.0
		if voucher.line_ids:
			for line in voucher.line_ids:
				total += line.amount
				
		if voucher.amount == total:
			return True
		else:
			return False
			
	def proforma_voucher(self, cr, uid, ids, context=None):
		"""
		Override
		"""
		
		for id in ids:
			if not self.check_total_voucher(cr, uid, id):
				raise osv.except_osv('Warning!', 'Total voucher is not equal with line total')
				return False

		return super(account_voucher, self).proforma_voucher(cr, uid, ids, context)
		
	def onchange_journal_id(self, cr, uid, ids, journal_id):
		value = {}
		domain = {}
		warning = {}
		
		obj_journal = self.pool.get('account.journal')
				
		if journal_id:
			journal = obj_journal.browse(cr, uid, [journal_id])[0]
			value['account_id'] = journal.default_debit_account_id.id
		
		
		return {'value' : value, 'domain' : domain, 'warning' : warning}
        
        
							
account_voucher()							
	
