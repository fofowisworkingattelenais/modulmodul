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

class hr_contract(osv.osv):
	_name = 'hr.contract'
	_inherit = 'hr.contract'

	
	_columns =	{
							'wage_type_id': fields.many2one('hr.contract.wage.type', 'Wage Type', required=False),
							}
							
	def buat_sequence(self, cr, uid, contract_id, context=None):
		"""
		Buat sequence
		"""
		
		obj_user = self.pool.get('res.users')
		obj_sequence = self.pool.get('ir.sequence')
		obj_contract = self.pool.get('hr.contract')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		kontrak = obj_contract.browse(cr, uid, [contract_id])[0]
		
		# jika kontrak sudah mendapatkan name, maka tidak perlu buat sequence
		if kontrak.name != '/':
			return True		
		
		# buat sequence
		if not user.company_id.sequence_kontrak_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk history karyawan belum diset')
			return False
		elif user.company_id.sequence_kontrak_id:
			sequence_id = user.company_id.sequence_kontrak_id.id
			sequence = obj_sequence.get_id(cr, uid, sequence_id)
			obj_contract.write(cr, uid, [contract_id], {'name' : sequence})
			return True								

hr_contract()							
							






