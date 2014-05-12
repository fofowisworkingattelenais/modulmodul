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

class hr_payroll_structure(osv.osv):
	_name = 'hr.payroll.structure'
	_inherit = 'hr.payroll.structure'
	_columns = 	{
				'rate_structure_ids' : fields.one2many(obj='hr.rate_structure', fields_id='structure_id', string='Rate Per Struktur'),
				'pendapatan_teratur_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_salary_rule_rel', id1='struct_id', id2='rule_id', string='Pendapatan Teratur', domain=[('category_id.parent_id.name','=','Pendapatan Teratur')]),
				'pendapatan_tidak_teratur_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_salary_rule_rel', id1='struct_id', id2='rule_id', string='Pendapatan Tidak Teratur', domain=[('category_id.parent_id.name','=','Pendapatan Tidak Teratur')]),
				'potongan_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_salary_rule_rel', id1='struct_id', id2='rule_id', string='Potongan', domain=[('category_id.parent_id.name','=','Potongan'),('register_id','=',False)]),
				'potongan_kontribusi_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_salary_rule_rel', id1='struct_id', id2='rule_id', string='Potongan', domain=[('category_id.parent_id.name','=','Potongan'),('register_id','!=',False)]),
				'asuransi_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_salary_rule_rel', id1='struct_id', id2='rule_id', string='Asuransi', domain=[('category_id.parent_id.name','=','Asuransi'),('register_id','=',False)]),
				'asuransi_kontribusi_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_salary_rule_rel', id1='struct_id', id2='rule_id', string='Asuransi', domain=[('category_id.parent_id.name','=','Asuransi'),('register_id','!=',False)]),
				'pensiun_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_salary_rule_rel', id1='struct_id', id2='rule_id', string='Iuran Pensiun', domain=[('category_id.parent_id.name','=','Pensiun'),('register_id','=',False)]),
				'pensiun_kontribusi_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_salary_rule_rel', id1='struct_id', id2='rule_id', string='Iuran Pensiun', domain=[('category_id.parent_id.name','=','Pensiun'),('register_id','!=',False)]),
				'jamsostek_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_jamsostek_rel', id1='struct_id', id2='rule_id', string='Komponen Jamsostek', domain=['|',('category_id.parent_id.name','=','Pendapatan Teratur'),('category_id.parent_id.name','=','Pendapatan Tidak Teratur')]),
				}
hr_payroll_structure()




