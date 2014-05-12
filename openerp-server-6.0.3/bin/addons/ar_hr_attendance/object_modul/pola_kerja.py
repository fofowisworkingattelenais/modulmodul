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


class pola_kerja(osv.osv):
	_name = 'hr.pola_kerja'
	_description = 'Pola Kerja'

		
	def default_active(self, cr, uid, context={}):
		return 1
				
	_columns = 	{
				'name' : fields.char(string='Pola Kerja', size=100, required=True),
				'kode' : fields.char(string='Kode', size=30, required=True),
				'detail_pola_kerja_ids' : fields.one2many(obj='hr.detail_pola_kerja', fields_id='pola_kerja_id', string='Detail Pola Kerja'),				
				'active' : fields.boolean(string='Aktif'),
				'keterangan' : fields.text(string='Keterangan'),
				}
				
	_defaults =	{
				'active' : default_active,
				}
				
	def cek_pola_kerja(self, cr, uid, id):
		obj_pola_kerja = self.pool.get('hr.pola_kerja')
		
		pola_kerja = obj_pola_kerja.browse(cr, uid, [id])[0]
		
		# pastikan pola kerja memiliki detail
		if not pola_kerja.detail_pola_kerja_ids:
			raise osv.except_osv('Peringatan!', 'Pola kerja tidak memiliki detail pola kerja')
			return False
		
		urutan = []
		
		for detail in pola_kerja.detail_pola_kerja_ids:
			urutan.append(detail.name)
			
		# pastikan pola kerja memiliki urutan ke-1
		if 1 not in urutan:
			raise osv.except_osv('Peringatan!', 'Pola kerja tidak memiliki sequence mulai')
			return False
			
		# cek urutan detail pola kerja
		sequence_akhir = max(urutan)
		for sequence in range(sequence_akhir):
			if (sequence+1) not in urutan:
				raise osv.except_osv('Peringatan!', 'Sequence pola kerja tidak benar')
				return False
				
		return True
		
	def button_action_cek_pola_kerja(self, cr, uid, ids, context={}):
		"""
		Method untuk button cek pola kerja
		"""
		for id in ids:
			self.cek_pola_kerja(cr, uid, id)
			
		return True
		
	def buat_absensi(self, cr, uid, id, tanggal_mulai, tanggal_akhir):
		"""
		param :
		- tanggal_mulai : date
		- tanggal_akhir : date
		
		Method untuk membuat absensi
		"""
		hasil = []
		obj_pola_kerja = self.pool.get('hr.pola_kerja')
		obj_user = self.pool.get('res.users')
		obj_shift = self.pool.get('hr.shift_kerja')
		obj_detail_pola_kerja = self.pool.get('hr.detail_pola_kerja')
		
		pola_kerja = obj_pola_kerja.browse(cr, uid, [id])[0]
		user = obj_user.browse(cr, uid, [uid])[0]
		
		# cek default kode absensi
		if not user.company_id.default_kode_absen_id:
			raise osv.except_osv('Peringatan!', 'Kode absensi default belum diset')
			
		if not user.company_id.default_kode_absen_libur_id:
			raise osv.except_osv('Peringatan!', 'Kode absensi libur default belum diset')			
			
		urutan = []
		for detail in pola_kerja.detail_pola_kerja_ids:
			urutan.append(detail.name)
			
		max_urutan = max(urutan)
		
		jumlah_sequence = tanggal_akhir.toordinal() - tanggal_mulai.toordinal() + 1
		tanggal = tanggal_mulai
		
		
		for urutan in range(jumlah_sequence):
			if urutan == 0: 
				urutan_detail = tanggal_mulai.weekday() + 1
				if urutan_detail > max_urutan:
					urutan_detail = urutan_detail % max_urutan
				
				
			kriteria = [('name','=',urutan_detail),('pola_kerja_id','=',id)]
			detail_pola_kerja_ids = obj_detail_pola_kerja.search(cr, uid, kriteria)
			detail_pola_kerja = obj_detail_pola_kerja.browse(cr, uid, detail_pola_kerja_ids)[0]
			
			val =	{
					'tanggal' : tanggal.strftime('%Y-%m-%d'),
					'kode_absen_id' : detail_pola_kerja.kerja == 'masuk' and user.company_id.default_kode_absen_id.id or user.company_id.default_kode_absen_libur_id.id,
					'shift_kerja_id' : detail_pola_kerja.kerja == 'masuk' and detail_pola_kerja.shift_kerja_id.id or False,
					}
					
					
			tanggal = tanggal.toordinal() + 1
			tanggal = date.fromordinal(tanggal)
					
			hasil.append(val)
			
			if urutan_detail < max_urutan:
				urutan_detail += 1
			else:
				urutan_detail = 1
			
		return hasil
			
		
		
			
		
		
		
		

				
pola_kerja()


