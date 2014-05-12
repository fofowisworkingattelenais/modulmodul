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

class hr_contract(osv.osv):
	_name = 'hr.contract'
	_inherit = 'hr.contract'

	_columns =	{
				'struct_id': fields.many2one('hr.payroll.structure', 'Salary Structure', readonly=True, states={'draft':[('readonly',False)]}),
				
				'schedule_pay': fields.selection([
				    ('monthly', 'Monthly'),
				    ('quarterly', 'Quarterly'),
				    ('semi-annually', 'Semi-annually'),
				    ('annually', 'Annually'),
				    ('weekly', 'Weekly'),
				    ('bi-weekly', 'Bi-weekly'),
				    ('bi-monthly', 'Bi-monthly'),
				    ], 'Scheduled Pay', select=True, readonly=True, states={'draft':[('readonly',False)]}),			
			    'rate_karyawan_ids' : fields.one2many(obj='hr.rate_karyawan', fields_id='contract_id', string='Rate Karyawan', readonly=True, states={'draft':[('readonly',False)]}),
				

				
				# Ketentuan penggajian
				'salary_rule_ids' : fields.many2many(obj='hr.salary.rule', rel='rel_contract_rule', id1='contract_id', id2='salaray_rule_id', string='Ketentuan Gaji', readonly=True, states={'draft':[('readonly',False)]}),
				'pendapatan_teratur_ids' : fields.many2many(obj='hr.salary.rule', rel='rel_contract_rule', id1='contract_id', id2='salaray_rule_id', string='Pendapatan Teratur', domain=[('category_id.parent_id.name','=','Pendapatan Teratur')]),
				'pendapatan_tidak_teratur_ids' : fields.many2many(obj='hr.salary.rule', rel='rel_contract_rule', id1='contract_id', id2='salaray_rule_id', string='Pendapatan Tidak Teratur', domain=[('category_id.parent_id.name','=','Pendapatan Tidak Teratur')]),

				# Potongan
				'potongan_ids' : fields.many2many(obj='hr.salary.rule', rel='rel_contract_rule', id1='contract_id', id2='salaray_rule_id', string='Potongan Beban Karyawan', domain=[('category_id.parent_id.name','=','Potongan'),('register_id','=',False)]),
				'potongan_kontribusi_ids' : fields.many2many(obj='hr.salary.rule', rel='rel_contract_rule', id1='contract_id', id2='salaray_rule_id', string='Potongan Kontribusi Perusahaan', domain=[('category_id.parent_id.name','=','Potongan'),('register_id','!=',False)]),

				'asuransi_ids' : fields.many2many(obj='hr.salary.rule', rel='rel_contract_rule', id1='contract_id', id2='salaray_rule_id', string='Asuransi Beban Karyawan', domain=[('category_id.parent_id.name','=','Asuransi'),('register_id','=',False)]),
				'asuransi_kontribusi_ids' : fields.many2many(obj='hr.salary.rule', rel='rel_contract_rule', id1='contract_id', id2='salaray_rule_id', string='Asuransi Kontribusi Perusahaan', domain=[('category_id.parent_id.name','=','Asuransi'),('register_id','!=',False)]),

				# Asuransi
				'pensiun_ids' : fields.many2many(obj='hr.salary.rule', rel='rel_contract_rule', id1='contract_id', id2='salaray_rule_id', string='Pensiun Beban Karyawan', domain=[('category_id.parent_id.name','=','Pensiun'),('register_id','=',False)]),
				'pensiun_kontribusi_ids' : fields.many2many(obj='hr.salary.rule', rel='rel_contract_rule', id1='contract_id', id2='salaray_rule_id', string='Pensiun Kontribusi Perusahaan', domain=[('category_id.parent_id.name','=','Pensiun'),('register_id','!=',False)]),
				
				# Jamsostek
				'jamsostek_ids' : fields.many2many('hr.salary.rule', 'rel_contract_jamsostek', 'contract_id', 'salaray_rule_id', 'Ketentuan Perhitungan Jamsostek', readonly=True, states={'draft':[('readonly',False)]}),		    
				}


	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_contract, self).create(cr, uid, values, context)
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
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_contract, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			
			

		
			

hr_contract()




