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
from datetime import date
import decimal_precision as dp
from tools.safe_eval import safe_eval as eval


class ketentuan_cuti(osv.osv):
	_name = 'hr.ketentuan_cuti'
	_description = 'Ketentuan Absensi'

	def default_tahun(self, cr, uid, context={}):
		return date.today().year
		
	def default_state(self, cr, uid, context={}):
		return 'draft'

	_columns = 	{
				'employee_id' : fields.many2one(obj='hr.employee', string='Karyawan', required=True, domain=['|','|',('status_karyawan','=','tetap'),('status_karyawan','=','kontrak'),('status_karyawan','=','probation')], readonly=True, states={'draft':[('readonly',False)]}),
				'tahun' : fields.integer(string='Tahun', required=True, readonly=True, states={'draft':[('readonly',False)]}),
				'detail_ketentuan_cuti_ids' : fields.one2many(obj='hr.detail_ketentuan_cuti', fields_id='ketentuan_cuti_id', string='Detail Ketentuan Cuti', readonly=True, states={'draft':[('readonly',False)]}),
				'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'),('batal','Batal')], string='Status', readonly=True),
				}
				
	_defaults =	{
				'tahun' : default_tahun,
				'state' : default_state,
				}
				
	_sql_constraints =	[
											('identifier_ketentuan_cuti', 'unique(employee_id,tahun)', 'Seorang karyawan tidak boleh memiliki lebih dari satu ketentuan cuti tiap tahunnya !'),
											]
				
	def workflow_action_confirm(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, ids, {'state' : 'confirm'})
			
		return True
		
	def workflow_action_batal(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, ids, {'state' : 'batal'})
		return True
		
	def button_set_draft(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, ids, {'state' : 'draft'})
		return True
				

ketentuan_cuti()


