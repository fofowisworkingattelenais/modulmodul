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


class lowongan(osv.osv):
	_name = 'hr.lowongan'
	_description = 'Lowongan'
	
	def default_name(self, cr, uid, context={}):
		return '/' 
		
	def default_user_request_id(self, cr, uid, context={}):
		return uid
		
	def default_state(self, cr, uid, context={}):
		return 'request'
		
	def function_jumlah_diterima(self, cr, uid, ids, field, arg, context=None):
		res = {}
		obj_lamaran = self.pool.get('hr.lamaran')
		
		for id in ids:
			lamaran_ids = obj_lamaran.search(cr, uid, [('lowongan_id','=',id),('state','=','diterima')])
			res[id] = len(lamaran_ids)
			
		return res	
		
	_columns = 	{
				'name' : fields.char('# Lowongan', size=100, required=True, readonly=True),
				'user_request_id' : fields.many2one('res.users', 'Direquest Oleh', required=True, readonly=True),
				'tanggal_request' : fields.date('Tanggal Request', required=True, readonly=True, states={'request' : [('readonly',False)]}),
				'posisi_id' : fields.many2one('hr.job', 'Posisi', required=True, readonly=True, states={'request' : [('readonly',False)]}),
				'jumlah' : fields.integer('Jumlah Dibutuhkan', required=True, readonly=True, states={'request' : [('readonly',False)]}),
				'jumlah_diterima' : fields.function(function_jumlah_diterima, method=True, string='Jumlah Diterima', store=False, type='integer'), 
				'proses_seleksi_id' : fields.many2one('hr.proses_seleksi', 'Proses Seleksi', readonly=True, states={'disetujui' : [('readonly',False),('required',True)]}),
				'sequence_lamaran_id' : fields.many2one('ir.sequence', 'Sequence Lamaran', readonly=True, states={'disetujui' : [('readonly',False),('required',True)]}),
				#'lamaran_ids' : fields.one2many('hr.lamaran', 'lowongan_id', 'Lamaran'),
				'state' : fields.selection([('request','Request'),('disetujui','Disetujui'),('seleksi','Seleksi'),('selesai','Selesai'),('batal','Batal')], 'Status', readonly=True),
				}
		
	_defaults = {
				'name' : default_name,
				'user_request_id' : default_user_request_id,
				'state' : default_state,
				}

	def buat_sequence(self, cr, uid, lowongan_id):
		obj_ir_sequence = self.pool.get('ir.sequence')
		obj_user = self.pool.get('res.users')
		obj_lowongan = self.pool.get('hr.lowongan')

		user = obj_user.browse(cr, uid, [uid])[0]

		lowongan = obj_lowongan.browse(cr, uid, [lowongan_id])[0]
		
		sequence_id = user.company_id.sequence_lowongan_id.id
		
		if not sequence_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk lowongan belum diset')
			return False
			
		sequence = obj_ir_sequence.next_by_id(cr, uid, sequence_id)
		self.write(cr, uid, lowongan_id, {'name' : sequence})
		return True
		
	def tolak_sisa_lamaran(self, cr, uid, lowongan_id):
		obj_lamaran = self.pool.get('hr.lamaran')
		wf_service = netsvc.LocalService("workflow")
		
		lamaran_ids = obj_lamaran.search(cr, uid, [('lowongan_id','=',lowongan_id),('state','in',('seleksi','approval','limit_gaji','nego_gaji'))])
		
		for lamaran_id in lamaran_ids:
			wf_service.trg_validate(uid, 'hr.lamaran', lamaran_id, 'button_tidakDiterima', cr)
			
		return True

	def cek_kuota(self, cr, uid, lowongan_id):
		obj_lowongan = self.pool.get('hr.lowongan')
		
		lowongan = obj_lowongan.browse(cr, uid, [lowongan_id])[0]
		
		if lowongan.jumlah_diterima >= lowongan.jumlah:
			return False
			
		return True
		
	def workflow_action_disetujui(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.buat_sequence(cr, uid, id):
				return False
				
			self.write(cr, uid, id, {'state' : 'disetujui'})
			
		return True
		
	def workflow_action_seleksi(self, cr, uid, ids, contet={}):
		for id in ids:
			self.write(cr, uid, id, {'state' : 'seleksi'})
			
		return True
		
	def workflow_action_selesai(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.tolak_sisa_lamaran(cr, uid, id):
				return False
		
			self.write(cr, uid, id, {'state' : 'selesai'})
			
		return True
		
	def workflow_action_batal(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, id, {'state' : 'batal'})
			
		return True
		
lowongan()
