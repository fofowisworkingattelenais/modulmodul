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

class stock_picking(osv.osv):
	_name = 'stock.picking'
	_inherit = 'stock.picking'
						

	def _get_discount_invoice(self, cursor, user, move_line):
		if move_line.purchase_line_id:
			if move_line.purchase_line_id.order_id.discount_type == 'total':
				discount = move_line.purchase_line_id.order_id.total_discount
			elif move_line.purchase_line_id.order_id.discount_type == 'line':
				discount = move_line.purchase_line_id.discount

			return discount
		return super(stock_picking, self)._get_discount_invoice(cursor, user, move_line)
							
stock_picking()							
							






