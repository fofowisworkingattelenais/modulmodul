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
import netsvc


class lamaran(osv.osv):
	_name = 'hr.lamaran'
	_description = 'Lamaran'
	
	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def default_name(self, cr, uid, context={}):
		return '/'
		
	_columns = {
		'name' : fields.char('# Lamaran', size=30, readonly=True),
		'lowongan_id' : fields.many2one('hr.lowongan', 'Lowongan', required=True, domain="[('state','=','seleksi')]", readonly=True, states={'draft' : [('readonly',False)]}),
		'pelamar_id' : fields.many2one('hr.pelamar', 'Pelamar', required=True, domain="[('state','=','pelamar')]", readonly=True, states={'draft' : [('readonly',False)]}),
		'gaji_min' : fields.float('Gaji Minimum', Digits=(16,2), readonly=True, states={'limit_gaji' : [('required',True),('readonly',False)]}),
		'gaji_maks' : fields.float('Gaji Maksimum', Digits=(16,2), readonly=True, states={'limit_gaji' : [('required',True),('readonly', False)]}),
		'gaji' : fields.float('Gaji', Digits=(16,2), readonly=True, states={'nego_gaji' : [('required',True),('readonly', False)]}),
		'keterangan' : fields.text('Keterangan'),
		'proses_lamaran_ids' : fields.one2many('hr.proses_lamaran', 'lamaran_id', 'Proses Lamaran'),
		'state' : fields.selection([('draft','Draft'),('seleksi','Seleksi'),('approval','Approval'),('limit_gaji','Penentuan Limit Gaji'),('nego_gaji','Nego Gaji'),('diterima','Diterima'),('tidak_diterima','Tidak Diterima'),('batal','Batal')], 'Status', readonly=True),
		}
		
	_defaults ={
		'name' : default_name,
		'state' : default_state,
		}

	def buat_karyawan(self, cr, uid, lamaran_id):
		obj_lamaran = self.pool.get('hr.lamaran')
		obj_pelamar = self.pool.get('hr.pelamar')
		obj_employee = self.pool.get('hr.employee')
		
		lamaran = obj_lamaran.browse(cr, uid, [lamaran_id])[0]
		
		# ubah state pelamar
		obj_pelamar.write(cr, uid, [lamaran.pelamar_id.id], {'state' : 'diterima'})
		
		# buat hr.employee
		val = {
			'name' : lamaran.pelamar_id.name,
			}
			
		employee_id = obj_employee.create(cr, uid, val)
		
		return True


	def cek_gaji(self, cr, uid, lamaran_id):
		obj_lamaran = self.pool.get('hr.lamaran')
		
		lamaran = obj_lamaran.browse(cr, uid, [lamaran_id])[0]
		
		if lamaran.gaji > lamaran.gaji_maks:
			raise osv.except_osv('Peringatan!' , 'Gaji tidak boleh lebih besar dari gaji maksimum')
			return False
			
		return True
		
	def cek_limit_gaji(self, cr, uid, lamaran_id):
		obj_lamaran = self.pool.get('hr.lamaran')
		
		lamaran = obj_lamaran.browse(cr, uid, [lamaran_id])[0]
		
		if lamaran.gaji_maks <= lamaran.gaji_min:
			raise osv.except_osv('Peringatan', 'Gaji maksimal tidak boleh sama dengan atau kurang dari gaji minimum')
			return False
			
		return True
		
	def tutup_lowongan(self, cr, uid, lamaran_id):
		obj_lamaran = self.pool.get('hr.lamaran')
		obj_lowongan = self.pool.get('hr.lowongan')
		wf_service = netsvc.LocalService("workflow")
		
		lamaran = obj_lamaran.browse(cr, uid, [lamaran_id])[0]
		
		if obj_lowongan.cek_kuota(cr, uid, lamaran.lowongan_id.id):
			return True
			
		wf_service.trg_validate(uid, 'hr.lowongan', lamaran.lowongan_id.id, 'button_selesai', cr)
		return True

	def buat_sequence(self, cr, uid, lamaran_id):
		obj_ir_sequence = self.pool.get('ir.sequence')
		obj_lowongan = self.pool.get('hr.lowongan')
		obj_lamaran = self.pool.get('hr.lamaran')

		lamaran = obj_lamaran.browse(cr, uid, [lamaran_id])[0]
		
		sequence_id = lamaran.lowongan_id.sequence_lamaran_id.id
		
		if not sequence_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk lamaran belum diset')
			return False
			
		sequence = obj_ir_sequence.next_by_id(cr, uid, sequence_id)
		self.write(cr, uid, lamaran_id, {'name' : sequence})
		return True
		
	def buat_tahap_kesatu(self, cr, uid, lamaran_id):
		obj_lamaran = self.pool.get('hr.lamaran')
		obj_tahap_seleksi = self.pool.get('hr.tahap_seleksi')
		obj_proses_lamaran = self.pool.get('hr.proses_lamaran')
		
		lamaran = obj_lamaran.browse(cr, uid, [lamaran_id])[0]
		
		if not lamaran.lowongan_id.proses_seleksi_id.tahap_seleksi_ids:
			#TODO: apa yg sistem lakukaan jika proses seleksi tidk punya thapan
			pass
		else:
			tahap_seleksi_id = obj_tahap_seleksi.search(cr, uid, [('proses_seleksi_id','=',lamaran.lowongan_id.proses_seleksi_id.id),('urutan','=',1)])[0]
			
			tahap_seleksi = obj_tahap_seleksi.browse(cr, uid, [tahap_seleksi_id])[0]
			
			val = {
					'lamaran_id' : lamaran.id,
					'seleksi_id' : tahap_seleksi.seleksi_id.id,
					'urutan' : tahap_seleksi.urutan,
					}
					
			obj_proses_lamaran.create(cr, uid, val)
			
		return True
		
	def workflow_action_seleksi(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.buat_sequence(cr, uid, id):
				return False
				
			if not self.buat_tahap_kesatu(cr, uid, id):
				return False
				
			self.write(cr, uid, [id], {'state' : 'seleksi'})
			
		return True
		
	def workflow_action_approval(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'approval'})
			
		return True 
		
	def workflow_action_negoGaji(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.cek_limit_gaji(cr, uid, id):
				return False
		
			self.write(cr, uid, [id], {'state' : 'nego_gaji'})
			
		return True
		
	def workflow_action_diterima(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.cek_gaji(cr, uid, id):
				return False
				
			if not self.buat_karyawan(cr, uid, id):
				return False
						
			self.write(cr, uid, [id], {'state' : 'diterima'})
			
			if not self.tutup_lowongan(cr, uid, id):
				return False			
			
		return True
		
	def workflow_action_tidakDiterima(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'tidak_diterima'})
			
		return True		
		
	def workflow_action_batal(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'batal'})
			
		return True
		
	def workflow_action_limitGaji(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'limit_gaji'})
			
		return True
lamaran()
