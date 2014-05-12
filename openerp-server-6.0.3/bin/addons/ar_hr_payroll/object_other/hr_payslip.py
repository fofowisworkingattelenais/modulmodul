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
import pooler

class one2many_mod3(fields.one2many):
	def get(self, cr, obj, ids, name, user=None, offset=0, context=None, values=None):
		obj_payslip = pooler.get_pool(cr.dbname).get('hr.payslip')

		if context is None:
			context = {}
		if self._context:
			context = context.copy()
		context.update(self._context)
		if values is None:
			values = {}

		res = {}
		ids2 = []
		for id in ids:
			res[id] = [] 
			rule_ids = []
			payslip = obj_payslip.browse(cr, user, [id])[0]
			if payslip.struct_id.jamsostek_ids:
				for jamsostek in payslip.struct_id.jamsostek_ids:
					 rule_ids.append(jamsostek.id)

			ids2 += obj.pool.get(self._obj).search(cr, user, self._domain + [(self._fields_id, 'in', ids),('salary_rule_id','in',rule_ids)], limit=self._limit, context=context)
		
		for r in obj.pool.get(self._obj)._read_flat(cr, user, ids2, [self._fields_id], context=context, load='_classic_write'):
			if r[self._fields_id] in res:
			    res[r[self._fields_id]].append(r['id'])
		return res

