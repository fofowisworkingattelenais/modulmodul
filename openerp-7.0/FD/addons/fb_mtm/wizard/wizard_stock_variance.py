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
import netsvc
from tools.translate import _


class wizard_stock_variance(osv.osv_memory):
	_name = 'fb_mtm.stock_variance'
	_description = 'Wizard Stock Move Variance'


	_columns = 	{
				'date_from' : fields.date(string='Date From', required=True),
				'date_to' : fields.date(string='Date To', required=True),
				'variance': fields.float(string='Total Actual Cost', required=True),
				}

	def cetak_report(self, cr, uid, ids, data, context=None):
		data = self.read(cr, uid, ids, context=context)[0]
		datas = {
			'ids': [],
			'model': 'stock.move',
			'form': data
			}
		return {
			'type': 'ir.actions.report.xml',
			'report_name': 'fb_mtm.stock_variance',
			'datas': datas,
			}

wizard_stock_variance()


