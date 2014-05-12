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


class wizard_stok_total(osv.osv_memory):
	_name = 'titis.stok_total'
	_description = 'Wizard Stok Total'

		
	_columns = 	{
				'categ_id' : fields.many2one(obj='product.category', string='Product Category', required='True'),
				'close_date' : fields.date(string='Close Date', required='True'),
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
			'report_name': 'laporan_stok_total',
			'datas': datas,
			}
				
wizard_stok_total()


