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


class gaji_nonreguler(osv.osv):
	_name = 'hr.gaji_nonreguler'
	_description = 'Gaji Non Reguler'

	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def default_tanggal_penggajian(self, cr, uid, context={}):
		return date.today().strftime('%Y-%m-%d')

		
	def function_name(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_gaji_nonreguler = self.pool.get('hr.gaji_nonreguler')
		
		for gaji_nonreguler in obj_gaji_nonreguler.browse(cr, uid, ids):
			res[gaji_nonreguler.id] = '%s %s' % (str(gaji_nonreguler.tanggal_penggajian), gaji_nonreguler.salary_rule_id.name)
		return res	

		
		
	_columns = 	{
				'name' : fields.function(string='Jadwal Penggajian', fnct=function_name, type='char', size=255, method=True, store=False),
				'tanggal_penggajian' : fields.date(string='Tanggal Penggajian', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'salary_rule_id' : fields.many2one(obj='hr.salary.rule', string='Ketentuan Gaji', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'keterangan' : fields.text(string='Keterangan'),
				'detail_gaji_nonreguler_ids' : fields.one2many(obj='hr.detail_gaji_nonreguler', fields_id='gaji_nonreguler_id', strig='Detail Gaji Non-Reguler', readonly=True, states={'draft':[('readonly',False)]}),
				'jadwal_penggajian_id' : fields.many2one(obj='hr.jadwal_penggajian', string='Jadwal Penggajian', readonly=True),
				'state' : fields.selection([('draft','Draft'),('confirm', 'Confirm'),('batal', 'Batal')], 'Status', required=True, readonly=True),
				}
				
	_defaults =	{
				'state' : default_state,
				'tanggal_penggajian' : default_tanggal_penggajian,
				}
				
	def workflow_action_confirm(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.buat_jadwal_penggajian(cr, uid, id):
				return False
				
			if not self.buat_eksekusi_penggajian(cr, uid, id):
				return False
				
			self.write(cr, uid, [id], {'state':'confirm'})
				
		return True
		
	def workflow_action_batal(self, cr, uid, ids, context={}):
		for id in ids:
		
			if not self.boleh_dibatalkan(cr, uid, id):
				return False
				
			self.write(cr, uid, [id], {'state':'batal'})
				
		return True		
				
				
	def buat_jadwal_penggajian(self, cr, uid, id):
		"""
		Buat hr.jadwal_penggajian
		"""
		
		obj_gaji_nonreguler = self.pool.get('hr.gaji_nonreguler')
		obj_jadwal_penggajian = self.pool.get('hr.jadwal_penggajian')
		
		gaji_nonreguler = obj_gaji_nonreguler.browse(cr, uid, [id])[0]
		
		kriteria = [('tanggal_penggajian','=',gaji_nonreguler.tanggal_penggajian),('salary_rule_id','=',gaji_nonreguler.salary_rule_id.id)]
		cek_ids = obj_jadwal_penggajian.search(cr, uid, kriteria)
		
		if cek_ids : return True
		
		res = 	{
				'tanggal_penggajian' : gaji_nonreguler.tanggal_penggajian,
				'salary_rule_id' : gaji_nonreguler.salary_rule_id.id,
				}
				
		jadwal_penggajian_id = obj_jadwal_penggajian.create(cr, uid, res)
		
		obj_gaji_nonreguler.write(cr, uid, [id], {'jadwal_penggajian_id' : jadwal_penggajian_id})
		
		return True
		
	def buat_eksekusi_penggajian(self, cr, uid, id):
		"""
		Buar hr.eksekusi_penggajian
		"""
		obj_gaji_nonreguler = self.pool.get('hr.gaji_nonreguler')
		obj_eksekusi_penggajian = self.pool.get('hr.eksekusi_penggajian')
		obj_detail = self.pool.get('hr.detail_gaji_nonreguler')
		
		gaji_nonreguler = obj_gaji_nonreguler.browse(cr, uid, [id])[0]	
		
		
		
		
		
		if not gaji_nonreguler.detail_gaji_nonreguler_ids :	return True
		
		for detail in gaji_nonreguler.detail_gaji_nonreguler_ids:
			kriteria = [('jadwal_penggajian_id','=',gaji_nonreguler.jadwal_penggajian_id.id),('employee_id','=',detail.employee_id.id)]
			cari_ids = obj_eksekusi_penggajian.search(cr, uid, kriteria)
			
			if not cari_ids:
				res =	{
						'jadwal_penggajian_id' : gaji_nonreguler.jadwal_penggajian_id.id,
						'employee_id' : detail.employee_id.id
						}
					
				eksekusi_penggajian_id = obj_eksekusi_penggajian.create(cr, uid, res)
				
				obj_detail.write(cr, uid, [detail.id], {'eksekusi_penggajian_id' : eksekusi_penggajian_id})
			
		return True
		
		
	def cek_jadwal_penggajian(self, cr, uid, id):
		"""
		Cek jadwal penggajian
		
		Return : True jika sudah ada, False jika belum
		"""
		obj_gaji_nonreguler = self.pool.get('hr.gaji_nonreguler')
		
		gaji_nonreguler = obj_gaji_nonreguler.browse(cr, uid, [id])[0]	
		
		if gaji_nonreguler.jadwal_penggajian_id : return True
		
		return False
		
	def cek_eksekusi_penggajian(self, cr, uid, id):
		"""
		Cek eksekusi penggajian
		
		Return : True jika sudah ada, False jika belum
		"""
		obj_gaji_nonreguler = self.pool.get('hr.gaji_nonreguler')
		
		gaji_nonreguler = obj_gaji_nonreguler.browse(cr, uid, [id])[0]	
		
		if gaji_nonreguler.detail_gaji_nonreguler_ids : return False
		
		for detail in gaji_nonreguler.detail_gaji_nonreguler_ids:
			if detail.eksekusi_penggajian_id : return True
		
		return False
		
	def boleh_dibatalkan(self, cr, uid, id):
		"""
		Cek apakah data boleh dibatalkan
	
		return True jika boleh False jika tidak boleh
		"""
		if self.cek_jadwal_penggajian(cr, uid, id) : return False
		
		if self.cek_eksekusi_penggajian(cr, uid, id) : return False
		
		return True
				

		
		
		
	
		
	
		
		

				
		
		
				

				
gaji_nonreguler()


