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

class sale_order(osv.osv):
    _inherit = "sale.order"

    #smcus_tel: add field smcus_address_allotment_id dan smcus_customer_id ke procurement saat generate procurement dari sale.order
    def action_ship_create(self, cr, uid, ids, *args):
        res = super(sale_order, self).action_ship_create(cr, uid, ids, *args)
        #to pymad
        py_obj = self.pool.get('smcus.pymad')
        pyl_obj = self.pool.get('smcus.pymad.line')

        for order in self.browse(cr, uid, ids, context={}):
            vals = { 
                'partner_id': order.partner_id.id,
                'origin': order.name,
                'order_id': order.id,
                'date_order': order.date_order,
                'user_id': order.user_id.id,
                'amount_untaxed': order.amount_untaxed,
                'amount_tax': order.amount_tax,
                'amount_total': order.amount_total,
            }
            py_id = py_obj.create(cr, uid, vals, context=None)

            for line in order.order_line:
                vals = { 
                    'pymad_id': py_id,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'address_allotment_id': line.address_allotment_id.id,
                    'customer_id': order.partner_id.id,
                    'product_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'tax_id': [(6, 0, [x.id for x in line.tax_id])],
                }
                pyl_id = pyl_obj.create(cr, uid, vals, context=None)
            py_name = py_obj.read(cr, uid, py_id, ['name'], context=None)
            message = _("A Draft PyMAD '%s' is created.") % (py_name['name'],)
            self.log(cr, uid, order.id, message)

        return True

    def action_cancel(self, cr, uid, ids, *args):
        #delete pymad
        py_obj = self.pool.get('smcus.pymad')
        for order in self.browse(cr, uid, ids, context={}):
            res_id = py_obj.search(cr, uid, [('state', 'in', ('cancel', 'validated', 'invoiced')),
                                            ('order_id', '=', order.id)])
            if res_id:
                raise osv.except_osv(_('Invalid action !'), _('There still some PyMAD which still in progress. Make sure all PyMAD is in draft state'))
                
            res_id = py_obj.search(cr, uid, [('state', '=', 'draft'),
                                            ('order_id', '=', order.id)])
            #remove smcus_pymad
            py_obj.unlink(cr, uid, res_id, context=None)
            
        res = super(sale_order, self).action_cancel(cr, uid, ids, *args)
        

sale_order()
