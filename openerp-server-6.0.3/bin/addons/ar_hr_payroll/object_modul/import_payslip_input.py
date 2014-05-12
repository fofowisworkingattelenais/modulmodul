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


class import_payslip_input(osv.osv):
	_name = 'hr.import_payslip_input'
	_description = 'Import Payslip Input'
	
	def default_name(self, cr, uid, context={}):
		return '/'
		
	def default_state(self, cr, uid, context={}):
		return 'draft'

		
	_columns = 	{
				'name' : fields.char(string='# Import', size=30, required=True, readonly=True),
				'run_id' : fields.many2one(obj='hr.payslip.run', string='# Batch', required=True),
				'keterangan' : fields.text(string='Keterangan'),
				'import_detail_payslip_input_ids' : fields.one2many(obj='hr.import_detail_payslip_input', fields_id='import_payslip_input_id', string='# Import'),
				'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'),('batal','Batal')], string='Status', readonly=True),
				}
				
	_defaults =	{
				'name' : default_name,
				'state' : default_state,
				}
				
	def buat_payslip_input(self, cr, uid, id):
		obj_import_payslip_input = self.pool.get('hr.import_payslip_input')
		obj_payslip_input = self.pool.get('hr.payslip.input')
		
		import_payslip_input = obj_import_payslip_input.browse(cr, uid, [id])[0]
		
		if not import_payslip_input.import_detail_payslip_input_ids: return True
		
		
		
		for detail in import_payslip_input.import_detail_payslip_input_ids:
			kriteria1 = [('payslip_id.payslip_run_id','=',import_payslip_input.run_id.id),('payslip_id.employee_id','=',detail.employee_id.id),('code','=',detail.kode)]
			input_ids = obj_payslip_input.search(cr, uid, kriteria1)
			
			if input_ids:
				input_id = input_ids[0]
				res =	{
						'amount' : detail.jumlah,
						}
						
				obj_payslip_input.write(cr, uid, [input_id], res)
				
		return True
		
	def workflow_action_confirm(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.buat_payslip_input(cr, uid, id):
				return False
		
			self.write(cr, uid, [id], {'state':'confirm'})
		return True		
			

import_payslip_input()
