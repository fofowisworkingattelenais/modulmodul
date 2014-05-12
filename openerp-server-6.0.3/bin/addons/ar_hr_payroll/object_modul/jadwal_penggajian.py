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
from ar_base_waktu import date_tools as dt
from datetime import date


class jadwal_penggajian(osv.osv):
	_name = 'hr.jadwal_penggajian'
	_description = 'Jadwal Penggajian'
	_order = 'tanggal_penggajian, id'

	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def default_tanggal_penggajian(self, cr, uid, context={}):
		return date.today().strftime('%Y-%m-%d')

		
	def function_name(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_jadwal_penggajian = self.pool.get('hr.jadwal_penggajian')
		
		for jadwal_penggajian in obj_jadwal_penggajian.browse(cr, uid, ids):
			res[jadwal_penggajian.id] = '%s %s' % (str(jadwal_penggajian.tanggal_penggajian), jadwal_penggajian.salary_rule_id.name)
		return res	
		
	def function_tanggal_selanjutnya(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_jadwal_penggajian = self.pool.get('hr.jadwal_penggajian')
		for jadwal_penggajian in obj_jadwal_penggajian.browse(cr, uid, ids):
			if jadwal_penggajian.salary_rule_id:
				if jadwal_penggajian.salary_rule_id.jadwal_pembayaran == 'hari':
					res[jadwal_penggajian.id] = dt.cari_tanggal(jadwal_penggajian.tanggal_penggajian, 1)
				elif jadwal_penggajian.salary_rule_id.jadwal_pembayaran == 'minggu':
					res[jadwal_penggajian.id] = dt.cari_tanggal(jadwal_penggajian.tanggal_penggajian, 7)
				elif jadwal_penggajian.salary_rule_id.jadwal_pembayaran == 'bulan':
					res[jadwal_penggajian.id] = dt.cari_tanggal_selanjutnya(jadwal_penggajian.tanggal_penggajian, jadwal_penggajian.salary_rule_id.pilih_tanggal, 1)
				else:
					res[jadwal_penggajian.id] = False
				
			else:
				res[jadwal_penggajian.id] = False
		return res		
		
		
	_columns = 	{
				'name' : fields.function(string='Jadwal Penggajian', fnct=function_name, type='char', size=255, method=True, store=False),
				'tanggal_penggajian' : fields.date(string='Tanggal Penggajian', required=True),
				'tanggal_selanjutnya' : fields.function(fnct=function_tanggal_selanjutnya, string='Tanggal Selanjutnya', method=True, store=False, type='date'),
				'salary_rule_id' : fields.many2one(obj='hr.salary.rule', string='Ketentuan Penggajian', required=True),
				'state' : fields.selection([('draft','Draft'),('active', 'Active'),('missed', 'Missed'),('run','Run')], 'Status', required=True, readonly=True),
				}
				
	_defaults =	{
				'state' : default_state,
				'tanggal_penggajian' : default_tanggal_penggajian,
				}

		
	def buat_eksekusi_penggajian(self, cr, uid, jadwal_penggajian_id):
		obj_eksekusi_penggajian = self.pool.get('hr.eksekusi_penggajian')
		obj_jadwal_penggajian = self.pool.get('hr.jadwal_penggajian')
		obj_salary_rule = self.pool.get('hr.salary.rule')
	
		jadwal_penggajian = obj_jadwal_penggajian.browse(cr, uid, [jadwal_penggajian_id])[0]
		salary_rule_id = jadwal_penggajian.salary_rule_id.id
	
		employee_ids = obj_salary_rule.list_karyawan(cr, uid, salary_rule_id)
		
		# raise osv.except_osv('a', '%s' % (employee_ids))
	
	
		if not employee_ids : return True
	
		for employee_id in employee_ids:
			kriteria = [('employee_id','=',employee_id),('jadwal_penggajian_id','=',jadwal_penggajian_id)]
			eksekusi_penggajian_ids = obj_eksekusi_penggajian.search(cr, uid, kriteria)
		
			if not eksekusi_penggajian_ids:
		
	
				res =	{
						'employee_id' : employee_id,
						'jadwal_penggajian_id' : jadwal_penggajian_id,
						'payslip_line_id' : False,
						}
				
				obj_eksekusi_penggajian.create(cr, uid, res)
	
		return True
	
	def buat_jadwal_penggajian(self, cr, uid, jadwal_penggajian_id):
		obj_jadwal_penggajian = self.pool.get('hr.jadwal_penggajian')
	

	
		jadwal_penggajian = obj_jadwal_penggajian.browse(cr, uid, [jadwal_penggajian_id])[0]
	
		# cek dulu, jika sudah ada untuk run date selanjutnya maka tidak perlu dibuat
		kriteria = [('tanggal_penggajian','=',jadwal_penggajian.tanggal_selanjutnya),('salary_rule_id','=',jadwal_penggajian.salary_rule_id.id)]
		jadwal_penggajian_ids = obj_jadwal_penggajian.search(cr, uid, kriteria)
	
		
		if jadwal_penggajian_ids : return True	
		
		if jadwal_penggajian.salary_rule_id.jadwal_pembayaran == 'tidak_terjadwal' : return True	
		
		# raise osv.except_osv('a', '%s %s' % (jadwal_penggajian_ids, jadwal_penggajian.salary_rule_id.jadwal_pembayaran))
	
		res =	{
				'tanggal_penggajian' : jadwal_penggajian.tanggal_selanjutnya,
				'salary_rule_id' : jadwal_penggajian.salary_rule_id.id,
				}
			
		obj_jadwal_penggajian.create(cr, uid, res)
	
		return True
			
		
		
				
		
		
				

				
jadwal_penggajian()


