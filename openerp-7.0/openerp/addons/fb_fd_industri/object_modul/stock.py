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
            'ctn_no': fields.char(string='Ctn No', size=100),
            'custpono': fields.char(string='Customer Po No', size=100),
            'measurement': fields.char(string='Measurement', size=100),
            # 'client_order_ref': fields.many2one('sale.order', 'Client Order Reference'),
            'payment_term': fields.many2one('account.payment.term', 'Payment Term'),
            'pricelist_id':fields.many2one('product.pricelist', 'Pricelist', required=True,  help="The pricelist sets the currency used for this purchase order. It also computes the supplier price for the selected products/quantities."),
            'currency_id': fields.related('pricelist_id', 'currency_id', type="many2one", relation="res.currency", string="Currency",readonly=True, required=True),

            'remark': fields.char(string='Remark', size=100),
            'countryorigin': fields.char(string='Country of Origin', size=100),
            'packing': fields.char(string='Packing', size=100),

            # 'gross_weight': fields.float(string='Gross Weight', digits=(4, 1), required=True),
            # 'net_weight': fields.float(string='Net Weight', digits=(4, 1), required=True),
        }


    def _prepare_chained_picking(self, cr, uid, picking_name, picking, picking_type, moves_todo, context=None):

        vals = super(stock_move, self)._prepare_chained_picking(cr, uid, picking_name, picking, picking_type, moves_todo, context=None)
        vals.update({'pricelist_id': picking.pricelist_id.id, 'payment_term': picking.payment_term.id})
        return vals

stock_move()


class stock_picking(osv.osv):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    _columns = {
                'ctn_no': fields.char(string='Ctn No', size=100),
                'custpono': fields.char(string='Customer Po No', size=100),
                'measurement': fields.char(string='Measurement', size=100),
                # 'client_order_ref': fields.many2one('sale.order', 'Client Order Reference'),
                'payment_term': fields.many2one('account.payment.term', 'Payment Term'),
                'pricelist_id':fields.many2one('product.pricelist', 'Pricelist', required=True,  help="The pricelist sets the currency used for this purchase order. It also computes the supplier price for the selected products/quantities."),
                'currency_id': fields.related('pricelist_id', 'currency_id', type="many2one", relation="res.currency", string="Currency",readonly=True, required=True),
                # 'gross_weight': fields.float(string='Gross Weight', digits=(4, 1), required=True),
                # 'net_weight': fields.float(string='Net Weight', digits=(4, 1), required=True),
                'remark': fields.char(string='Remark', size=100),
                'countryorigin': fields.char(string='Country of Origin', size=100),
                'packing': fields.char(string='Packing', size=100),

            }



stock_picking()


class stock_picking_out(osv.osv):
    # _name = 'stock.picking.out'
    _inherit = 'stock.picking.out'

    _columns = {
                # 'ctn_no': fields.char(string='Ctn No', size=100),
                'custpono': fields.char(string='Customer Po No', size=100),
                # 'measurement': fields.char(string='Measurement', size=100)
                'payment_term': fields.many2one('account.payment.term', 'Payment Term'),
                'pricelist_id':fields.many2one('product.pricelist', 'Pricelist', required=True,  help="The pricelist sets the currency used for this purchase order. It also computes the supplier price for the selected products/quantities."),
                'currency_id': fields.related('pricelist_id', 'currency_id', type="many2one", relation="res.currency", string="Currency",readonly=True, required=True),

                'remark': fields.char(string='Remark', size=100),
                'countryorigin': fields.char(string='Country of Origin', size=100),
                'packing': fields.char(string='Packing', size=100),

            }
    # _defaults = {
    #     'ctn_no': 1.0
    # }



stock_picking_out()

class stock_picking_in(osv.osv):
    # _name = 'stock.picking.out'
    _inherit = 'stock.picking.in'

    _columns = {
                # 'ctn_no': fields.char(string='Ctn No', size=100),
                'custpono': fields.char(string='Customer Po No', size=100),
                # 'measurement': fields.char(string='Measurement', size=100)


            }
    # _defaults = {
    #     'ctn_no': 1.0
    # }
stock_picking_in()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

