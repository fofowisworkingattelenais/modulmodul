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

import wizard
from osv import fields, osv
from datetime import date
import netsvc
from tools.translate import _
import csv
import tools
import base64
from tempfile import TemporaryFile


class wizard_import_absensi(osv.osv_memory):
	_name = 'titis.wizard_import_absensi'
	_description = 'Wizard Import Absensi'

	_columns = 	{
								'import_file' : fields.binary(string='File', required='True'),
								'detail_ids' : fields.one2many(string='Detail', obj='titis.detail_wizard_import_absensi', fields_id='wizard_id'),
								}
				

	def create_import_line(self, cr, uid, id, nip, tanggal, clock_in, clock_out):
		obj_detail = self.pool.get('titis.detail_wizard_import_absensi')
		obj_absensi = self.pool.get('hr.absensi')
		
		kriteria = [('wizard_id','=',id),('absensi_id.karyawan_id.nip_lama','=',nip),('absensi_id.tanggal','=',tanggal)]
		
		detail_ids = obj_detail.search(cr, uid, kriteria)
		
		if not detail_ids:
			kriteria1 = [('tanggal','=',tanggal),('karyawan_id.nip_lama','=',nip)]
			absensi_ids = obj_absensi.search(cr, uid, kriteria1)
			if absensi_ids:
				val =	{
							'wizard_id' : id,
							'absensi_id' : absensi_ids[0],
							'jam_masuk' : '%s %s:00' % (tanggal, clock_in),
							'jam_keluar' : '%s %s:00' % (tanggal, clock_out),
							}
				detail_id = obj_detail.create(cr, uid, val)
				
		return True
							
				
		

	def import_csv(self, cr, uid, ids, data, context=None):
		obj_wizard = self.pool.get('titis.wizard_import_absensi')
		
		import_data = obj_wizard.browse(cr, uid, ids)[0]
		
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(import_data.import_file))
		fileobj.seek(0)
		reader = csv.DictReader(fileobj, delimiter=',')

		for baris in reader:
			if not self.create_import_line(cr, uid, import_data.id, baris['nip'], baris['tanggal'], baris['clock_in'], baris['clock_out']):
				raise osv.except_osv('Warning!', 'Error on create detail')
				return False
				
		return	{
					    'name': 'Import Absensi',
					    'view_type': 'form',
					    'view_mode': 'form',
					    'res_model': 'titis.wizard_import_absensi',
					    'type': 'ir.actions.act_window',
					    'res_id' : import_data.id,
					    'target' : 'new',
					    }
					    
	def simpan_absensi(self, cr, uid, ids, data, context=None):
		obj_absensi = self.pool.get('hr.absensi')
		obj_user = self.pool.get('res.users')
		obj_kode = self.pool.get('hr.kode_absen')
		
		kode_ids = obj_kode.search(cr, uid, [('name','=','Hadir')])
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		wizard = self.browse(cr,uid, ids)[0]
		if wizard.detail_ids:
			for detail in wizard.detail_ids:
				val	=	{
							'realisasi_jam_masuk' : detail.jam_masuk,
							'realisasi_jam_keluar' : detail.jam_keluar,
							'kode_absen_id' : kode_ids[0],
							}
				obj_absensi.write(cr, uid, [detail.absensi_id.id], val)
				
		return {'type': 'ir.actions.act_window_close'}
	
wizard_import_absensi()

class detail_wizard_import_absensi(osv.osv_memory):
	_name = 'titis.detail_wizard_import_absensi'
	_description = 'Detail Wizard Import Absensi'
	
	_columns =	{
							'wizard_id' : fields.many2one(string='# Wizard', obj='titis.wizard_import_absensi'),
							'absensi_id' : fields.many2one(string='Absensi', obj='hr.absensi', required=True),
							'employee_id' : fields.related('absensi_id','timesheet_id','employee_id','name', related='hr.employee', type='char', readonly=True, string='Karyawan'),
							'jam_masuk' : fields.datetime(string='Jam Masuk'),
							'jam_keluar' : fields.datetime(string='Jam Keluar'),
							}
	
detail_wizard_import_absensi()
