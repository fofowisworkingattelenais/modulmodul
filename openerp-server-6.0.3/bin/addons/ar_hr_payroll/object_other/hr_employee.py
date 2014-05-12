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

class hr_employee(osv.osv):
	_name = 'hr.employee'
	_inherit = 'hr.employee'
		
	def function_ketentuan_gaji_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				struktur_gaji_ids = obj_kontrak.get_all_structures(cr, uid, [karyawan.contract_id.id])
				for struktur_gaji in obj_struktur_gaji.browse(cr, uid, struktur_gaji_ids):
					if struktur_gaji.rule_ids:
						for ketentuan_gaji in struktur_gaji.rule_ids: 
							res[karyawan.id].append(ketentuan_gaji.id)			
		return res	
		
	def function_pendapatan_teratur_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')

		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.pendapatan_teratur_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.pendapatan_teratur_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.pendapatan_teratur_ids:	
					for struktur_gaji in karyawan.contract_id.pendapatan_teratur_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res
		
	def function_pendapatan_tidak_teratur_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.pendapatan_tidak_teratur_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.pendapatan_tidak_teratur_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.pendapatan_tidak_teratur_ids:	
					for struktur_gaji in karyawan.contract_id.pendapatan_tidak_teratur_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res	
		
	def function_pendapatan_tidak_teratur_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.pendapatan_tidak_teratur_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.pendapatan_tidak_teratur_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.pendapatan_tidak_teratur_ids:	
					for struktur_gaji in karyawan.contract_id.pendapatan_tidak_teratur_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res
		
	def function_potongan_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.potongan_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.potongan_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.potongan_ids:	
					for struktur_gaji in karyawan.contract_id.potongan_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res
		
	def function_potongan_kontribusi_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.potongan_kontribusi_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.potongan_kontribusi_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.potongan_kontribusi_ids:	
					for struktur_gaji in karyawan.contract_id.potongan_kontribusi_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res
		
	def function_asuransi_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.asuransi_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.asuransi_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.asuransi_ids:	
					for struktur_gaji in karyawan.contract_id.asuransi_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res
		
	def function_asuransi_kontribusi_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.asuransi_kontribusi_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.asuransi_kontribusi_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.asuransi_kontribusi_ids:	
					for struktur_gaji in karyawan.contract_id.asuransi_kontribusi_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res
		
	def function_pensiun_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.pensiun_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.pensiun_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.pensiun_ids:	
					for struktur_gaji in karyawan.contract_id.pensiun_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res
		
	def function_pensiun_kontribusi_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.pensiun_kontribusi_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.pensiun_kontribusi_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.pensiun_kontribusi_ids:	
					for struktur_gaji in karyawan.contract_id.pensiun_kontribusi_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res
		
	def function_jamsostek_ids(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		obj_struktur_gaji = self.pool.get('hr.payroll.structure')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = []
			if karyawan.contract_id:
				# ketentuan gaji menurut struktur
				if karyawan.contract_id.struct_id.jamsostek_ids:
					for struktur_gaji in karyawan.contract_id.struct_id.jamsostek_ids:
						res[karyawan.id].append(struktur_gaji.id)
						
				# ketentuan gaji menurut history
				if karyawan.contract_id.jamsostek_ids:	
					for struktur_gaji in karyawan.contract_id.jamsostek_ids:
						res[karyawan.id].append(struktur_gaji.id)						
		return res																				

		
	
	_columns =	{
				'ketentuan_gaji_ids':fields.function(function_ketentuan_gaji_ids, string='Ketentuan Gaji', type='many2many', relation='hr.salary.rule', method=True),
				'ketentuan_gaji_tambahan_ids' : fields.many2many('hr.salary.rule', 'rel_employee_salaryrule', 'employee_id', 'salaray_rule_id', 'Ketentuan Gaji Tambahan'),
				'eksekusi_penggajian_ids' : fields.one2many(obj='hr.eksekusi_penggajian', fields_id='employee_id', string='Eksekusi Penggajian'),
				
				'pendapatan_teratur_ids':fields.function(function_pendapatan_teratur_ids, string='Pendapatan Teratur', type='many2many', relation='hr.salary.rule', method=True),
				'pendapatan_tidak_teratur_ids':fields.function(function_pendapatan_tidak_teratur_ids, string='Pendapatan Tidak Teratur', type='many2many', relation='hr.salary.rule', method=True),
				'potongan_ids':fields.function(function_potongan_ids, string='Potongan', type='many2many', relation='hr.salary.rule', method=True),
				'potongan_kontribusi_ids':fields.function(function_potongan_kontribusi_ids, string='Potongan Kontribusi Perusahaan', type='many2many', relation='hr.salary.rule', method=True),
				'asuransi_ids':fields.function(function_asuransi_ids, string='Asuransi', type='many2many', relation='hr.salary.rule', method=True),
				'asuransi_kontribusi_ids':fields.function(function_asuransi_kontribusi_ids, string='Asuransi Kontribusi Perusahaan', type='many2many', relation='hr.salary.rule', method=True),	
				'pensiun_ids':fields.function(function_pensiun_ids, string='Pensiun', type='many2many', relation='hr.salary.rule', method=True),
				'pensiun_kontribusi_ids':fields.function(function_pensiun_kontribusi_ids, string='Pensiun Kontribusi Perusahaan', type='many2many', relation='hr.salary.rule', method=True),								
				'jamsostek_ids':fields.function(function_jamsostek_ids, string='Jamsostek', type='many2many', relation='hr.salary.rule', method=True),
				}

	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_employee, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_employee, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_employee, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			
	def cari_ketentuan_gaji_tambahan(self, cr, uid, employee_id):
		obj_employee = self.pool.get('hr.employee')
		obj_rule = self.pool.get('hr.salary.rule')
		
		employee = obj_employee.browse(cr, uid, [employee_id])[0]
		rule_ids = obj_rule._recursive_search_of_rules(cr, uid, employee.ketentuan_gaji_tambahan_ids, {})
				
		return rule_ids
			

		
		
			

hr_employee()




