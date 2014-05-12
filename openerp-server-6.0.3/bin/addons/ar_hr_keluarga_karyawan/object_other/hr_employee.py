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
	
	def function_jumlah_anak(self, cr, uid, ids, field_name, arg, context):
		res = {}
		obj_karyawan = self.pool.get('hr.employee')
		
		for karyawan in obj_karyawan.browse(cr, uid, ids):
			res[karyawan.id] = len(karyawan.anak_ids)
			
		return res	
	
	_columns =	{
				'nama_pasangan' : fields.char('Nama Pasangan', size=100),
				'tanggal_menikah' : fields.date('Tanggal Menikah'),
				'nama_ayah' : fields.char('Nama Ayah', size=100),
				'nama_ibu' : fields.char('Nama Ibu', size=100),
				'anak_ids' : fields.one2many('hr.anak_karyawan', 'employee_id', 'Anak'),
				'jumlah_anak' : fields.function(function_jumlah_anak, method=True, type='integer', string='Jumlah Anak'),
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




