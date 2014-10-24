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


from osv import fields, osv


class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'
    _columns = {
            'ctn_no': fields.float(string='Ctn No', digits=(4, 1),  required=True),
            # 'client_order_ref': fields.many2one('sale.order', 'Client Order Reference'),
            # 'payment_term': fields.many2one('account.payment.term', 'Payment Term'),
            # 'pricelist_id':fields.many2one('product.pricelist', 'Pricelist', required=True,  help="The pricelist sets the currency used for this purchase order. It also computes the supplier price for the selected products/quantities."),
            # 'currency_id': fields.related('pricelist_id', 'currency_id', type="many2one", relation="res.currency", string="Currency",readonly=True, required=True),
            # 'gross_weight': fields.float(string='Gross Weight', digits=(4, 1), required=True),
            # 'net_weight': fields.float(string='Net Weight', digits=(4, 1), required=True),
        }

stock_move()

class stock_picking(osv.osv):
    # _name = 'stock.picking'
    _inherit = 'stock.picking'

    _columns = {
            'ctn_no': fields.float(string='Ctn No', digits=(4, 1),  required=True),
            # 'client_order_ref': fields.many2one('sale.order', 'Client Order Reference'),
            'payment_term': fields.many2one('account.payment.term', 'Payment Term'),

            'pricelist_id':fields.many2one('product.pricelist', 'Pricelist', required=True,  help="The pricelist sets the currency used for this purchase order. It also computes the supplier price for the selected products/quantities."),
            'currency_id': fields.related('pricelist_id', 'currency_id', type="many2one", relation="res.currency", string="Currency",readonly=True, required=True),
            'gross_weight': fields.float(string='Gross Weight', digits=(4, 1), required=True),
            'net_weight': fields.float(string='Net Weight', digits=(4, 1), required=True),
        }
    _defaults = {
        'ctn_no': 1.0
    }
stock_picking()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

