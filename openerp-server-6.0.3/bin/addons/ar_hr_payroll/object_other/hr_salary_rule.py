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
from datetime import time, date
from ar_base_waktu import date_tools as dt

class hr_salary_rule(osv.osv):
	_name = 'hr.salary.rule'
	_inherit = 'hr.salary.rule'
	
	def default_jadwal_pembayaran(self, cr, uid, context={}):
		return'tidak_terjadwal'
		
	def default_tanggal_mulai_berlaku(self, cr, uid, context={}):
		return date.today().strftime('%Y-%m-%d')

	_columns =	{
				'jadwal_pembayaran' : fields.selection(selection=[('hari','Harian'),('minggu','Mingguan'),('bulan','Bulanan'),('tidak_terjadwal','Tidak Terjadwal')], string='Jadwal Pembayaran', required=True),
				'pilih_hari' : fields.many2one(obj='base.hari', string='Hari'),
				'pilih_tanggal' : fields.integer(string='Tanggal'),
				'tanggal_mulai_berlaku' : fields.date(string='Tanggal Mulai Berlaku'),
				'jadwal_penggajian_ids' : fields.one2many(obj='hr.jadwal_penggajian', fields_id='salary_rule_id', string='Jadwal Penggajian'),
				}
				
	_defaults =	{
				'jadwal_pembayaran' : default_jadwal_pembayaran,
				'tanggal_mulai_berlaku' : default_tanggal_mulai_berlaku,
				}

	def buat_jadwal_penggajian(self, cr, uid, salary_rule_id):
		obj_salary_rule = self.pool.get('hr.salary.rule')
		obj_jadwal_penggajian = self.pool.get('hr.jadwal_penggajian')
		
		salary_rule = obj_salary_rule.browse(cr, uid, [salary_rule_id])[0]

		dt_tanggal = dt.string2date(salary_rule.tanggal_mulai_berlaku)
		
		if salary_rule.jadwal_pembayaran == 'hari':
		    str_tanggal = self.jadwal_pembayaran_harian(cr, uid, salary_rule_id, dt_tanggal)
		elif salary_rule.jadwal_pembayaran == 'minggu':
		    str_tanggal = self.jadwal_pembayaran_mingguan(cr, uid, salary_rule_id, dt_tanggal)
		elif salary_rule.jadwal_pembayaran == 'bulan':
		    str_tanggal = self.jadwal_pembayaran_bulanan(cr, uid, salary_rule_id, dt_tanggal)
		    
		if salary_rule.jadwal_pembayaran != 'tidak_terjadwal':
		
			res =   {
					'tanggal_penggajian' : str_tanggal,
					'salary_rule_id' : salary_rule_id,
					}
				
			obj_jadwal_penggajian.create(cr, uid, res)
	
		return True


	def jadwal_pembayaran_harian(self, cr, uid, salary_rule_id, dt_tanggal):
		return dt_tanggal
		
	def jadwal_pembayaran_mingguan(self, cr, uid, salary_rule_id, dt_tanggal):
		obj_salary_rule = self.pool.get('hr.salary.rule')
		
		salary_rule = obj_salary_rule.browse(cr, uid, [salary_rule_id])[0]
		
		int_dayweek = dt_tanggal.isoweekday()
		
		if salary_rule.pilih_hari.urutan >= int_dayweek:
		    a = dt_tanggal.toordinal() + salary_rule.pilih_hari.urutan - int_dayweek
		else:
		    a = dt_tanggal.toordinal() + (7 - int_dayweek) + salary_rule.pilih_hari.urutan
		              
		return date.fromordinal(a).strftime('%Y-%m-%d') 
		
	def jadwal_pembayaran_bulanan(self, cr, uid, salary_rule_id, dt_tanggal):
		#TODO: Berantakan tapi berfungsi
		
		obj_salary_rule = self.pool.get('hr.salary.rule')
		
		salary_rule = obj_salary_rule.browse(cr, uid, [salary_rule_id])[0]        
		#raise osv.except_osv('a', str(dt_tanggal))
		a = dt_tanggal.day
		#raise osv.except_osv('a', a)
		b = dt_tanggal.toordinal()
		
		if a < salary_rule.pilih_tanggal:
		    d = date.fromordinal(b)
		    c = dt.cari_tanggal_selanjutnya(d.strftime('%Y-%m-%d'), salary_rule.pilih_tanggal, 0)
		    return c
		else:
		   # raise osv.except_osv('a', 2)
		    d = b + (salary_rule.pilih_tanggal - a)
		    e = date.fromordinal(d)
		    f = dt.cari_tanggal_selanjutnya(e.strftime('%Y-%m-%d'), salary_rule.pilih_tanggal, 1)
		    return f       
		    
		    
	def list_karyawan(self, cr, uid, rule_id):
		'''
		Method untuk mencari id karyawan yang memiliki ketentuan penggajian dengan id = rule_id
		'''
		obj_employee = self.pool.get('hr.employee')
		hasil = []
		
		# List semua id employee
		#TODO : kriteria harusnya hanya employee yang aktif
		kriteria_employee = ['|','|',('state','=','probation'),('state','=','kontrak'),('state','=','tetap')]
		employee_ids = obj_employee.search(cr, uid, kriteria_employee)
		
		if not employee_ids : return hasil
		
		for employee in obj_employee.browse(cr, uid , employee_ids):
		    if employee.ketentuan_gaji_ids:
		        for salary_rule in employee.ketentuan_gaji_ids:
		            if salary_rule.id == rule_id : hasil.append(employee.id)
		            
		    if employee.ketentuan_gaji_tambahan_ids:
		        for salary_rule in employee.ketentuan_gaji_tambahan_ids:
		            if salary_rule.id == rule_id : hasil.append(employee.id)
		            
		return hasil   		            
        
        
	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			salary_rule_id = super(hr_salary_rule, self).create(cr, uid, values, context)
			
			buat_jadwal = context.get('buat_jadwal', False)
			
			if buat_jadwal : self.buat_jadwal_penggajian(cr, uid, salary_rule_id)
			
			return salary_rule_id
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return  super(hr_salary_rule, self).copy(cr, uid, id, default, context)
			
			
			
			
			
			
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_salary_rule, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')

hr_salary_rule()




