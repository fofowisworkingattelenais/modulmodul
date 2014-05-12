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
import time
import netsvc
from mx import DateTime
from tools import config
from tools.translate import _

class sale_order(osv.osv):

	_name = 'sale.order'
	_inherit = 'sale.order'
	
	def get_price_unit(self, cr, uid, ids, context=None):
		return True
	
	_columns = 	{
					'state': fields.selection([
						('draft', 'Quotation'),
						('waiting_date', 'Waiting Schedule'),
						('validate', 'Validate'),
						('manual', 'Manual In Progress'),
						('progress', 'In Progress'),
						('shipping_except', 'Shipping Exception'),
						('invoice_except', 'Invoice Exception'),
						('done', 'Done'),
						('cancel', 'Cancelled')
						], 'Order State', readonly=True, help="Gives the state of the quotation or sales order. \nThe exception state is automatically set when a cancel operation occurs in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception). \nThe 'Waiting Schedule' state is set when the invoice is confirmed but waiting for the scheduler to run on the date 'Ordered Date'.", select=True)
				}
		
	def action_validate(self, cr, uid, ids, *args):	
		for id in ids:		
			self.write(cr, uid, [id], {'state' : 'validate'})
		return True

sale_order()




