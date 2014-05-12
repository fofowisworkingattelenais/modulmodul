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
from dateutil.relativedelta import relativedelta

from osv import osv, fields
import netsvc
import pooler
from tools.translate import _
import decimal_precision as dp
from osv.orm import browse_record, browse_null

class smcus_pymad(osv.osv):
    _name = "smcus.pymad"
    _description = "Telenais PyMAD Form"

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('smcus.pymad.line').browse(cr, uid, ids, context=context):
            result[line.pymad_id.id] = True
        return result.keys()

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        val1=0
        for advance in self.browse(cr, uid, ids, context=context):
            res[advance.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'amount_ca': 0.0,
            }
            for line in advance.pymad_line:
               val1 += line.price_subtotal
            res[advance.id]['amount_untaxed']= val1
            res[advance.id]['amount_tax']= val1
            res[advance.id]['amount_total']= val1
            res[advance.id]['amount_ca']= val1*0.5
        return res

    _columns = {
        'name': fields.char('Reference', size=64, required=True,
            readonly=True, states={'draft': [('readonly', False)]}, select=True),
        'partner_id': fields.many2one('res.partner', 'Customer', readonly=True, 
            domain=[('customer', '=', True)], required=True, change_default=True, select=True, states={'draft': [('readonly', False)]},),
        'origin': fields.char('Origin', size=100, readonly=True, states={'draft': [('readonly', False)]},),
        'order_id': fields.many2one('sale.order', 'SO No', select=True, readonly=True, states={'draft': [('readonly', False)]}, required=True,),
        'date_pymad': fields.date('Date PyMAD', required=True, select=True, readonly=True, states={'draft': [('readonly', False)]},),
        'date_order': fields.related('order_id', 'date_order', type='date', store=True, string='Date SO', readonly=True),       
        'user_id': fields.many2one('res.users', 'PIC/Sales', readonly=True, states={'draft': [('readonly', False)]}, select=True, required=True,),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('validated', 'Validated'),
            ('invoiced', 'Invoiced'),
            ('cancel', 'Cancelled')
            ], 'State', readonly=True, select=True),
        'pymad_line': fields.one2many('smcus.pymad.line', 'pymad_id', 'PYMAD Lines', readonly=True,states={'draft': [('readonly', False)]},),
        'amount_untaxed': fields.float('Untaxed Total', required=True, digits_compute= dp.get_precision('Sale Price'), readonly=True),
        'amount_tax': fields.float('Taxes', required=True, digits_compute= dp.get_precision('Sale Price'), readonly=True),
        'amount_total': fields.float('Total', required=True, digits_compute= dp.get_precision('Sale Price'), readonly=True),
        'notes': fields.text('Notes'),
    }
    
    _defaults = {
        'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'smcus.pymad'),
        'state': 'draft',
        'date_pymad': lambda *a: time.strftime('%Y-%m-%d'),
        'user_id': lambda obj, cr, uid, context: uid,
        'amount_tax': 0.0,
        'amount_untaxed': 0.0,
        'amount_total': 0.0,
    }

    def action_draft(self, cr, uid, ids, *args):
        if not len(ids):
            return False
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def action_cancel(self, cr, uid, ids, *args):
        if not len(ids):
            return False
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def action_validate(self, cr, uid, ids, *args):
        if not len(ids):
            return False
        self.write(cr, uid, ids, {'state': 'validated'})
        return True

smcus_pymad()

class smcus_pymad_line(osv.osv):
    _name = "smcus.pymad.line"
    _description = "Telenais PyMAD Line"

    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.price_unit * line.product_qty
        return res

    _columns = {
        'pymad_id': fields.many2one('smcus.pymad', 'PYMAD', select=True, required=True, ondelete='cascade'),
        'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)]),
        'name': fields.char('Job Index', size=256, required=True),
        'address_allotment_id': fields.many2one('res.partner.address', 'Expatriate'),
        'customer_id': fields.many2one('res.partner', 'Customer', select=True, domain=[('customer', '=', True)]),
        'product_qty': fields.float('Quantity', required=True, digits=(16,2)),
        'product_uom': fields.many2one('product.uom', 'Product UOM', required=True),
        'price_unit': fields.float('Unit Price', required=True, digits_compute= dp.get_precision('Sale Price')),
        'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal', digits_compute= dp.get_precision('Sale Price')),
        'tax_id': fields.many2many('account.tax', 'smcus_pymad_tax', 'pymad_line_id', 'tax_id', 'Taxes'),
    }
    
    def onchange_product(self, cr, uid, ids, product_id):
        prod_obj = self.pool.get('product.product')
        if product_id:
            product = prod_obj.read(cr, uid, product_id, ['name'], context=None)
            return {'value': {'name': product['name']}}

smcus_pymad_line()
