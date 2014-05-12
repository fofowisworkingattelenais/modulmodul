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

import wizard
from osv import fields, osv
from datetime import date
import netsvc
from tools.translate import _


class wizard_report_actual_vs_budget(osv.osv_memory):
	_name = 'titis.wizard_report_actual_vs_budget'
	_description = 'Wizard Report Actual Vs Budget'

		
	_columns = 	{
				'fiscal_year_id' : fields.many2one(obj='account.fiscalyear', string='Fiscal Years', required='True'),
				'period_id' : fields.many2one(obj='account.period', string='Period', required='True'),
				'analytic_account_id' : fields.many2one(obj='account.analytic.account', string='Analytic Account', required='True'),
				}

	def print_report(self, cr, uid, ids, data, context=None):
		data = self.read(cr, uid, ids, context=context)[0]
		datas = {
			'ids': [],
			'model': 'crossovered.budget',
			'form': data
                 }
		return {
			'type': 'ir.actions.report.xml',
			'report_name': 'laporan_actual_vs_budget',
			'datas': datas,
			}
				
wizard_report_actual_vs_budget()


