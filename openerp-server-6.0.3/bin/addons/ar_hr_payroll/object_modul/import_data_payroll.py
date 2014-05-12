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


class import_data_payroll(osv.osv):
	_name = 'hr.import_data_payroll'
	_description = 'Import Data Payroll'

		
	_columns = 	{
				'detail_periode_gaji_id' : fields.many2one('hr.detail_periode_gaji', 'Periode Gaji', required=True),
				'employee_id' : fields.many2one('hr.employee', 'Karyawan', required=True),
				'var1' : fields.float('VAR1', Digits=(10,2)),
				'var2' : fields.float('VAR2', Digits=(10,2)),
				'var3' : fields.float('VAR3', Digits=(10,2)),
				'var4' : fields.float('VAR4', Digits=(10,2)),
				'var5' : fields.float('VAR5', Digits=(10,2)),
				'proses' : fields.boolean('Proses'),
				}

import_data_payroll()
