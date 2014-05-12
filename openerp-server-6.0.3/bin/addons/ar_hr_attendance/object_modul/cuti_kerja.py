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


class cuti_kerja(osv.osv):
	_name = 'hr.cuti_kerja'
	_description = 'Cuti Kerja'
	
	def default_name(self, cr, uid, context={}):
		return '/'
		
	def default_state(self, cr, uid, context={}):
		return 'draft'

	_columns = 	{
				'name' : fields.char(string='# Pengajuan', size=30, required=True, readonly=True),
				'employee_id' : fields.many2one(obj='hr.employee', string='Karyawan', domain=['|','|',('status_karyawan','=','tetap'),('status_karyawan','=','kontrak'),('status_karyawan','=','probation')], required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'tanggal_mulai' : fields.date(string='Tanggal Mulai', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'tanggal_akhir' : fields.date(string='Tanggal Akhir', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'kode_absen_id' : fields.many2one(obj='hr.kode_absen', string='Jenis Cuti', required=True, domain=[('jenis_absen_id.tipe','=','cuti')], readonly=True, states={'draft':[('readonly',False)]}),
				'ketentuan_cuti_id' : fields.many2one(obj='hr.ketentuan_cuti', string='Ketentuan Cuti', readonly=True),
				'detail_ketentuan_cuti_id' : fields.many2one(obj='hr.detail_ketentuan_cuti', string='Detail Ketentuan Cuti', readonly=True),
				'keterangan' : fields.text(string='Keterangan Tambahan'),
				'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'),('disetujui','Disetujui'),('ditolak','Ditolak'),('batal','Batal')], string='Status', readonly=True, required=True),

				
				}
				
	_defaults =	{
				'name' : default_name,
				'state' : default_state,
				}
				
	def workflow_action_confirm(self, cr, uid, ids, context={}):
		for id in ids:
			# buat sequence
			if not self.buat_sequence(cr, uid, id):
				return False
				
			# pengecekan apakah karyawan boleh pengambil cuti ini
			jumlah_cuti = self.cek_boleh_cuti(cr, uid, id)
			if not jumlah_cuti:
				raise osv.except_osv('Peringatan!', 'Karywan tidak boleh mengambil cuti ini')
				return False
				
			# pengecekan apakah jatah cuti karyawan untuk cuti ini msh ada
			if not self.cek_jatah_cuti(cr, uid, id, jumlah_cuti):
				raise osv.except_osv('Peringatan!', 'Jatah cuti anda tidak mencukupi')
				return False
		
			self.write(cr, uid, [id], {'state' : 'confirm'})
			
		return True
		
	def workflow_action_disetujui(self, cr, uid, ids, context={}):
		for id in ids:
		
			if not self.ubah_absensi(cr, uid, id):
				return False
				
			if not self.tambahkan_ketentuan_cuti(cr, uid, id):
				return False
				
			self.write(cr, uid, [id], {'state' : 'disetujui'})
			
		return True		
		
	def workflow_action_ditolak(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'ditolak'})
			
		return True		
		
	def workflow_action_batal(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'batal'})
			
		return True		
		
		
	def buat_sequence(self, cr, uid, id):
		"""
		Method untuk membuat nomor pengajuan cuti
		"""
		obj_sequence = self.pool.get('ir.sequence')
		obj_cuti = self.pool.get('hr.cuti_kerja')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		if not user.company_id.sequence_cuti_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk pengajuan cuti belum diset')
			return False

		sequence_id = user.company_id.sequence_cuti_id.id		
		sequence = obj_sequence.next_by_id(cr, uid, sequence_id)
		
		obj_cuti.write(cr, uid, [id], {'name' : sequence})
		
		return True			
		
	def cek_boleh_cuti(self, cr, uid, id):
		"""
		Method untuk mengecek apakah karyawan berhak mengambil cuti ini
		
		Return :
		mengembalikan jumlah hari yang masih boleh diambil
		"""
		
		obj_cuti = self.pool.get('hr.cuti_kerja')
		obj_detail = self.pool.get('hr.detail_ketentuan_cuti')
		
		cuti = obj_cuti.browse(cr, uid, [id])[0]
		tahun = int(cuti.tanggal_mulai[0:4])
		#raise osv.except_osv('a', str(tahun))
		kriteria = [('ketentuan_cuti_id.tahun','=',tahun),('ketentuan_cuti_id.employee_id.id','=',cuti.employee_id.id),('kode_absen_id.id','=',cuti.kode_absen_id.id),('ketentuan_cuti_id.state','=','confirm')]
		
		detail_ids = obj_detail.search(cr, uid, kriteria)
		if not detail_ids:
			return False
		else:
			detail = obj_detail.browse(cr, uid, detail_ids)[0]
			return detail.jumlah_diperbolehkan - int(detail.jumlah_digunakan)
		
	def cek_jatah_cuti(self, cr, uid, id, jumlah_hari):
		"""
		Method untuk mengecek apakah karyawan masih mempunyai jatah cuti ini
		"""
		obj_cuti = self.pool.get('hr.cuti_kerja')
		
		cuti = obj_cuti.browse(cr, uid, [id])[0]
		
		dt_tanggal_mulai = date(int(cuti.tanggal_mulai[0:4]), int(cuti.tanggal_mulai[5:7]), int(cuti.tanggal_mulai[8:10]))
		dt_tanggal_akhir = date(int(cuti.tanggal_akhir[0:4]), int(cuti.tanggal_akhir[5:7]), int(cuti.tanggal_akhir[8:10]))
		
		ord_tanggal_mulai = dt_tanggal_mulai.toordinal()
		ord_tanggal_akhir = dt_tanggal_akhir.toordinal()
		
		permohonan = ord_tanggal_akhir - ord_tanggal_mulai + 1
		
		if permohonan > jumlah_hari:
			return False
		else:
			return True
		
	def ubah_absensi(self, cr, uid, id):
		"""
		Method untuk mengubah absensi jika cuti disetujui
		"""
		obj_cuti = self.pool.get('hr.cuti_kerja')
		obj_absensi = self.pool.get('hr.absensi')
		cuti = obj_cuti.browse(cr, uid, [id])[0]
		
		kriteria = [('timesheet_id.employee_id.id','=',cuti.employee_id.id),('tanggal','>=',cuti.tanggal_mulai),('tanggal','<=',cuti.tanggal_akhir)]
		absensi_ids = obj_absensi.search(cr, uid, kriteria)
		
		if absensi_ids:
			for absensi in obj_absensi.browse(cr, uid, absensi_ids):
				res =	{
							'kode_absen_id' : cuti.kode_absen_id.id,
							}	
							
				obj_absensi.write(cr, uid, [absensi.id], res)
				obj_absensi.workflow_action_confirm(cr, uid, [absensi.id])
		
		return True
		
	def tambahkan_ketentuan_cuti(self, cr, uid, id):
		obj_cuti = self.pool.get('hr.cuti_kerja')
		obj_detail = self.pool.get('hr.detail_ketentuan_cuti')
		
		cuti = obj_cuti.browse(cr, uid, [id])[0]
		tahun = int(cuti.tanggal_mulai[0:4])
		kriteria = [('ketentuan_cuti_id.tahun','=',tahun),('ketentuan_cuti_id.employee_id.id','=',cuti.employee_id.id),('kode_absen_id.id','=',cuti.kode_absen_id.id),('ketentuan_cuti_id.state','=','confirm')]
		
		detail_ids = obj_detail.search(cr, uid, kriteria)
		if not detail_ids:
			return False
		else:
			res =	{
						'detail_ketentuan_cuti_id' : detail_ids[0],
						}
			obj_cuti.write(cr, uid, id, res)
			return True	
		
		
		
				
	



				
		
		
				

				
cuti_kerja()


