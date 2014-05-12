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
from datetime import datetime
import decimal_precision as dp

class purchase_order_line(osv.osv):
	_name = 'purchase.order.line'
	_inherit = 'purchase.order.line'

	def _amount_line(self, cr, uid, ids, prop, arg, context=None):
		"""
		Override method _amount_line agar memperhitungkan discount

		"""

		res = {}
		obj_currency = self.pool.get('res.currency')
		obj_tax = self.pool.get('account.tax')

		for line in self.browse(cr, uid, ids, context=context):
			# MENENTUKAN DISCOUNT TOTAL/LINE
			if line.order_id.discount_type == 'total':
				discount = line.order_id.total_discount
			elif line.order_id.discount_type == 'line':
				discount = line.discount
		
			price = line.price_unit * (1 - (discount or 0.0) / 100.0)
			taxes = obj_tax.compute_all(cr, uid, line.taxes_id, price, line.product_qty)
			cur = line.order_id.pricelist_id.currency_id
			res[line.id] = obj_currency.round(cr, uid, cur, taxes['total'])
			
		return res	
	
	_columns = {
                			'discount' : fields.float(string='Discount (%)', digits=(16,2)),
                			'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal', digits_compute= dp.get_precision('Purchase Price')),
                			}

							
purchase_order_line()							
							






