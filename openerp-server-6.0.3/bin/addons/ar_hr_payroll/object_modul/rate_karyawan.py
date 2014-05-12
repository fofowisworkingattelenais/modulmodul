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
from datetime import date
import decimal_precision as dp


class rate_karyawan(osv.osv):
	_name = 'hr.rate_karyawan'
	_description = 'Rate Karyawan'
	

	def function_employee_id(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_rate_karyawan = self.pool.get('hr.rate_karyawan')
		
		for rate_karyawan in obj_rate_karyawan.browse(cr, uid, ids):
			res[rate_karyawan.id] = rate_karyawan.contract_id.employee_id.id
			
		return res
		
		
	_columns = 	{
				'employee_id' : fields.function(fnct=function_employee_id, type='many2one', relation='hr.employee', method=True, strore=False, string='Karyawan'), #TODO: Pertimbangkan untuk strore nilai function
				'contract_id' : fields.many2one(obj='hr.contract', string='History', required=True),
				'jenis_rate_id' : fields.many2one(obj='hr.jenis_rate', string='Jenis Rate', required=True),
				'jumlah' : fields.float(string='Jumlah',  digits=(16,2), required=True),
				}
				


				
		
		
				

				
rate_karyawan()


