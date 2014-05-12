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

class company_voucher_approval(osv.osv):
	_name = 'titis.company_voucher_approval'
	_description = 'Company Voucher Approval'
	
	def default_voucher_type_id(self, cr, uid, context=None):
		obj_account_voucher_type = self.pool.get('titis.voucher_type')
		voucher_type = []

		if context.get('voucher_type', False):
			kriteria = [('name', '=', context['voucher_type'])]

			voucher_type_ids = obj_account_voucher_type.search(cr, uid, kriteria)
			if voucher_type_ids : voucher_type = voucher_type_ids[0]

		return voucher_type
			
	_columns =	{
							'name' : fields.char(string='Approval', size=100, required=True),
							'company_id' : fields.many2one(string='Company', obj='res.company'),
							'sequence' : fields.integer(string='Sequence', required=True),
							'user_id' : fields.many2one(string='Approved By', obj='res.users', required=True),
							'voucher_type_id' : fields.many2one(string='Voucher Type', obj='titis.voucher_type', required=True),
							}						
							
	_defaults =	{
							'voucher_type_id' : default_voucher_type_id,
							}
				
company_voucher_approval()							
							






