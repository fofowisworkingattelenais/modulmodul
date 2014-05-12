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

class hr_payslip_run(osv.osv):
	_name = 'hr.payslip.run'
	_inherit = 'hr.payslip.run'

	def default_name(self, cr, uid, context={}):
		return '/'
		
	def default_date_start(self, cr, uid, context={}):
		return False
		
	def default_date_end(self, cr, uid, context={}):
		return False		
		
	def function_date_start(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_payslip_run = self.pool.get('hr.payslip.run')
		
		for payslip_run in obj_payslip_run.browse(cr, uid, ids):
			if not payslip_run.detail_periode_gaji_id:
				res[payslip_run.id] = False
			else:
				res[payslip_run.id] = payslip_run.detail_periode_gaji_id.tanggal_mulai
				
		return res
		
	def function_date_end(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_payslip_run = self.pool.get('hr.payslip.run')
		
		for payslip_run in obj_payslip_run.browse(cr, uid, ids):
			if not payslip_run.detail_periode_gaji_id:
				res[payslip_run.id] = False
			else:
				res[payslip_run.id] = payslip_run.detail_periode_gaji_id.tanggal_akhir
				
		return res				

	_columns =	{
				'name': fields.char('Name', size=64, required=True, readonly=True),
				'date_start' : fields.function(function_date_start, string='Tanggal Mulai', type='date'),
				'date_end' : fields.function(function_date_end, string='Tanggal Akhir', type='date'),				
				'detail_periode_gaji_id' : fields.many2one('hr.detail_periode_gaji', 'Periode Gaji', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'tanggal_slip' : fields.date(string='Tanggal Slip', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				}
				
	_defaults =	{
				'name' : default_name,
				'date_start' : default_date_start,
				'date_end' : default_date_end,
				}


	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_payslip_run, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_payslip_run, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_payslip_run, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			
	def validasi_payslip(self, cr, uid, payslip_run_id):
		obj_payslip_run = self.pool.get('hr.payslip.run')
		
		payslip_run = obj_payslip_run.browse(cr, uid, [payslip_run_id])[0]
		
		if not payslip_run.slip_ids : return True
		
		for slip in payslip_run.slip_ids:
		    wf_service = netsvc.LocalService('workflow')
		    wf_service.trg_validate(uid, 'hr.payslip', slip.id, 'hr_verify_sheet', cr)
		    
		return True
		
	def action_buat_payslip(self, cr, uid, ids, context={}):
		obj_payslip_run = self.pool.get('hr.payslip.run')
		obj_eksekusi_penggajian = self.pool.get('hr.eksekusi_penggajian')
		obj_payslip = self.pool.get('hr.payslip')
	
		for id in ids:
			payslip_run = obj_payslip_run.browse(cr, uid, [id])[0]
			list_employee = []
			
			kriteria = [('jadwal_penggajian_id.tanggal_penggajian','=',payslip_run.tanggal_slip),('state','=','draft')]
			eksekusi_penggajian_ids = obj_eksekusi_penggajian.search(cr, uid, kriteria)
			
			
			if not eksekusi_penggajian_ids : return True
			
			for eksekusi_penggajian in obj_eksekusi_penggajian.browse(cr, uid, eksekusi_penggajian_ids):
			    if eksekusi_penggajian.employee_id.id not in list_employee : list_employee.append(eksekusi_penggajian.employee_id.id)
			    
			
			for employee_id in list_employee:
			
			    # Cek payslip
			    kriteria = [('payslip_run_id','=',payslip_run.id),('employee_id','=',employee_id)]
			    payslip_ids = obj_payslip.search(cr, uid, kriteria)
			    
			    if not payslip_ids:
			
			        res =   {
			                'employee_id' : employee_id,
			                'tanggal_slip' : payslip_run.tanggal_slip,
			                'payslip_run_id' : payslip_run.id,
			                'detail_periode_gaji_id' : payslip_run.detail_periode_gaji_id.id,
			                }
			                
			        #raise osv.except_osv('a', res) 
			                
			        payslip_id = obj_payslip.create(cr, uid, res)
			        obj_payslip.action_cari_payslip_input(cr, uid, [payslip_id])
			        obj_payslip.compute_sheet(cr, uid, [payslip_id])
			    
			    #raise osv.except_osv('a', payslip_id) 
			            
			    
			    
		return True				

		
		
	def onchange_detail_periode_gaji_id(self, cr, uid, ids, detail_periode_gaji_id):
		value = {}
		obj_detail_periode_gaji = self.pool.get('hr.detail_periode_gaji')
		
		if detail_periode_gaji_id:
			detail_periode_gaji = obj_detail_periode_gaji.browse(cr, uid, [detail_periode_gaji_id])[0]
			
			value.update({'date_from' : detail_periode_gaji.tanggal_mulai, 'date_from' : detail_periode_gaji.tanggal_akhir })
			
		return {'value' : value}
		
	def buat_sequence(self, cr, uid, payslip_run_id):
		obj_sequence = self.pool.get('ir.sequence')
		obj_payslip_run = self.pool.get('hr.payslip.run')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		if not user.company_id.sequence_batch_gaji_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk payslip batch belum diset')
			return False

		sequence_id = user.company_id.sequence_batch_gaji_id.id		
		sequence = obj_sequence.next_by_id(cr, uid, sequence_id)
		
		obj_payslip_run.write(cr, uid, [payslip_run_id], {'name' : sequence})
		
		return True

	def close_payslip_run(self, cr, uid, ids, context=None):
		for id in ids:
		    if not self.buat_sequence(cr, uid, id):
		        return False
		
		
		    if not self.validasi_payslip(cr, uid, id):
		        return False
		        
		    self.write(cr, uid, [id], {'state': 'close'}, context=context) 
		    
		return True 		
		
	
			

hr_payslip_run()




