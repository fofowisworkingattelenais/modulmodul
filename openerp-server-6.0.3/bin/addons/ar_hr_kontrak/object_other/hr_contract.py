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
from datetime import date, time, datetime
from tools.safe_eval import safe_eval as eval
import unicodedata

class hr_contract(osv.osv):
	_name = 'hr.contract'
	_inherit = 'hr.contract'
	
	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def default_name(self, cr, uid, context={}):
		return '/'		


	_columns =	{
				'name': fields.char('Contract Reference', size=64, required=True, readonly=True),
				'employee_id': fields.many2one('hr.employee', 'Employee', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'company_id': fields.many2one('res.company', 'Perusahaan', readonly=True, states={'draft':[('readonly',False)]}),
				'department_id': fields.many2one('hr.department', 'Unit Kerja', readonly=True, states={'draft':[('readonly',False)]}),
				'manager_id': fields.many2one('hr.employee', 'Supervisor', readonly=True, states={'draft':[('readonly',False)]}),
				'type_id': fields.many2one('hr.contract.type', 'Contract Type', readonly=True, states={'draft':[('readonly',False)]}),
				'job_id': fields.many2one('hr.job', 'Job Title', readonly=True, states={'draft':[('readonly',False)]}),
				'date_start': fields.date('Start Date'),
				'date_end': fields.date('End Date'),
				'tanggal_mulai': fields.date('Tanggal Mulai', required=True, readonly=True, states={'draft':[('readonly',False)]}),								
				'mulai_otomatis' : fields.boolean('Mulai Otomatis', readonly=True, states={'draft':[('readonly',False)]}),
				'trial_date_start': fields.date('Trial Start Date', readonly=True, states={'draft':[('readonly',False)]}),
				'trial_date_end': fields.date('Trial End Date', readonly=True, states={'draft':[('readonly',False)]}),
				'working_hours': fields.many2one('resource.calendar','Working Schedule', readonly=True, states={'draft':[('readonly',False)]}),
				'wage': fields.float('Wage', digits=(16,2),  help="Basic Salary of the employee", readonly=True, states={'draft':[('readonly',False)]}),
				'advantages': fields.text('Advantages', readonly=True, states={'draft':[('readonly',False)]}),
				'notes': fields.text('Notes'),
				'permit_no': fields.char('Work Permit No', size=256, required=False, readonly=True, states={'draft':[('readonly',False)]}),
				'visa_no': fields.char('Visa No', size=64, required=False, readonly=True, states={'draft':[('readonly',False)]}),
				'visa_expire': fields.date('Visa Expire Date', readonly=True, states={'draft':[('readonly',False)]}),	
				'tipe_history_id' : fields.many2one('hr.tipe_history', 'Tipe History', required=True, readonly=True, states={'draft':[('readonly',False)]}),	
				'history_sebelum_id' : fields.many2one(obj='hr.contract', string='# History Sebelum', readonly=True),
				'periode_gaji_id': fields.many2one('hr.periode_gaji', 'Periode Gaji', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'state' : fields.selection([('draft','Draft'),('valid','Valid'),('batal','Batal'),('selesai','Selesai')], 'Status', readonly=True),
				
				# konfigurasi visibilitas
				'visibilitas_ruang_lingkup_pekerjaan' : fields.boolean(string='Ruang Lingkup Pekerjaan'),
				'visibilitas_kategori_karyawan' : fields.boolean(string='Kategori Karyawan'),
				'visibilitas_remunerasi' : fields.boolean(string='Remunerasi'),
				'visibilitas_absensi' : fields.boolean(string='Absensi'),
				
				# konfigurasi required
				'required_ruang_lingkup_pekerjaan' : fields.boolean(string='Ruang Lingkup Pekerjaan'),
				'required_kategori_karyawan' : fields.boolean(string='Kategori Karyawan'),
				'required_remunerasi' : fields.boolean(string='Remunerasi'),
				'required_absensi' : fields.boolean(string='Absensi'),
				}
				
	_defaults =	{
				'state' : default_state,
				'name' : default_name,
				}

	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		a = self.copy_history_sebelumnya(cr, uid, values['employee_id'], values['tipe_history_id'], values)
		
		#raise osv.except_osv('Peringatan', str(a))
		
		#values.update(a)
		
		if situasi == 'aman':
			return super(hr_contract, self).create(cr, uid, a, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_contract, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		"""
		Data tidak bisa dihapus
		"""
		
		raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')

		
	def workflow_action_valid(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.buat_sequence(cr, uid, id):
				return False
				
			if not self.jalankan_kode_python(cr, uid, id):
				return False
				
			if not self.log_history(cr, uid, id):
				return False
				
			if not self.selesaikan_kontrak_aktif(cr, uid, id):
				return False
				
			self.write(cr, uid, [id], {'state' : 'valid'})
		return True		
		
	def workflow_action_batal(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.kembali_history_sebelumnya(cr, uid, id):
				return False
						
			self.write(cr, uid, [id], {'state' : 'batal'})
			
		return True		
		
	def workflow_action_selesai(self, cr, uid, ids, context={}):
		for id in ids:

				
			self.write(cr, uid, [id], {'state' : 'selesai'})
			
		return True		
	
		
	def buat_sequence(self, cr, uid, contract_id, context=None):
		"""
		Buat sequence
		"""
		
		obj_user = self.pool.get('res.users')
		obj_sequence = self.pool.get('ir.sequence')
		obj_contract = self.pool.get('hr.contract')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		kontrak = obj_contract.browse(cr, uid, [contract_id])[0]
		
		# jika kontrak sudah mendapatkan name, maka tidak perlu buat sequence
		if kontrak.name != '/':
			return True		
		
		# buat sequence
		if not user.company_id.sequence_kontrak_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk history karyawan belum diset')
			return False
		elif user.company_id.sequence_kontrak_id:
			sequence_id = user.company_id.sequence_kontrak_id.id
			sequence = obj_sequence.next_by_id(cr, uid, sequence_id)
			obj_contract.write(cr, uid, [contract_id], {'name' : sequence})
			return True		
			
	def selesaikan_kontrak_aktif(self, cr, uid, kontrak_id):
		"""
		Buat agar history aktif menjadi selesai
		"""
		
		obj_kontrak = self.pool.get('hr.contract')
		
		kontrak = obj_kontrak.browse(cr, uid, [kontrak_id])[0]
		
		if kontrak.history_sebelum_id:
			wf_service = netsvc.LocalService('workflow')
			wf_service.trg_validate(uid, 'hr.contract', kontrak.history_sebelum_id.id, 'button_selesai', cr)		
			
			
		return True			
		
		
	def jalankan_kode_python(self, cr, uid, kontrak_id):
		"""
		Menjalankan method tertentu tergantung dengan tipe history
		"""
		
		obj_kontrak = self.pool.get('hr.contract')
		
		kontrak = obj_kontrak.browse(cr, uid, [kontrak_id])[0]
		
		localdict =	{
					'kontrak' : kontrak,
					'self' : self,
					'cr' : cr,
					'uid' : uid,
					}
					
		try:
			eval(kontrak.tipe_history_id.kode_python, localdict, mode='exec', nocopy=True)
		except:
			raise osv.except_osv('Peringatan!', 'Kode python salah')	
			
		return True
		
	def onchange_tipe_history_id(self, cr, uid, ids, tipe_history_id):
		domain = {}
		value = {}
		obj_tipe_history = self.pool.get('hr.tipe_history')
		

		
		
		value.update({'employee_id' : False})
		domain.update({'employee_id' : [('id','in',[])]})
		
		

					
		if tipe_history_id:
			try:
				tipe_history = obj_tipe_history.browse(cr, uid, [tipe_history_id])[0]
				localdict =	{
							'self' : self,
							'cr' : cr,
							'uid' : uid,
							'tipe_history' : tipe_history,
							'karyawan_ids' : [],
							'value' : value,
							}				
				eval(tipe_history.kode_python_karyawan, localdict, mode='exec', nocopy=True)
				karyawan_ids = localdict['karyawan_ids']

			except:
				karyawan_ids = []
			value = localdict['value']
			domain.update({'employee_id' : [('id','in',karyawan_ids)]})
			
					
		return {'value' : value, 'domain' : domain}
		
	def kembali_history_sebelumnya(self, cr, uid, id):
		"""
		Method untuk mengembalikan history aktif karyawan ke history sebelumnya, jika ada
		"""
		obj_history = self.pool.get('hr.contract')
		obj_karyawan = self.pool.get('hr.employee')
		
		# aktifkan history sebelumnya
		history = obj_history.browse(cr, uid, [id])[0]
		
		if history.history_sebelum_id:
			if not self.jalankan_kode_python(cr, uid, history.history_sebelum_id.id):
				return False
		
			obj_history.write(cr, uid, [history.history_sebelum_id.id], {'state' : 'valid'})
		else:
		
			obj_karyawan.write(cr, uid, [history.employee_id.id], {'status_karyawan' : 'draft'})
		
		# ubah field history yang dibatalkan
		obj_history.write(cr, uid, [id], {'status' : 'batal'})
		
		return True
		
	def log_history(self, cr, uid, id):
		"""
		Menyimpan informasi history aktif sebelumnya
		"""
		obj_history = self.pool.get('hr.contract')
		
		history = obj_history.browse(cr, uid, [id])[0]
		
		history_aktif_id = history.employee_id.contract_id and history.employee_id.contract_id.id or False
				
		if not history_aktif_id:
			pass
		else:
			obj_history.write(cr, uid, [id], {'history_sebelum_id' : history_aktif_id})
		
		return True		
		
	def copy_history_sebelumnya(self, cr, uid, karyawan_id, tipe_history_id, value):
		"""
		Mengambil data dari history sebelumnya
		"""
		
		obj_employee = self.pool.get('hr.employee')
		obj_tipe_history = self.pool.get('hr.tipe_history')
		obj_history = self.pool.get('hr.contract')
		
		employee = obj_employee.browse(cr, uid, [karyawan_id])[0]
		tipe_history = obj_tipe_history.browse(cr, uid, [tipe_history_id])[0]
		
		val = {}

		# Buat list untuk method read
		list_field = []
		if tipe_history.field_copy_ids:
			for field_copy in tipe_history.field_copy_ids:
				list_field.append(field_copy.name.encode('ascii', 'ignore'))

				
		if not employee.contract_id:
			return value

		dict_history = obj_history.read(cr, uid, [employee.contract_id.id], list_field)[0]
		fields = obj_history.fields_get(cr, uid)
		
		
		for item_dict in dict_history:
			if item_dict == 'id':
				continue
				
			if fields[item_dict]['type'] == 'many2one':
				dict_history[item_dict] = dict_history[item_dict][0]
				value[item_dict] = dict_history[item_dict]
			elif fields[item_dict]['type'] == 'one2many':
				#TODO
				pass
			elif fields[item_dict]['type'] == 'many2many':
				dict_history[item_dict] = [(6, 0, dict_history[item_dict])]
				value[item_dict] = dict_history[item_dict]
				
			
		
				
		return value
					
		
			
			
		
		
			

hr_contract()




