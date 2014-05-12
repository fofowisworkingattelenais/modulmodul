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

class account_bank_statement_line(osv.osv):

	def default_account_id(self, cr, uid, context={}):
		obj_user = self.pool.get('res.users')

		user = obj_user.browse(cr, uid, [uid])[0]

		jenis = context.get('jenis', False)

		if not jenis :
			return False

		if jenis == 'cash_register' :
			account_id = user.company_id.default_account_cash_register_id.id
			
			if not account_id :
				return False
			return account_id
		
		elif jenis == 'bank_statement' :
			return False

	_name = 'account.bank.statement.line'
	_inherit = 'account.bank.statement.line'

	_defaults = {
					'account_id' : default_account_id,
				}
			

account_bank_statement_line()




