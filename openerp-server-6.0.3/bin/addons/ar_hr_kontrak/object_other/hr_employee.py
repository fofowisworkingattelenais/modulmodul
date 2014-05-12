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

	def function_contract_id(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		obj_kontrak = self.pool.get('hr.contract')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			kontrak_id = False
			
			kontrak_ids = obj_kontrak.search(cr, uid, [('employee_id','=',karyawan.id),('state','=','valid')])
			if kontrak_ids : kontrak_id = kontrak_ids[0]
			
			res[karyawan.id] = kontrak_id
			
		return res
		
	def function_company_id(self, cr, uid, ids, field_name, args, context=None):
		res = {}

		obj_karyawan = self.pool.get('hr.employee')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			if not karyawan.contract_id : return False
			
			res[karyawan.id] = False
			
		return res
		
	def function_department_id(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			if not karyawan.contract_id : return False
			
			res[karyawan.id] = False #karyawan.contract_id.department_id.id
			
		return res		
		
	def function_job_id(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			if not karyawan.contract_id : return False
			
			res[karyawan.id] = False #karyawan.contract_id.job_id.id
			
		return res		

		
	
	_columns =	{
				'contract_id':fields.function(function_contract_id, string='Kontrak Aktif', type='many2one', relation='hr.contract', method=True, store=False),
				'tanggal_bergabung' : fields.date('Tanggal Bergabung'),
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
			

hr_employee()




