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

class hr_payslip(osv.osv):
	_name = 'hr.payslip'
	_inherit = 'hr.payslip'

	def buat_sequence(self, cr, uid, id):
		obj_sequence = self.pool.get('ir.sequence')
		obj_payslip = self.pool.get('hr.payslip')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		if not user.company_id.sequence_gaji_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk slip gaji belum diset')
			return False

		sequence_id = user.company_id.sequence_gaji_id.id		
		sequence = obj_sequence.get_id(cr, uid, sequence_id)
		
		obj_payslip.write(cr, uid, [id], {'name' : sequence})
		
		return True										

hr_payslip()							
							






