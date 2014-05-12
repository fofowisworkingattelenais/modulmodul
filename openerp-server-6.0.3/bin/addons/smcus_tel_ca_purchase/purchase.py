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

class purchase_order(osv.osv):
    _inherit = "purchase.order"

    def wkf_confirm_order(self, cr, uid, ids, context=None):
        res = super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context=context)
        #to cash advance
        ca_obj = self.pool.get('smcus.cash.advance')
        cal_obj = self.pool.get('smcus.cash.advance.line')
        for order in self.browse(cr, uid, ids, context={}):
            vals = { 
                'partner_id': order.partner_id.id,
                'purchase_id': order.id,
                'date_po': order.date_order,
                'amount_untaxed': order.amount_untaxed,
                'amount_tax': order.amount_tax,
                'amount_total': order.amount_untaxed,
                #'amount_total': order.amount_total,
                'amount_ca': order.amount_untaxed*0.5,
            }
            ca_id = ca_obj.create(cr, uid, vals, context=context)

            for line in order.order_line:
                vals = { 
                    'cash_advance_id': ca_id,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'address_allotment_id': line.smcus_address_allotment_id.id,
                    'customer_id': line.smcus_customer_id.id,
                    'product_qty': line.product_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'tax_id': [(6, 0, [x.id for x in line.taxes_id])],
                    'origin': (order.name or '')+':'+(order.origin or ''),
                }
                cal_id = cal_obj.create(cr, uid, vals, context=context)
            ca_name = ca_obj.read(cr, uid, ca_id, ['name'], context=None)
            message = _("A Draft Cash Advance '%s' is created.") % (ca_name['name'],)
            self.log(cr, uid, order.id, message)

        return True

    def action_cancel(self, cr, uid, ids, *args):
        #delete cash advance
        ca_obj = self.pool.get('smcus.cash.advance')
        for order in self.browse(cr, uid, ids, context={}):
            res_id = ca_obj.search(cr, uid, [('state', 'in', ('cancel', 'validated')),
                                            ('purchase_id', '=', order.id)])
            if res_id:
                raise osv.except_osv(_('Invalid action !'), _('There still Cash Advance which still in progress. Make sure Cash Advance is in Draft state'))
                
            res_id = ca_obj.search(cr, uid, [('state', '=', 'draft'),
                                            ('purchase_id', '=', order.id)])
            #remove smcus_cash_advance
            ca_obj.unlink(cr, uid, res_id, context=None)
            
        res = super(purchase_order, self).action_cancel(cr, uid, ids, *args)
        return res

purchase_order()

