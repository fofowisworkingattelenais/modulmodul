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


class lembur(osv.osv):
	_name = 'hr.lembur'
	_description = 'Lembur'

	def default_name(self, cr, uid, context={}):
		return '/'
		
	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	_columns = 	{
								'name' : fields.char(string='# Permohonan Lembur', size=30, required=True, readonly=True),
								'employee_id' : fields.many2one(string='Karyawan', obj='hr.employee', domain=['|','|',('status_karyawan','=','tetap'),('status_karyawan','=','kontrak'),('status_karyawan','=','probation')], required=True, readonly=True, states={'draft':[('readonly',False)]}),
								'tanggal_permohonan' : fields.date(string='Tanggal Permohonan', required=True, readonly=True, states={'draft':[('readonly',False)]}),
								'flag_sebelum' : fields.boolean(string='Sebelum Shift', readonly=True, states={'draft':[('readonly',False)]}),
								'jumlah_menit_sebelum' : fields.integer(string='Jumlah Menit Sebelum', readonly=True, states={'draft':[('readonly',False)]}),
								'flag_setelah' : fields.boolean(string='Setelah Shift', readonly=True, states={'draft':[('readonly',False)]}),
								'jumlah_menit_setelah' : fields.integer(string='Jumlah Menit Setelah', readonly=True, states={'draft':[('readonly',False)]}),
								'keterangan' : fields.text(string='Keterangan'),
								'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'),('disetujui','Disetujui'),('ditolak','Ditolak'),('batal','Batal')], string='Status', readonly=True),

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
		
	def workflow_action_disetujui(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.ubah_absensi(cr, uid, id):
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
		Method untuk membuat nomor permohonan lembur
		"""
		obj_sequence = self.pool.get('ir.sequence')
		obj_lembur = self.pool.get('hr.lembur')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		if not user.company_id.sequence_lembur_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk pengajuan lembur belum diset')
			return False

		sequence_id = user.company_id.sequence_lembur_id.id		
		sequence = obj_sequence.next_by_id(cr, uid, sequence_id)
		
		self.write(cr, uid, [id], {'name' : sequence})
					
		return True
		
	def ubah_absensi(self, cr, uid, id):
		obj_absensi = self.pool.get('hr.absensi')
		lembur = self.browse(cr, uid, [id])[0]
		kriteria = [('tanggal','=', lembur.tanggal_permohonan),('timesheet_id.employee_id.id','=',lembur.employee_id.id)]
		absensi_ids = obj_absensi.search(cr, uid, kriteria)
		if absensi_ids:
			val 	=	{
						'lembur_id' : lembur.id
						}
			obj_absensi.write(cr, uid, [absensi_ids[0]], val)
			
		return True
		
				
lembur()


