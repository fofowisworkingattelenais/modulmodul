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

class smcus_cash_advance(osv.osv):
    _name = "smcus.cash.advance"
    _description = "Telenais Cash Advance Form"

    _columns = {
        'name': fields.char('Reference', size=64, required=True,
            readonly=True, states={'draft': [('readonly', False)]}, select=True),
        'partner_id': fields.many2one('res.partner', 'Supplier', readonly=True, domain=[('supplier', '=', True)], required=True, change_default=True, select=True),
        'purchase_id': fields.many2one('purchase.order', 'PO No', select=True, readonly=True, required=True,),
        'date_ca': fields.date('Date CA', required=True, select=True, readonly=True, states={'draft': [('readonly', False)]},),
        'date_po': fields.related('purchase_id', 'date_order', type='date', store=True, string='Date PO', readonly=True),       
        'user_id': fields.many2one('res.users', 'PIC/Sales', readonly=True, states={'draft': [('readonly', False)]}, select=True, required=True,),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('validated', 'Validated'),
            ('cancel', 'Cancelled')
            ], 'State', readonly=True, select=True),
        'cash_advance_line': fields.one2many('smcus.cash.advance.line', 'cash_advance_id', 'Cash Advance Lines', readonly=True),
        'amount_untaxed': fields.float('Untaxed Total PO', required=True, digits_compute= dp.get_precision('Purchase Price'), readonly=True),
        'amount_tax': fields.float('Taxes PO', required=True, digits_compute= dp.get_precision('Purchase Price'), readonly=True),
        'amount_total': fields.float('Total PO', required=True, digits_compute= dp.get_precision('Purchase Price'), readonly=True),
        'amount_ca': fields.float('Total Cash Advance', required=True, digits_compute= dp.get_precision('Purchase Price'), readonly=True, states={'draft': [('readonly', False)]},
            help="The total cash advance amount. By default 50%"),
        'notes': fields.text('Notes'),
    }
    
    _defaults = {
        'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'smcus.cash.advance'),
        'state': 'draft',
        'date_ca': lambda *a: time.strftime('%Y-%m-%d'),
        'user_id': lambda obj, cr, uid, context: uid,
    }

    def onchange_amount_ca(self, cr, uid, ids, amount_total, amount_ca):
        v = {}
        if amount_ca>amount_total:
            warning = {
                       'title': _('Value Invalid!'),
                       'message' : 'Cash Advance Amount cannot more than PO amount total!'
                    }
            return {'value': {'amount_ca': 0.5*amount_total}, 'warning': warning}
        elif amount_ca<0:
            warning = {
                       'title': _('Value Invalid!'),
                       'message' : 'Cash Advance Amount cannot less than 0!'
                    }
            return {'value': {'amount_ca': 0.5*amount_total}, 'warning': warning}
        else:
            return {'value': {'amount_ca': amount_ca}}

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

    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for rec in self.browse(cr, uid, ids, context=context):
            if rec.state not in ['draft']:
                raise osv.except_osv(_('Invalid action !'), _('Only delete Draft Cash Advance'))

        return super(smcus_cash_advance, self).unlink(cr, uid, ids, context=context)

smcus_cash_advance()

class smcus_cash_advance_line(osv.osv):
    _name = "smcus.cash.advance.line"
    _description = "Telenais Cash Advance Line"

    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.price_unit * line.product_qty
        return res

    _columns = {
        'cash_advance_id': fields.many2one('smcus.cash.advance', 'Cash Advance', select=True, required=True, ondelete='cascade'),
        'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)]),
        'name': fields.char('Job Index', size=256, required=True),
        'address_allotment_id': fields.many2one('res.partner.address', 'Expatriate'),
        'customer_id': fields.many2one('res.partner', 'Customer', select=True, domain=[('customer', '=', True)]),
        'product_qty': fields.float('Quantity', required=True, digits=(16,2)),
        'product_uom': fields.many2one('product.uom', 'Product UOM', required=True),
        'price_unit': fields.float('Unit Price', required=True, digits_compute= dp.get_precision('Purchase Price')),
        'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal', digits_compute= dp.get_precision('Purchase Price')),
        'tax_id': fields.many2many('account.tax', 'smcus_cash_advance_tax', 'cash_advance_line_id', 'tax_id', 'Taxes'),
        'origin': fields.char('Origin', size=100),
    }
    
    def onchange_product(self, cr, uid, ids, product_id):
        prod_obj = self.pool.get('product.product')
        if product_id:
            product = prod_obj.read(cr, uid, product_id, ['name'], context=None)
            return {'value': {'name': product['name']}}

smcus_cash_advance_line()
