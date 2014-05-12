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
from datetime import date, datetime
import decimal_precision as dp


class absensi(osv.osv):
	_name = 'hr.absensi'
	_description = 'Absensi'

	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def function_waktu_shift(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_absensi = self.pool.get('hr.absensi')
		for absensi in obj_absensi.browse(cr, uid, ids):
			res[absensi.id] =	{
								'jam_masuk' : False,
								'jam_keluar' : False,
								'mulai_istirahat' : False,
								'selesai_istirahat' : False,
								}
			if absensi.shift_kerja_id and absensi.tanggal:
				tanggal = absensi.tanggal
				
				# jam masuk
				jam_jam_masuk = str(int(absensi.shift_kerja_id.jam_masuk)).rjust(2, '0')
				menit_jam_masuk = str(int(absensi.shift_kerja_id.jam_masuk % int(absensi.shift_kerja_id.jam_masuk) * 60.0)).rjust(2, '0')
				
				# jam keluar
				jam_jam_keluar = str(int(absensi.shift_kerja_id.jam_keluar)).rjust(2, '0')
				menit_jam_keluar = str(int(absensi.shift_kerja_id.jam_keluar % int(absensi.shift_kerja_id.jam_keluar) * 60.0)).rjust(2, '0')
				
				# mulai istirahat
				jam_mulai_istirahat = str(int(absensi.shift_kerja_id.mulai_istirahat)).rjust(2, '0')
				menit_mulai_istirahat = str(int(absensi.shift_kerja_id.mulai_istirahat % int(absensi.shift_kerja_id.mulai_istirahat) * 60.0)).rjust(2, '0')
				
				# selesai istirahat
				jam_selesai_istirahat = str(int(absensi.shift_kerja_id.selesai_istirahat)).rjust(2, '0')
				menit_selesai_istirahat = str(int(absensi.shift_kerja_id.selesai_istirahat % int(absensi.shift_kerja_id.selesai_istirahat) * 60.0)).rjust(2, '0')
																
				res[absensi.id]['jam_masuk'] = '%s %s:%s:00' % (tanggal, jam_jam_masuk, menit_jam_masuk)
				res[absensi.id]['jam_keluar'] = '%s %s:%s:00' % (tanggal, jam_jam_keluar, menit_jam_keluar)
				res[absensi.id]['mulai_istirahat'] = '%s %s:%s:00' % (tanggal, jam_mulai_istirahat, menit_mulai_istirahat)
				res[absensi.id]['selesai_istirahat'] = '%s %s:%s:00' % (tanggal, jam_selesai_istirahat, menit_selesai_istirahat)
		return res
		
	def function_perhitungan_absen(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_absensi = self.pool.get('hr.absensi')
		for absensi in obj_absensi.browse(cr, uid, ids):
			res[absensi.id] =	{
								'overtime_datang' : 0.0,
								'terlambat_datang' : 0.0,
								'overtime_pulang' : 0.0,
								'cepat_pulang' : 0.0,
								'waktu_kerja' : 0.0,
								'overtime_datang_diakui' : 0.0,
								'overtime_pulang_diakui' : 0.0,
								}
								
			if absensi.jam_masuk and absensi.realisasi_jam_masuk:
				dt_jam_masuk = datetime(int(absensi.jam_masuk[0:4]), int(absensi.jam_masuk[5:7]), int(absensi.jam_masuk[8:10]), int(absensi.jam_masuk[11:13]), int(absensi.jam_masuk[14:16]))
				dt_realisasi_jam_masuk = datetime(int(absensi.realisasi_jam_masuk[0:4]), int(absensi.realisasi_jam_masuk[5:7]), int(absensi.realisasi_jam_masuk[8:10]), int(absensi.realisasi_jam_masuk[11:13]), int(absensi.realisasi_jam_masuk[14:16]))
				if dt_realisasi_jam_masuk < dt_jam_masuk:
					res[absensi.id]['overtime_datang'] = (dt_jam_masuk - dt_realisasi_jam_masuk).seconds / 60.0
				elif dt_realisasi_jam_masuk > dt_jam_masuk:
					res[absensi.id]['terlambat_datang'] = (dt_realisasi_jam_masuk - dt_jam_masuk).seconds / 60.0
					
			if absensi.jam_keluar and absensi.realisasi_jam_keluar:
				dt_jam_keluar = datetime(int(absensi.jam_keluar[0:4]), int(absensi.jam_keluar[5:7]), int(absensi.jam_keluar[8:10]), int(absensi.jam_keluar[11:13]), int(absensi.jam_keluar[14:16]))
				dt_realisasi_jam_keluar = datetime(int(absensi.realisasi_jam_keluar[0:4]), int(absensi.realisasi_jam_keluar[5:7]), int(absensi.realisasi_jam_keluar[8:10]), int(absensi.realisasi_jam_keluar[11:13]), int(absensi.realisasi_jam_keluar[14:16]))
				if dt_realisasi_jam_keluar > dt_jam_keluar:
					res[absensi.id]['overtime_pulang'] = (dt_realisasi_jam_keluar - dt_jam_keluar).seconds / 60.0
				elif dt_realisasi_jam_keluar < dt_jam_keluar:
					res[absensi.id]['cepat_pulang'] = (dt_jam_keluar - dt_realisasi_jam_keluar).seconds / 60.0			
					
			if absensi.lembur_id:
				if absensi.lembur_id.state == 'disetujui':
					if absensi.lembur_id.flag_sebelum:
						res[absensi.id]['overtime_datang_diakui'] = (absensi.lembur_id.jumlah_menit_sebelum > res[absensi.id]['overtime_datang'] and  res[absensi.id]['overtime_datang'] > 0) and res[absensi.id]['overtime_datang'] or absensi.lembur_id.jumlah_menit_sebelum
					if absensi.lembur_id.flag_setelah:
						res[absensi.id]['overtime_pulang_diakui'] = absensi.lembur_id.jumlah_menit_setelah > res[absensi.id]['overtime_pulang'] and res[absensi.id]['overtime_pulang'] or absensi.lembur_id.jumlah_menit_setelah					
						
		return res
				
		
	_columns = 	{
				'tanggal' : fields.date(string='Tanggal', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'jam_masuk' : fields.function(fnct=function_waktu_shift, string='Jam Masuk', type='datetime', method=True, store=False, multi='all'),
				'jam_keluar' : fields.function(fnct=function_waktu_shift, string='Jam Keluar', type='datetime', method=True, store=False, multi='all'),
				'mulai_istirahat' : fields.function(fnct=function_waktu_shift, string='Mulai Istirahat', type='datetime', method=True, store=False, multi='all'),
				'selesai_istirahat' : fields.function(fnct=function_waktu_shift, string='Selesai Istirahat', type='datetime', method=True, store=False, multi='all'),
				'overtime_datang' : fields.function(fnct=function_perhitungan_absen, string='Overtime Datang', type='float', digits=(16,2), method=True, store=False, multi='perhitungan'),
				'terlambat_datang' : fields.function(fnct=function_perhitungan_absen, string='Terlambat Datang', type='float', digits=(16,2), method=True, store=False, multi='perhitungan'),
				'overtime_pulang' : fields.function(fnct=function_perhitungan_absen, string='Overtime Pulang', type='float', digits=(16,2), method=True, store=False, multi='perhitungan'),
				'cepat_pulang' : fields.function(fnct=function_perhitungan_absen, string='Cepat Pulang', type='float', digits=(16,2), method=True, store=False, multi='perhitungan'),				
				'realisasi_jam_masuk' : fields.datetime(string='Realisasi Jam Masuk', readonly=True, states={'draft':[('readonly',False)]}),
				'realisasi_jam_keluar' : fields.datetime(string='Realisasi Jam Keluar', readonly=True, states={'draft':[('readonly',False)]}),
				'realisasi_mulai_istirahat' : fields.datetime(string='Realisasi Mulai Istrirahat', readonly=True, states={'draft':[('readonly',False)]}),
				'realisasi_selesai_istirahat' : fields.datetime(string='Realisasi Selesai Istirahat', readonly=True, states={'draft':[('readonly',False)]}),
				'kode_absen_id' : fields.many2one(obj='hr.kode_absen', string='Kode Absen', required=True, readonly=True, states={'draft':[('readonly',False)]}),	
				'shift_kerja_id' : fields.many2one(obj='hr.shift_kerja', string='Shift Kerja', readonly=True, states={'draft':[('readonly',False)]}),
				'timesheet_id' : fields.many2one(obj='hr.timesheet_karyawan', string='Timesheet', required=True),
				'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm')], string='Status', readonly=True),		
				'karyawan_id' : fields.related('timesheet_id','employee_id',relation='hr.employee',type='many2one',store=True,readonly=True, string='Karyawan'),
				
				# cuti
				#'lembur_id' : fields.many2one(string='Lembur', obj="hr.lembur", readonly=True),
				
				'lembur_id' : fields.char(string='Kode Absen', size=100, required=True),
				
				'overtime_datang_diakui' : fields.function(fnct=function_perhitungan_absen, string='Overtime Datang Diakui', type='float', digits=(16,2), method=True, store=False, multi='perhitungan'),
				'overtime_pulang_diakui' : fields.function(fnct=function_perhitungan_absen, string='Overtime Pulang Diakui', type='float', digits=(16,2), method=True, store=False, multi='perhitungan'),		
				}
				
	_defaults =	{
				'state' : default_state,
				}
				
	def workflow_action_confirm(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'confirm'})
		return True
		
	def name_get(self, cr, uid, ids, context=None):
		res = []
		for absensi in self.browse(cr, uid, ids):
			res.append((absensi.id,absensi.tanggal))
			
		return res
				



				
		
		
				

				
absensi()


