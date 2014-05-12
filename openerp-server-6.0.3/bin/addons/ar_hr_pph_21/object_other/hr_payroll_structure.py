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
				'perhitungan_pph_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_pph_rel', id1='struct_id', id2='rule_id', string='Perhitungan PPH 21'),		
				'perhitungan_pph_non_gross_up_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_pph_rel', id1='struct_id', id2='rule_id', string='Perhitungan PPH 21 Non Gross-Up', domain=[('category_id.parent_id.name','=','Perhitungan PPH 21')]),
				'perhitungan_pph_gross_up_ids':fields.many2many(obj='hr.salary.rule', rel='hr_structure_pph_rel', id1='struct_id', id2='rule_id', string='Perhitungan PPH 21 Gross-Up', domain=[('category_id.parent_id.name','=','Perhitungan PPH 21 Gross-Up')]),
				}
hr_payroll_structure()




