##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from datetime import datetime

from osv import osv, fields
import netsvc
import pooler
from tools.translate import _
import decimal_precision as dp
from osv.orm import browse_record, browse_null

#define tipe field untuk di form dan list
class stock_move_pbos(osv.osv):
	_name = "stock.move.pbos"
	_description = "Telenais PBOS Form"
	_columns = {
		'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)]),
                'manufacturer_pname': fields.char('product.product', 'Material Name', required=True),
                'product_uom': fields.many2one('product.uom', 'Unit', required=True),
                'notes': fields.char('Notes', size=64),
                #'amount': fields.function('_amount_line', method=True, string='Amount'),
		'part_numb': fields.char('Part Number', size=64, required=True, select=True),
		'batch_size': fields.char('Batch Size', size=32, required=False, translate=False),
		'rendement_std': fields.float('Rendement std', digits=(16, 4), required=True),
		'due_date':fields.datetime('Order Date', help="Date of Order", select=True),
		'batch_no':fields.char('Batch No', size=32, required=False),
		'doc_number':fields.char('Document Number', size=32,required=True),	
        	'print_and_check': fields.char('Print and Check by', size=32, required=False, translate=False),
		'check_date':fields.datetime('Date', help="Date of Order", select=True),
		'state': fields.selection([
           		('draft', 'Draft'),
			('validated', 'Validated'),
			('produced', 'Produced'),
		        ('cancel', 'Cancelled')
            		], 'State', readonly=True, select=True),
	}

	_defaults = {
        	'state': 'draft',
   	}

#function button cancel
def action_cancel(self, cr, uid, ids, *args):
	if not len(ids):
		return False
	self.write(cr, uid, ids, {'state': 'cancel'})
	return True

#function button validate
def action_validate(self, cr, uid, ids, *args):
      	if not len(ids):
		return False
	self.write(cr, uid, ids, {'state': 'validated'})
       	return True

#function button delete
def unlink(self, cr, uid, ids, context=None):
       	if context is None:
		context = {}
       	for rec in self.browse(cr, uid, ids, context=context):
       	    if rec.state not in ['draft']:
                raise osv.except_osv(_('Invalid action !'), _('Only delete Draft PBOS'))	        
	return super(stock.move.pbos, self).unlink(cr, uid, ids, context=context)

stock_move_pbos()


#define field untuk di notebook (PBOS Line)
class stock_move_pbos_line(osv.osv):
	_name = "stock.move.pbos.line"
	_description = "ajsfnfksaj"

#function get harga product
def _amount_line(self, cr, uid, ids, prop, arg, context=None):
	res = {}
       	for line in self.browse(cr, uid, ids, context=context):
      	    res[line.id] = line.price_unit
       	return res

	_columns = {
		'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)]),
		'manufacturer_pname': fields.char('product.product', 'Material Name', required=True),
		'product_uom': fields.many2one('product.uom', 'Unit', required=True),
		#'amount': fields.function('_amount_line', method=True, string='Amount'),
}


def onchange_product(self, cr, uid, ids, product_id):
       	prod_obj = self.pool.get('product.product')
       	if product_id:
       	    product = prod_obj.read(cr, uid, product_id, ['name'], context=None)
       	return {'value': {'name': product['name']}}

stock_move_pbos_line()