class hr_payslip(osv.osv):
	_name = 'hr.payslip'
	_inherit = 'hr.payslip'

	def default_number(self, cr, uid, context={}):
		return '/'
		
	def default_date_from(self, cr, uid, context={}):
		return False
		
	def default_date_to(self, cr, uid, context={}):
		return False
		
	def function_date_from(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			if not payslip.detail_periode_gaji_id:
				res[payslip.id] = False
			else:
				res[payslip.id] = payslip.detail_periode_gaji_id.tanggal_mulai
				
		return res
		
	def function_date_to(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			if not payslip.detail_periode_gaji_id:
				res[payslip.id] = False
			else:
				res[payslip.id] = payslip.detail_periode_gaji_id.tanggal_akhir
				
		return res
		
	def function_contract_id(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			if not payslip.employee_id:
				res[payslip.id] = False
			else:
				res[payslip.id] = payslip.employee_id.contract_id.id
				
		return res
		
	def function_struct_id(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			if not payslip.employee_id:
				res[payslip.id] = False
			else:
				res[payslip.id] = payslip.employee_id.contract_id.struct_id.id
				
		return res	
		
	
		
	def function_total_pendapatan_teratur(self, cr, uid, ids, field_name, args, context=None):					

		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.detail_pendapatan_teratur_ids:
				for line in payslip.detail_pendapatan_teratur_ids:
					res[payslip.id] += line.total
			
		return res
		
	def function_total_pendapatan_tidak_teratur(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.detail_pendapatan_tidak_teratur_ids:
				for line in payslip.detail_pendapatan_tidak_teratur_ids:
					res[payslip.id] += line.total
			
		return res				
		

		
	def function_total_potongan(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.detail_potongan_ids:
				for line in payslip.detail_potongan_ids:
					res[payslip.id] += line.total
			
		return res
		
	def function_total_potongan_perusahaan(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.detail_potongan_perusahaan_ids:
				for line in payslip.detail_potongan_perusahaan_ids:
					res[payslip.id] += line.total
			
		return res			
		
	def function_total_asuransi(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')

		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.detail_asuransi_ids:
				for line in payslip.detail_asuransi_ids:
					res[payslip.id] += line.total
			
		return res
		
	def function_total_asuransi_perusahaan(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')


		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.detail_asuransi_perusahaan_ids:
				for line in payslip.detail_asuransi_perusahaan_ids:
					res[payslip.id] += line.total
			
		return res			
		
	def function_total_pensiun(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.detail_pensiun_ids:
				for line in payslip.detail_pensiun_ids:
					res[payslip.id] += line.total
			
		return res	
		
	def function_total_pensiun_perusahaan(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.detail_pensiun_perusahaan_ids:
				for line in payslip.detail_pensiun_perusahaan_ids:
					res[payslip.id] += line.total
			
		return res		
		
	def function_total_jamsostek(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.detail_jamsostek_ids:
				for line in payslip.detail_jamsostek_ids:
					res[payslip.id] += line.total
			
		return res				
		
	def function_total_thp(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = payslip.total_pendapatan_teratur + payslip.total_pendapatan_teratur - payslip.total_potongan - payslip.total_asuransi - payslip.total_pensiun + payslip.total_potongan_perusahaan + payslip.total_asuransi_perusahaan + payslip.total_pensiun_perusahaan
			
		return res							
			

	_columns =	{
				'contract_id' : fields.function(function_contract_id, string='History', type='many2one', relation='hr.contract'),
				'struct_id' : fields.function(function_struct_id, string='Struktur Gaji', type='many2one', relation='hr.payroll.structure'),
				'date_from' : fields.function(function_date_from, string='Tanggal Mulai', type='date'),
				'date_to' : fields.function(function_date_to, string='Tanggal Akhir', type='date'),
				
				'total_thp' : fields.function(fnct=function_total_thp, string='Total THP', type='float', digits=(16,2), method=True, store=False),
				'detail_periode_gaji_id' : fields.many2one('hr.detail_periode_gaji', 'Periode Gaji', required=True),
				'number': fields.char('Reference', size=64, required=False, readonly=True),
				'tanggal_slip' : fields.date(string='Tanggal Slip Gaji', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'payslip_run_id': fields.many2one('hr.payslip.run', '# Batches', readonly=True, required=True),
				
				# Pendapatan Teratur
				'detail_pendapatan_teratur_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Pendapatan Teratur', domain=[('category_id.parent_id.name', '=', 'Pendapatan Teratur')], readonly=True, states={'draft':[('readonly',False)]}),
				'total_pendapatan_teratur' : fields.function(fnct=function_total_pendapatan_teratur, string='Total Pendapatan Teratur', type='float', digits=(16,2), method=True, store=False),
				
				# Pendapatan Tidak Teratur
				'detail_pendapatan_tidak_teratur_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Pendapatan Tidak Teratur', domain=[('category_id.parent_id.name', '=', 'Pendapatan Tidak Teratur')], readonly=True, states={'draft':[('readonly',False)]}),					
				'total_pendapatan_tidak_teratur' : fields.function(fnct=function_total_pendapatan_tidak_teratur, string='Total Pendapatan Tidak Teratur', type='float', digits=(16,2), method=True, store=False),
				
				# Potongan
				'detail_potongan_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Potongan', domain=[('category_id.parent_id.name', '=', 'Potongan')], readonly=True, states={'draft':[('readonly',False)]}),
				'detail_potongan_karyawan_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Potongan Kontribusi Karyawan', domain=[('category_id.parent_id.name', '=', 'Potongan'),('register_id','=',False)], readonly=True),
				'detail_potongan_perusahaan_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Potongan Kontribusi Perusahaan', domain=[('category_id.parent_id.name', '=', 'Potongan'),('register_id','!=',False)], readonly=True),
				'total_potongan' : fields.function(fnct=function_total_potongan, string='Total Potongan', type='float', digits=(16,2), method=True, store=False),
				'total_potongan_perusahaan' : fields.function(fnct=function_total_potongan_perusahaan, string='Total Potongan Kontribusi Perusahaan', type='float', digits=(16,2), method=True, store=False),
				
				# Asuransi
				'detail_asuransi_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Asuransi', domain=[('category_id.parent_id.name', '=', 'Asuransi')], readonly=True, states={'draft':[('readonly',False)]}),
				'detail_asuransi_karyawan_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Asuransi Kontribusi Karyawan', domain=[('category_id.parent_id.name', '=', 'Asuransi'),('register_id','=',False)], readonly=True),
				'detail_asuransi_perusahaan_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Asuransi Kontribusi Perusahaan', domain=[('category_id.parent_id.name', '=', 'Asuransi'),('register_id','!=',False)], readonly=True),
				'total_asuransi' : fields.function(fnct=function_total_asuransi, string='Total Asuransi', type='float', digits=(16,2), method=True, store=False),
				'total_asuransi_perusahaan' : fields.function(fnct=function_total_asuransi_perusahaan, string='Total Asuransi Kontribusi Perusahaan', type='float', digits=(16,2), method=True, store=False),

				# Pensiun
				'detail_pensiun_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Pensiun', domain=[('category_id.parent_id.name', '=', 'Pensiun')], readonly=True, states={'draft':[('readonly',False)]}),
				'detail_pensiun_karyawan_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Pensiun Kontribusi Karyawan', domain=[('category_id.parent_id.name', '=', 'Pensiun'),('register_id','=',False)], readonly=True),
				'detail_pensiun_perusahaan_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Pensiun Kontribusi Perusahaan', domain=[('category_id.parent_id.name', '=', 'Pensiun'),('register_id','!=',False)], readonly=True),																
				'total_pensiun' : fields.function(fnct=function_total_pensiun, string='Total Pensiun', type='float', digits=(16,2), method=True, store=False),
				'total_pensiun_perusahaan' : fields.function(fnct=function_total_pensiun_perusahaan, string='Total Pensiun Kontribusi Perusahaan', type='float', digits=(16,2), method=True, store=False),
				
				'detail_jamsostek_ids': one2many_mod3('hr.payslip.line', 'slip_id', 'Detail Perhitungan Jamsostek', readonly=True),
				'total_jamsostek' : fields.function(fnct=function_total_jamsostek, string='Total Jamsostek', type='float', digits=(16,2), method=True, store=False),
				'detail_jamsostek_perusahaan_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Jamsostek Kontribusi Perusahaan', domain=[('category_id.name', 'in', ('Jaminan Hari Tua','Jaminan Kecelakaan Kerja','Jaminan Kematian','Jaminan Pemeliharaan Kesehatan')),('register_id','!=',False)], readonly=True),
				'detail_jamsostek_karyawan_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Detail Jamsostek Kontribusi Karyawan', domain=[('category_id.name', 'in', ('Jaminan Hari Tua','Jaminan Kecelakaan Kerja','Jaminan Kematian','Jaminan Pemeliharaan Kesehatan')),('register_id','=',False)], readonly=True),
				
				}
				
	_defaults =	{
				'number' : default_number,
				'date_from' : default_date_from,
				'date_to' : default_date_to,
				}


	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_payslip, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_payslip, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_payslip, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			
	def hr_verify_sheet(self, cr, uid, ids, context=None):
		"""
		Method untuk button Confirm pada form hr.payslip
		"""
		obj_payslip = self.pool.get('hr.payslip')


		
		for id in ids:
			if not self.buat_sequence(cr, uid, id):
				return False
				
			obj_payslip.write(cr, uid, [id], {'state': 'verify'}, context)
			
		return True
			

		
		
	def onchange_detail_periode_gaji_id(self, cr, uid, ids, detail_periode_gaji_id):
		"""
		Method on_change untuk field detail_periode_gaji_id
		"""
		value = {}
		obj_detail_periode_gaji = self.pool.get('hr.detail_periode_gaji')
		
		if detail_periode_gaji_id:
			detail_periode_gaji = obj_detail_periode_gaji.browse(cr, uid, [detail_periode_gaji_id])[0]
			
			value.update({'date_from' : detail_periode_gaji.tanggal_mulai, 'date_from' : detail_periode_gaji.tanggal_akhir })
			
		return {'value' : value}
		
	def onchange_karyawan_id(self, cr, uid, ids, employee_id):
		"""
		Method on_change untuk field employee_id
		"""
		obj_karyawan = self.pool.get('hr.employee')
		obj_detail_periode_gaji = self.pool.get('hr.detail_periode_gaji')
		
		value = {}
		if employee_id:
			karyawan = obj_karyawan.browse(cr, uid, [employee_id])[0]
			periode_gaji_id = karyawan.contract_id.periode_gaji_id.id
		
			kriteria = [('periode_gaji_id','=',periode_gaji_id),('state','=','aktif')]
			detail_periode_gaji_ids = obj_detail_periode_gaji.search(cr, uid, kriteria)
		
			if detail_periode_gaji_ids:
				value.update({'detail_periode_gaji_id' : detail_periode_gaji_ids[0]})
			else:
				value.update({'detail_periode_gaji_id' : False})
				
			
				
		else:
			value.update({'detail_periode_gaji_id' : False})
			
		return {'value' : value}

		
	def compute_sheet(self, cr, uid, ids, context=None):
		"""
		Overloading penuh method ini
		"""
		obj_slip_line = self.pool.get('hr.payslip.line')
		obj_sequence = self.pool.get('ir.sequence')
		obj_payslip = self.pool.get('hr.payslip')
		obj_eksekusi_penggajian = self.pool.get('hr.eksekusi_penggajian')
	
		for payslip in obj_payslip.browse(cr, uid, ids, context=context):
			# Hapus payslip lama
			# TODO: pemborosan auto inc. Sebaiknya cari cara lain
			
			old_slipline_ids = obj_slip_line.search(cr, uid, [('slip_id', '=', payslip.id)], context=context)
			if old_slipline_ids:
			    obj_slip_line.unlink(cr, uid, old_slipline_ids, context=context)
			    
			# TODO: Pertimbangan untuk menghapus bagian kode ini karena contract_id sudah dijadikan field functional
			if payslip.contract_id:
			    contract_ids = [payslip.contract_id.id]
			else:
			    contract_ids = self.get_contract(cr, uid, payslip.employee_id, payslip.date_from, payslip.date_to, context=context)
			    
			for line in obj_payslip.get_payslip_lines(cr, uid, contract_ids, payslip.id, context=context):
				line.update({'slip_id' : payslip.id})
				slip_id = obj_slip_line.create(cr, uid, line)
				
				
				obj_slip_line.write(cr, uid, [slip_id], {'eksekusi_penggajian_id' : line['eksekusi_penggajian_id']})
				
				
				if line['eksekusi_penggajian_id']:
					obj_eksekusi_penggajian.write(cr, uid, [line['eksekusi_penggajian_id']], {'payslip_line_id' : slip_id})
		return True	
		
	def list_jadwal_penggajian(self, cr, uid, payslip_id):
		"""
		Mengembalikan ketentuan penggajian yang harus dihitung untuk karyawan dan tanggal pada payslip
		
		Param :
		- payslip_id : int. ID dari payslip
		
		Return :
		- Tuple dalam tuple
		"""
		obj_payslip = self.pool.get('hr.payslip')
		obj_jadwal_penggajian = self.pool.get('hr.jadwal_penggajian')
		obj_eksekusi_penggajian = self.pool.get('hr.eksekusi_penggajian')
		
		payslip = obj_payslip.browse(cr, uid, [payslip_id])[0]
		
		a = []
		
		kriteria1 = [('tanggal_penggajian','=',payslip.tanggal_slip)]
		
		jadwal_penggajian_ids = obj_jadwal_penggajian.search(cr, uid, kriteria1)
		
		if not jadwal_penggajian_ids : return a

		kriteria2 = [('employee_id','=',payslip.employee_id.id), ('jadwal_penggajian_id','in',jadwal_penggajian_ids),('state','=','draft')]
		eksekusi_penggajian_ids = obj_eksekusi_penggajian.search(cr, uid, kriteria2)
		
		if not eksekusi_penggajian_ids : return a
		
		for eksekusi_penggajian in obj_eksekusi_penggajian.browse(cr, uid, eksekusi_penggajian_ids):
		    a.append((eksekusi_penggajian.jadwal_penggajian_id.salary_rule_id.id, eksekusi_penggajian.jadwal_penggajian_id.salary_rule_id.sequence, eksekusi_penggajian.id))
		
		return a
		
	def list_jamsostek_rule(self, cr, uid, payslip_id):
		"""
		Mengembalikan list dari salary rule untuk jamsostek
		"""
		obj_payslip = self.pool.get('hr.payslip')
		
		payslip = obj_payslip.browse(cr, uid, [payslip_id])[0]
		
		a = []
		
		#if payslip.contract_id.jamsostek_perusahaan_ids:
			#for jamsostek_perusahaan in payslip.contract_id.jamsostek_perusahaan_ids:
				#a.append((jamsostek_perusahaan.id, jamsostek_perusahaan.sequence, False))
				
		#if payslip.contract_id.jamsostek_karyawan_ids:
			#for jamsostek_karyawan in payslip.contract_id.jamsostek_karyawan_ids:
				#a.append((jamsostek_karyawan.id, jamsostek_karyawan.sequence, False))				
		
		return a					
		
	def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, context):
		def _sum_salary_rule_category(localdict, category, amount):
		    if category.parent_id:
		        localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
		    localdict['categories'].dict[category.code] = category.code in localdict['categories'].dict and localdict['categories'].dict[category.code] + amount or amount
		    return localdict

		class BrowsableObject(object):
		    def __init__(self, pool, cr, uid, employee_id, dict):
		        self.pool = pool
		        self.cr = cr
		        self.uid = uid
		        self.employee_id = employee_id
		        self.dict = dict

		    def __getattr__(self, attr):
		        return attr in self.dict and self.dict.__getitem__(attr) or 0.0

		class InputLine(BrowsableObject):
		    """a class that will be used into the python code, mainly for usability purposes"""
		    def sum(self, code, from_date, to_date=None):
		        if to_date is None:
		            to_date = datetime.now().strftime('%Y-%m-%d')
		        result = 0.0
		        self.cr.execute("SELECT sum(amount) as sum\
		                    FROM hr_payslip as hp, hr_payslip_input as pi \
		                    WHERE hp.employee_id = %s AND hp.state = 'done' \
		                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
		                   (self.employee_id, from_date, to_date, code))
		        res = self.cr.fetchone()[0]
		        return res or 0.0

		class WorkedDays(BrowsableObject):
		    """a class that will be used into the python code, mainly for usability purposes"""
		    def _sum(self, code, from_date, to_date=None):
		        if to_date is None:
		            to_date = datetime.now().strftime('%Y-%m-%d')
		        result = 0.0
		        self.cr.execute("SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours\
		                    FROM hr_payslip as hp, hr_payslip_worked_days as pi \
		                    WHERE hp.employee_id = %s AND hp.state = 'done'\
		                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
		                   (self.employee_id, from_date, to_date, code))
		        return self.cr.fetchone()

		    def sum(self, code, from_date, to_date=None):
		        res = self._sum(code, from_date, to_date)
		        return res and res[0] or 0.0

		    def sum_hours(self, code, from_date, to_date=None):
		        res = self._sum(code, from_date, to_date)
		        return res and res[1] or 0.0

		class Payslips(BrowsableObject):
		    """a class that will be used into the python code, mainly for usability purposes"""

		    def sum(self, code, from_date, to_date=None):
		        if to_date is None:
		            to_date = datetime.now().strftime('%Y-%m-%d')
		        self.cr.execute("SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)\
		                    FROM hr_payslip as hp, hr_payslip_line as pl \
		                    WHERE hp.employee_id = %s AND hp.state = 'done' \
		                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s",
		                    (self.employee_id, from_date, to_date, code))
		        res = self.cr.fetchone()
		        return res and res[0] or 0.0

		#we keep a dict with the result because a value can be overwritten by another rule with the same code
		result_dict = {}
		rules = {}
		categories_dict = {}
		blacklist = []
		payslip_obj = self.pool.get('hr.payslip')
		inputs_obj = self.pool.get('hr.payslip.worked_days')
		obj_rule = self.pool.get('hr.salary.rule')
		payslip = payslip_obj.browse(cr, uid, payslip_id, context=context)

		    
		# Memasukan data inputs ke dalam perhitungan slip gaji
		inputs = {}
		for input_line in payslip.input_line_ids:
		    inputs[input_line.code] = input_line
			
		
		# Memasukan data rate karyawan ke dalam perhitungan slip gaji
		# Masukan rate pada struktur dulu kemudian append/update dengan rate pada history
		rate_karyawan = {}
		
		if payslip.struct_id.rate_structure_ids:
			for rate_struktur in payslip.struct_id.rate_structure_ids:
				rate_karyawan[rate_struktur.jenis_rate_id.kode] = rate_struktur

		if payslip.contract_id.rate_karyawan_ids:		
			for rate_line in payslip.contract_id.rate_karyawan_ids:
				rate_karyawan[rate_line.jenis_rate_id.kode] = rate_line

		# Instanisasi object yang dapat digunakan sebagai formula dalam perhitungan gaji
		categories_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, categories_dict)
		input_obj = InputLine(self.pool, cr, uid, payslip.employee_id.id, inputs)		
		payslip_obj = Payslips(self.pool, cr, uid, payslip.employee_id.id, payslip)
		rules_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, rules)
		rate_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, rate_karyawan)
		
		localdict = {'categories': categories_obj, 'rules': rules_obj, 'payslip': payslip_obj,  'inputs': input_obj, 'rate' : rate_obj}

		structure_ids = self.pool.get('hr.contract').get_all_structures(cr, uid, contract_ids, context=context)


		rule_ids = self.list_jadwal_penggajian(cr, uid, payslip.id)
		#rule_ids += self.list_jamsostek_rule(cr, uid, payslip.id)

		
		# Membuat dict
		dict_rule_run = {}
		for b in rule_ids:
		    dict_rule_run[b[0]] = b[2]
		#raise osv.except_osv('a', dict_rule_run)    
		
		
		#run the rules by sequence
		sorted_rule_ids = [id for id, sequence, d in sorted(rule_ids, key=lambda x:x[1])]


		for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
		    employee = contract.employee_id
		    localdict.update({'employee': employee, 'contract': contract})
		    for rule in obj_rule.browse(cr, uid, sorted_rule_ids, context=context):
		        
		        key = rule.id
		        
		        localdict['result'] = None
		        localdict['result_qty'] = 1.0
		        #check if the rule can be applied
		        if obj_rule.satisfy_condition(cr, uid, rule.id, localdict, context=context) and rule.id not in blacklist:
		            #compute the amount of the rule
		            amount, qty, rate = obj_rule.compute_rule(cr, uid, rule.id, localdict, context=context)
		            #check if there is already a rule computed with that code
		            previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
		            #set/overwrite the amount computed for this rule in the localdict
		            tot_rule = amount * qty * rate / 100.0
		            localdict[rule.code] = tot_rule
		            rules[rule.code] = rule
		            #sum the amount for its salary category
		            localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
		            #create/overwrite the rule in the temporary results
		            result_dict[key] = {
		                'salary_rule_id': rule.id,
		                'contract_id': contract.id,
		                'name': rule.name,
		                'code': rule.code,
		                'category_id': rule.category_id.id,
		                'sequence': rule.sequence,
		                'appears_on_payslip': rule.appears_on_payslip,
		                'condition_select': rule.condition_select,
		                'condition_python': rule.condition_python,
		                'condition_range': rule.condition_range,
		                'condition_range_min': rule.condition_range_min,
		                'condition_range_max': rule.condition_range_max,
		                'amount_select': rule.amount_select,
		                'amount_fix': rule.amount_fix,
		                'amount_python_compute': rule.amount_python_compute,
		                'amount_percentage': rule.amount_percentage,
		                'amount_percentage_base': rule.amount_percentage_base,
		                'register_id': rule.register_id.id,
		                'amount': amount,
		                'employee_id': contract.employee_id.id,
		                'quantity': qty,
		                'rate': rate,
		                'eksekusi_penggajian_id' : dict_rule_run[key],
		            }
		        else:
		            #blacklist this rule and its children
		            blacklist += [id for id, seq in self.pool.get('hr.salary.rule')._recursive_search_of_rules(cr, uid, [rule], context=context)]

		result = [value for code, value in result_dict.items()]
		return result
		
	def hr_verify_sheet(self, cr, uid, ids, context=None):
		"""
		Overloading total
		"""
		for id in ids:
		    # Beri sequence
		    if not self.buat_sequence(cr, uid, id):
		        return False
		
		    self.write(cr, uid, ids, {'state': 'verify'}, context=context)
		    
		    if not self.ubah_status_eksekusi_penggajian(cr, uid, id):
		        return False
		        
		return True
		
	def ubah_status_eksekusi_penggajian(self, cr, uid, payslip_id):
		obj_payslip = self.pool.get('hr.payslip')
		obj_eksekusi_penggajian = self.pool.get('hr.eksekusi_penggajian')
		
		payslip = obj_payslip.browse(cr, uid, [payslip_id])[0]
		
		if not payslip.line_ids : return True
		
		for line in payslip.line_ids:
		    obj_eksekusi_penggajian.write(cr, uid, [line.eksekusi_penggajian_id.id], {'state' : 'run'})
		    
		return True     
		
	def action_cari_payslip_input(self, cr, uid, ids, context={}):
	
		for id in ids:
			self.cari_payslip_input(cr, uid, id)
			
		return True
		
	def cari_payslip_input(self, cr, uid, id):
		obj_payslip = self.pool.get('hr.payslip')
		obj_salary_rule = self.pool.get('hr.salary.rule')
		obj_payslip_input = self.pool.get('hr.payslip.input')
		
		
		payslip = obj_payslip.browse(cr, uid, [id])[0]
		
		rule_ids = self.list_jadwal_penggajian(cr, uid, payslip.id)
		
		sorted_rule_ids = [id for id, sequence, d in sorted(rule_ids, key=lambda x:x[1])]
		
		for rule in obj_salary_rule.browse(cr, uid, sorted_rule_ids):
			if rule.input_ids:
				for rule_input in rule.input_ids:
					kriteria = [('code','=',rule_input.code),('payslip_id','=',payslip.id)]
					cek_ids = obj_payslip_input.search(cr, uid, kriteria)
					
					if not cek_ids:
						res =	{
								'name' : rule_input.name,
								'payslip_id' : payslip.id,
								'sequence' : 1,
								'code' : rule_input.code,
								'amount' : 0.0,
								'contract_id' : payslip.contract_id.id,
								}
					
						input_id = obj_payslip_input.create(cr, uid, res)
		
		return True
		
	def buat_sequence(self, cr, uid, id):
		obj_sequence = self.pool.get('ir.sequence')
		obj_payslip = self.pool.get('hr.payslip')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		if not user.company_id.sequence_gaji_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk slip gaji belum diset')
			return False

		sequence_id = user.company_id.sequence_gaji_id.id		
		sequence = obj_sequence.next_by_id(cr, uid, sequence_id)
		
		obj_payslip.write(cr, uid, [id], {'name' : sequence})
		
		return True			
		
	   	
		
		
		
		

		
			


hr_payslip()




