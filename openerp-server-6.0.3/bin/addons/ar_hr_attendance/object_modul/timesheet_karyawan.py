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
from datetime import date, datetime, tzinfo
import decimal_precision as dp



class timesheet_karyawan(osv.osv):
	_name = 'hr.timesheet_karyawan'
	_description = 'Timesheet Karyawan'

	def default_name(self, cr, uid, context={}):
		return '/'
		
	def default_state(self, cr, uid, context={}):
		return 'draft'

	_columns = 	{
				'name' : fields.char(string='# Timesheet', size=30, required=True, readonly=True),
				'employee_id' : fields.many2one(string='Karyawan', obj='hr.employee', required=True, readonly=True, domain=['|','|',('status_karyawan','=','probation'),('status_karyawan','=','kontrak'),('status_karyawan','=','tetap')], states={'draft':[('readonly',False)]}),
				'pola_kerja_id' : fields.many2one(string='Pola Kerja', obj='hr.pola_kerja', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'detail_periode_kerja_id' : fields.many2one(string='Periode Kerja', obj='hr.detail_periode_gaji', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'absensi_ids' : fields.one2many(string='Absensi', obj='hr.absensi', fields_id='timesheet_id', readonly=True, states={'draft':[('readonly',False)],'confirm':[('readonly',False)]}),
				'perhitungan_timesheet_ids' : fields.one2many(string='Perhitungan Timesheet', obj='hr.perhitungan_timesheet', fields_id='timesheet_id', readonly=True, states={'draft':[('readonly',False)],'confirm':[('readonly',False)]}),
				'keterangan' : fields.text(string='Keterangan'),
				'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'),('selesai','Selesai'),('batal','Batal')], string='State', readonly=True, required=True),
				
				}
				
	_defaults =	{
				'name' : default_name,
				'state' : default_state,
				}
				
	def workflow_action_confirm(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.buat_sequence(cr, uid, id):
				return False
				
			self.write(cr, uid, [id], {'state' : 'confirm'})
			
		return True
		
	def workflow_action_selesai(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.cek_konfirmasi_absen(cr, uid, id):
				raise osv.except_osv('Peringatan!', 'Masih ada absensi yang belum dikonfirmasi')
				return False
				
			self.write(cr, uid, [id], {'state' : 'selesai'})
			
		return True	
		
	def workflow_action_batal(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'batal'})
			
		return True		
		
	def onchange_employee_id(self, cr, uid, ids, employee_id):
		#value = {'pola_kerja_id' : False, 'detail_periode_kerja_id' : False}
		#domain = {'pola_kerja_id' : [('id','in',[])], 'detail_periode_kerja_id' : [('id','in',[])]}
		
		value = {}
		domain = {}
		
		obj_karyawan = self.pool.get('hr.employee')
		
		#raise osv.except_osv('a',str(employee_id))
		
		value.update({'pola_kerja_id':False, 'detail_periode_kerja_id':False})
		domain.update({'pola_kerja_id' : [('id','in',[])], 'detail_periode_kerja_id' : [('id','in',[])]})
		
		if employee_id:
			karyawan = obj_karyawan.browse(cr, uid, [employee_id])[0]
			history = karyawan.contract_id
			value.update({'pola_kerja_id':history.pola_kerja_id.id})
			domain.update({'pola_kerja_id':[('id','=',history.pola_kerja_id.id)], 'detail_periode_kerja_id':[('periode_gaji_id','=',history.periode_gaji_id.id)]})
			

			
			
		return {'value' : value, 'domain' : domain}
			
		
	def buat_sequence(self, cr, uid, id):
		obj_sequence = self.pool.get('ir.sequence')
		obj_timesheet = self.pool.get('hr.timesheet_karyawan')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		if not user.company_id.sequence_timesheet_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk timesheet belum diset')
			return False

		sequence_id = user.company_id.sequence_timesheet_id.id		
		sequence = obj_sequence.next_by_id(cr, uid, sequence_id)
		
		obj_timesheet.write(cr, uid, [id], {'name' : sequence})
		
		return True			
				
	def jumlah_hari(self, cr, uid, id):
		obj_timesheet = self.pool.get('hr.timesheet_karyawan')
		
		timesheet = obj_timesheet.browse(cr, uid, [id])[0]
		
		tanggal_mulai = timesheet.detail_periode_kerja_id.tanggal_mulai
		tanggal_akhir = timesheet.detail_periode_kerja_id.tanggal_akhir
		
		dt_tanggal_mulai = date(int(tanggal_mulai[0:4]), int(tanggal_mulai[5:7]), int(tanggal_mulai[8:10]))
		dt_tanggal_akhir = date(int(tanggal_akhir[0:4]), int(tanggal_akhir[5:7]), int(tanggal_akhir[8:10]))
		
		ord_tanggal_mulai = dt_tanggal_mulai.toordinal()
		ord_tanggal_akhir = dt_tanggal_akhir.toordinal()
		
		return ord_tanggal_akhir - ord_tanggal_mulai + 1
		
		
	def cari_hari_pertama(self, cr, uid, id):
		obj_timesheet = self.pool.get('hr.timesheet_karyawan')
		
		timesheet = obj_timesheet.browse(cr, uid, [id])[0]
		
		tanggal_mulai = '2012-11-01' #TODO
		
		dt_tanggal_mulai = date(int(tanggal_mulai[0:4]), int(tanggal_mulai[5:7]), int(tanggal_mulai[8:10]))
		
		return dt_tanggal_mulai.weekday() + 1
		
		
		
				
	def buat_absensi(self, cr, uid, ids, context={}):
		obj_absensi = self.pool.get('hr.absensi')
		obj_pola_kerja = self.pool.get('hr.pola_kerja')
		obj_timesheet = self.pool.get('hr.timesheet_karyawan')
		
		for id in ids:
			timesheet = obj_timesheet.browse(cr, uid, [id])[0]
			
			# cek pola kerja. jika pola kerja salah jangan buat absensi
			if not obj_pola_kerja.cek_pola_kerja(cr, uid, timesheet.pola_kerja_id.id):
				return False
				
			tanggal_mulai = timesheet.detail_periode_kerja_id.tanggal_mulai
			tanggal_akhir = timesheet.detail_periode_kerja_id.tanggal_akhir
		
			dt_tanggal_mulai = date(int(tanggal_mulai[0:4]), int(tanggal_mulai[5:7]), int(tanggal_mulai[8:10]))
			dt_tanggal_akhir = date(int(tanggal_akhir[0:4]), int(tanggal_akhir[5:7]), int(tanggal_akhir[8:10]))			

			for dict_absensi in obj_pola_kerja.buat_absensi(cr, uid, timesheet.pola_kerja_id.id, dt_tanggal_mulai, dt_tanggal_akhir):
				dict_absensi.update({'timesheet_id' : timesheet.id})
				
				absensi_id = obj_absensi.create(cr, uid, dict_absensi)
				
		return True

				
	def hitung_timesheet(self, cr, uid, id, context={}):
		obj_timesheet = self.pool.get('hr.timesheet_karyawan')
		obj_ketentuan_absensi = self.pool.get('hr.ketentuan_absensi')
		obj_perhitungan_timesheet = self.pool.get('hr.perhitungan_timesheet')
		
		timesheet = obj_timesheet.browse(cr, uid, [id])[0]
		
		localdict =	{
					'self' : self,
					'cr' : cr,
					'uid' : uid,
					'timesheet' : timesheet,
					'hasil' : 0.0
					}
		
		if timesheet.detail_periode_kerja_id.periode_gaji_id.ketentuan_absensi_ids:
			for ketentuan in timesheet.detail_periode_kerja_id.periode_gaji_id.ketentuan_absensi_ids:
				localdict['hasil'] = 0.0
				dict_hasil = obj_ketentuan_absensi.hitung_ketentuan(cr, uid, ketentuan.id, localdict)
				dict_hasil.update({'timesheet_id' : id})
				perhitungan_timesheet_id = obj_perhitungan_timesheet.create(cr, uid, dict_hasil)
			
		return True
		
	def hapus_perhitungan_absensi(self, cr, uid, id):
		obj_perhitungan = self.pool.get('hr.perhitungan_timesheet')
		
		kriteria = [('timesheet_id','=',id)]
		perhitungan_ids = obj_perhitungan.search(cr, uid, kriteria)
		
		if perhitungan_ids:
			obj_perhitungan.unlink(cr, uid, perhitungan_ids)
			
		return True 
		
	def button_action_hitung_timesheet(self, cr, uid, ids, context={}):
		obj_timesheet = self.pool.get('hr.timesheet_karyawan')
		for id in ids:
			# hapus perhitungan yang lama
			obj_timesheet.hapus_perhitungan_absensi(cr, uid, id)
		
			# buat perhitungan
			obj_timesheet.hitung_timesheet(cr, uid, id)
			
		return True		
		
	def validasi_absensi(self, cr, uid, id):
		obj_timesheet = self.pool.get('hr.timesheet_karyawan')
		obj_absensi = self.pool.get('hr.absensi')
		
		timesheet = obj_timesheet.browse(cr, uid, [id])[0]
		
		if timesheet.absensi_ids:
			for absensi in timesheet.absensi_ids:
				obj_absensi.workflow_action_confirm(cr, uid, [absensi.id])
				
		return True
		
	def button_action_validasi_absensi(self, cr, uid, ids, context={}):
		obj_timesheet = self.pool.get('hr.timesheet_karyawan')
		for id in ids:
			obj_timesheet.validasi_absensi(cr, uid, id)
			
		return True
		
	def cek_konfirmasi_absen(self, cr, uid, id):
		
		timesheet = self.browse(cr, uid, [id])[0]
		
		if timesheet.absensi_ids:
			for absen in timesheet.absensi_ids:
				if absen.state == 'draft':
					return False
					
		return True
			
					
				
timesheet_karyawan()


