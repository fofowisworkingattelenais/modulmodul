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


class proses_lamaran(osv.osv):
	def default_state(self, cr, uid, context={}):
		hasil = 'draft'
		return hasil
		
	def default_name(self, cr, uid, context={}):
		return '/'

	_name = 'hr.proses_lamaran'
	_description = 'Proses Lamaran'
	_columns = {
		'name' : fields.char('# Proses', size=30, readonly=True),
		'lamaran_id' : fields.many2one('hr.lamaran', 'Lamaran'),
		'seleksi_id' : fields.many2one('hr.seleksi', 'Tahap Seleksi', required=True),
		'urutan' : fields.integer('Urutan', required=True),
		'keterangan' : fields.text('Keterangan'),
		'addons_res_id' : fields.integer('# Res Addons', readonly=True),
		'state' : fields.selection([('draft','Draft'),('lulus','Lulus'),('tidak_lulus','Tidak Lulus'),('batal','Batal')], 'Status', readonly=True),
		}

	_defaults = {
		'state' : default_state,
		'name' : default_name,
		}

	def buat_sequence(self, cr, uid, proses_lamaran_id):
		obj_ir_sequence = self.pool.get('ir.sequence')
		obj_proses_lamaran = self.pool.get('hr.proses_lamaran')

		proses_lamaran = obj_proses_lamaran.browse(cr, uid, [proses_lamaran_id])[0]
		
		sequence_id = proses_lamaran.seleksi_id.sequence_seleksi_id.id
		
		if not sequence_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk seleksi belum diset')
			return False
			
		sequence = obj_ir_sequence.get_id(cr, uid, sequence_id, 'id=%s')
		self.write(cr, uid, proses_lamaran_id, {'name' : sequence})
		return True
		
	def akhir_proses(self, cr, uid, proses_lamaran_id):
		obj_proses_lamaran = self.pool.get('hr.proses_lamaran')
		obj_tahap_seleksi = self.pool.get('hr.tahap_seleksi')
		
		proses_lamaran = obj_proses_lamaran.browse(cr, uid, [proses_lamaran_id])[0]
		
		urutan_sekarang = proses_lamaran.urutan
		
		proses_seleksi_id = proses_lamaran.lamaran_id.lowongan_id.proses_seleksi_id.id
		
		kriteria_tahap_seleksi = [('proses_seleksi_id','=',proses_seleksi_id),('urutan','>',urutan_sekarang)]
		tahap_seleksi_ids = obj_tahap_seleksi.search(cr, uid, kriteria_tahap_seleksi)
		
		if tahap_seleksi_ids:
			return False
			
		return True
		
	def lamaran_tidak_diterima(self, cr, uid, proses_lamaran_id):
		obj_proses_lamaran = self.pool.get('hr.proses_lamaran')
		wf_service = netsvc.LocalService("workflow")
		
		proses_lamaran = obj_proses_lamaran.browse(cr, uid, [proses_lamaran_id])[0]
		
		wf_service.trg_validate(uid, 'hr.lamaran', proses_lamaran.lamaran_id.id, 'button_tidakDiterima', cr)
		
		return True
		
	def lamaran_diterima(self, cr, uid, proses_lamaran_id):
		obj_proses_lamaran = self.pool.get('hr.proses_lamaran')
		wf_service = netsvc.LocalService("workflow")
		
		proses_lamaran = obj_proses_lamaran.browse(cr, uid, [proses_lamaran_id])[0]
		
		wf_service.trg_validate(uid, 'hr.lamaran', proses_lamaran.lamaran_id.id, 'button_approval', cr)
		
		return True		
		
	def buat_proses_selanjutnya(self, cr, uid, proses_lamaran_id):
		obj_proses_lamaran = self.pool.get('hr.proses_lamaran')
		obj_tahap_seleksi = self.pool.get('hr.tahap_seleksi')
		
		proses_lamaran = obj_proses_lamaran.browse(cr, uid, [proses_lamaran_id])[0]
		urutan_sekarang = proses_lamaran.urutan
		
		proses_seleksi_id = proses_lamaran.lamaran_id.lowongan_id.proses_seleksi_id.id
		
		tahap_seleksi_id = obj_tahap_seleksi.search(cr, uid, [('proses_seleksi_id', '=', proses_seleksi_id),('urutan','>',urutan_sekarang)])[0]
		
		tahap_seleksi = obj_tahap_seleksi.browse(cr, uid, [tahap_seleksi_id])[0]
		
		
		
		val = {
				'lamaran_id' : proses_lamaran.lamaran_id.id,
				'seleksi_id' : tahap_seleksi.seleksi_id.id,
				'urutan' : tahap_seleksi.urutan,
				}
				
		proses_lamaran_baru_id = obj_proses_lamaran.create(cr, uid, val)
		
		return True
		
	def create(self, cr, uid, values, context={}):
		proses_lamaran_id = super(proses_lamaran, self).create(cr, uid, values, context)
		
		if not self.buat_sequence(cr, uid, proses_lamaran_id):
			return False
			
		return proses_lamaran_id
		
	def workflow_action_lulus(self, cr, uid, ids, context={}):
		for id in ids:
			if self.akhir_proses(cr, uid, id):
				if not self.lamaran_diterima(cr, uid, id):
					return False
			else:
				if not self.buat_proses_selanjutnya(cr, uid, id):
					return False
					
			self.write(cr, uid, [id], {'state' : 'lulus'})
			
		return True

	def workflow_action_tidakLulus(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.lamaran_tidak_diterima(cr, uid, id):
				return False
						
			self.write(cr, uid, [id], {'state' : 'tidak_lulus'})
			
		return True		
		
	def workflow_action_batal(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'batal'})
			
		return True				
proses_lamaran()
