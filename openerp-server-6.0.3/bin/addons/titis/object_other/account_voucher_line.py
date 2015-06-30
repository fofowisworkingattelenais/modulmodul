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
from tools.translate import _

class account_voucher_line(osv.osv):
	_name = 'account.voucher.line'
	_inherit = 'account.voucher.line'

	def default_get(self, cr, uid, fields_list, context=None):
		res = super(account_voucher_line, self).default_get(cr, uid, fields_list, context)

		if context.get('default_detail_type_selection', False):
			res.update({'type' : context.get('default_detail_type_selection', False)})

		return res

	_columns =	{
							'analytics_id' : fields.many2one(obj='account.analytic.plan.instance', string='Analytic Distribution'),
                            'partner_id': fields.many2one(obj='res.partner', string='Partner'),
							}

	def compute_amount(self, cr, uid, move_id, journal_id, currency_id):
		currency_pool = self.pool.get('res.currency')
		obj_move = self.pool.get('account.move.line')
		obj_journal = self.pool.get('account.journal')

		rs = {}

		line = obj_move.browse(cr, uid, [move_id])[0]
		journal = obj_journal.browse(cr, uid, [journal_id])[0]

		currency_id = currency_id or journal.company_id.currency_id.id
		company_currency = journal.company_id.currency_id.id

		#ine.reconcile_partial_id and line.amount_residual_currency < 0:
		    # skip line that are totally used within partial reconcile
		    #pass
		if line.currency_id and currency_id==line.currency_id.id:
		    amount_original = abs(line.amount_currency)
		    amount_unreconciled = abs(line.amount_residual_currency)
		else:
		    amount_original = currency_pool.compute(cr, uid, company_currency, currency_id, line.credit or line.debit or 0.0)
		    amount_unreconciled = currency_pool.compute(cr, uid, company_currency, currency_id, abs(line.amount_residual))
		line_currency_id = line.currency_id and line.currency_id.id or company_currency
		rs = {
			    'amount_original': amount_original,
			    'amount': amount_unreconciled,
			    'amount_unreconciled': amount_unreconciled,
				}
		return rs

	def onchange_move_id(self, cr, uid, ids, move_id, journal_id, currency_id):
		value = {}
		domain = {}
		warning = {}

		obj_move = self.pool.get('account.move.line')

		if move_id:
			move = obj_move.browse(cr, uid, [move_id])[0]
			value['account_id'] = move.account_id.id
			value['name'] = move.name
			value['date_original'] = move.date
			value['date_due'] = move.date_maturity
			res = self.compute_amount(cr, uid, move_id, journal_id, currency_id)
			value['amount'] = res['amount']
			value['amount_original'] = res['amount_original']
			value['amount_unreconciled'] = res['amount_unreconciled']

		return {'value' : value, 'domain' : domain, 'warning' : warning}

	def create_account_move_line(self, cr, uid, id):
		obj_currency = self.pool.get('res.currency')
		obj_tax = self.pool.get('account.tax')
		obj_move_line = self.pool.get('account.move.line')
		obj_move = self.pool.get('account.move')

		line = self.browse(cr, uid, [id])[0]
		total = 0.0
		move_pair = []

		context = {}

		# create one move line per voucher line where amount is not 0.0
		if not line.amount:
			return True, total, move_pair

		context_multi_currency = context.copy()
		context_multi_currency.update({'date': line.voucher_id.date})
		company_currency = line.voucher_id.journal_id.company_id.currency_id.id
		current_currency = line.voucher_id.currency_id.id

		if line.amount == line.amount_unreconciled:
			amount = line.move_line_id.amount_residual #residual amount in company currency
		else:
			amount = obj_currency.compute(cr, uid, current_currency, company_currency, line.untax_amount or line.amount, context=context_multi_currency)

		move_line = 	{
									'journal_id' : line.voucher_id.journal_id.id,
									'period_id' : line.voucher_id.period_id.id,
									'name' : line.name and line.name or '/',
									'account_id' : line.account_id.id,
									'move_id' : line.voucher_id.move_id.id, #TODO
									'partner_id' : line.partner_id.id, #TODO
									'currency_id' : company_currency <> current_currency and current_currency or False,
									'analytic_account_id' : line.account_analytic_id and line.account_analytic_id.id or False,
									'analytics_id' : line.analytics_id and line.analytics_id.id or False,
									'quantity' : 1,
									'credit' : 0.0,
									'debit' : 0.0,
									'date' : line.voucher_id.date
									}
		if not amount:
			raise osv.except_osv(_('Warning'),
				_("Error while processing 'account.voucher %s' (id:%s), amount: %s !") % (line.voucher_id.name, line.voucher_id.id, line.voucher_id.amount))

		if amount < 0:
			amount = -amount
			if line.type == 'dr':
				line.type = 'cr'
			else:
				line.type = 'dr'

		if (line.type=='dr'):
			total += amount
			move_line['debit'] = amount
		else:
			total -= amount
			move_line['credit'] = amount

		# Pajak
		if line.voucher_id.tax_id and line.voucher_id.type in ('sale', 'purchase'):
			move_line.update({
				'account_tax_id': line.voucher_id.tax_id.id,
			})
		if move_line.get('account_tax_id', False):
			tax_data = obj_tax.browse(cr, uid, [move_line['account_tax_id']], context=context)[0]
			if not (tax_data.base_code_id and tax_data.tax_code_id):
				raise osv.except_osv(_('No Account Base Code and Account Tax Code!'),_("You have to configure account base code and account tax code on the '%s' tax!") % (tax_data.name))

		sign = (move_line['debit'] - move_line['credit']) < 0 and -1 or 1
		move_line['amount_currency'] = company_currency <> current_currency and sign * line.amount or 0.0


		line_id = obj_move_line.create(cr, uid, move_line)

		obj_move.write(cr, uid, [line.voucher_id.move_id.id], {})

		# Kembalikan pasangan account.move.line
		if line.move_line_id.id:
			#TODO: Dua baris di bawah harusnya bisa jadi satu
			move_pair.append(line_id)
			move_pair.append(line.move_line_id.id)

		return True, total, move_pair




account_voucher_line()
