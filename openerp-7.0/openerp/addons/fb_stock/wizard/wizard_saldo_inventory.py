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

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from osv import fields, osv
from osv.orm import browse_record, browse_null
from tools.translate import _


class wizard_saldo_inventory(osv.osv_memory):
	_name = 'fb_stock.wizard_saldo_inventory'
	_description = 'Wizard Saldo Inventory'

	_columns = {
		'location_id': fields.many2one(obj='stock.location', string='Location', required='True'),
		'date_from': fields.date(string='Date From', required=True),
		'date_to': fields.date(string='Date To', required=True)
	}

	def cetak_laporan(self, cr, uid, ids, context=None):
		datas = {}
		if context is None:
			context = {}

		data = self.read(cr, uid, ids, ['date_from','date_to','location_id'], context)[0]
		# data = self.read(cr, uid, ids, ['date_from', 'date_to'], context=context)[0]
		print data
		datas =	{
				'ids' : context.get('active_ids', []),
				'res_model' : 'product.product',
				'form' : data
				}

		return {
				'type' : 'ir.actions.report.xml',
				'report_name' : 'saldo_inventory',
				'datas' : datas
				}


wizard_saldo_inventory()