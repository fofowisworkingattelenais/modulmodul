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


class import_detail_payslip_input(osv.osv):
	_name = 'hr.import_detail_payslip_input'
	_description = 'Import Detail Payslip Input'


		
	_columns = 	{
				'import_payslip_input_id' : fields.many2one(obj='hr.import_payslip_input', string='# Import'),
				'employee_id' : fields.many2one(obj='hr.employee', string='Karyawan', required=True),
				'kode' : fields.char(string='Kode', size=30, reaquired=True),
				'jumlah' : fields.float(string='Jumlah', digits=(16,2)),
				}


import_detail_payslip_input()
