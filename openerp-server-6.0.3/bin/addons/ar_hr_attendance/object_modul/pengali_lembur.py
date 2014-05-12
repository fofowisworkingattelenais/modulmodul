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


class pengali_lembur(osv.osv):
	_name = 'hr.pengali_lembur'
	_description = 'Pengali Lembur'

		
	def default_active(self, cr, uid, context={}):
		return 1
				
	_columns = 	{
				'salary_structure_id' : fields.many2one(obj='hr.payroll.structure', string='Struktur Gaji'),
				'status_hari' : fields.selection(selection=[('kerja','Hari Kerja'),('libur','Hari Libur')], string='Status Hari', required=True),
				'jam_min' : fields.integer(string='Jam Minimal',required=True),
				'jam_maks' : fields.integer(string='Jam Maksimal',required=True),
				'pengali' : fields.float(string='Pengali', required=True, digits=(5,2)),
				'active' : fields.boolean(string='Aktif'),
				'keterangan' : fields.text(string='Keterangan'),
				}
				
	_defaults =	{
				'active' : default_active,
				}
pengali_lembur()


