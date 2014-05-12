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


class peringatan_karyawan(osv.osv):
	_name = 'titis.peringatan_karyawan'
	_description = 'Peringatan Karyawan'
	
	def default_name(self, cr, uid, context={}):
		return '/'
		
	def default_state(self, cr, uid, context={}):
		return 'draft'

	_columns = 	{
				'name' : fields.char(string='# Peringatan', size=30, required=True, readonly=True),
				'employee_id' : fields.many2one(obj='hr.employee', string='Karyawan', domain=['|','|',('status_karyawan','=','tetap'),('status_karyawan','=','kontrak'),('status_karyawan','=','probation')], required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'tanggal' : fields.date(string='Tanggal Diberikan', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'jenis_peringatan_id' : fields.many2one(obj='titis.jenis_peringatan', string='Jenis Peringatan', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'keterangan' : fields.text(string='Keterangan Tambahan'),
				'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'),('disetujui','Disetujui'),('ditolak','Ditolak'),('batal','Batal')], string='Status', readonly=True, required=True),

				
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
				
			self.write(cr, uid, [id], {'state' : 'disetujui'})
			
		return True		
		
	def workflow_action_ditolak(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'ditolak'})
			
		return True		
		
	def workflow_action_batal(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'batal'})
			
	def buat_sequence(self, cr, uid, id):
		"""
		Method untuk membuat nomor pengajuan cuti
		"""
		obj_sequence = self.pool.get('ir.sequence')
		obj_peringatan = self.pool.get('titis.peringatan_karyawan')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		if not user.company_id.sequence_peringatan_karyawan_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk peringatan karyawan belum diset')
			return False

		sequence_id = user.company_id.sequence_peringatan_karyawan_id.id		
		sequence = obj_sequence.get_id(cr, uid, sequence_id)
		
		obj_peringatan.write(cr, uid, [id], {'name' : sequence})
		
		return True					

		
		
		
				
	



				
		
		
				

				
peringatan_karyawan()


