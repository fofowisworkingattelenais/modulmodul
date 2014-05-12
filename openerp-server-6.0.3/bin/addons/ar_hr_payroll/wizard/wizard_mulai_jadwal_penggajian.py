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


class mulai_jadwal_penggajian(osv.osv_memory):
	_name = 'hr.wizard_mulai_jadwal_penggajian'
	_description = 'Wizard Mulai Jadwal Penggajian'

		
	_columns = 	{
				'tanggal_penggajian' : fields.date(string='Tanggal Penggajian', required=True),
				}

	def jalankan(self, cr, uid, ids, context=None):
		obj_jadwal_penggajian = self.pool.get('hr.jadwal_penggajian')
		
		wizard_run = self.read(cr, uid, ids)[0] 
		tanggal_skr = wizard_run['tanggal_penggajian']
		
		
		kriteria = [('tanggal_penggajian','=',tanggal_skr)]
		
		jadwal_penggajian_ids = obj_jadwal_penggajian.search(cr, uid, kriteria)
			
		
		if not jadwal_penggajian_ids : return {'type': 'ir.actions.act_window_close'}
		
		for jadwal_penggajian_id in jadwal_penggajian_ids:
			obj_jadwal_penggajian.buat_eksekusi_penggajian(cr, uid, jadwal_penggajian_id)
			
			obj_jadwal_penggajian.buat_jadwal_penggajian(cr, uid, jadwal_penggajian_id)
			
		return {'type': 'ir.actions.act_window_close'}
				
mulai_jadwal_penggajian()


