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
from ar_base_waktu import date_tools as dt
from datetime import date


class eksekusi_penggajian(osv.osv):
	_name = 'hr.eksekusi_penggajian'
	_description = 'Eksekusi Penggajian'

	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def function_name(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_eksekusi_penggajian = self.pool.get('hr.eksekusi_penggajian')
		for eksekusi_penggajian in obj_eksekusi_penggajian.browse(cr, uid, ids):
			res[eksekusi_penggajian.id] = '%s %s' % (eksekusi_penggajian.jadwal_penggajian_id.name, eksekusi_penggajian.employee_id.name)
			
		return res
		
	_columns = 	{
				'name' : fields.function(fnct=function_name, type='char', method=True, store=False, string='Name', size=25),
				'employee_id' : fields.many2one(obj='hr.employee', string='Karyawan', required=True),
				'jadwal_penggajian_id' : fields.many2one(obj='hr.jadwal_penggajian', string='Jadwal Penggajian', required=True),
				'payslip_line_id' : fields.many2one(obj='hr.payslip.line', string='Detail Slip Gaji'),
				'state' : fields.selection([('draft','Draft'),('active', 'Active'),('missed', 'Missed'),('run','Run')], 'Status', required=True, readonly=True),
				}
				
	_defaults =	{
				'state' : default_state,
				}
				
eksekusi_penggajian()


