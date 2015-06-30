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

    def multiple_costprice_qty(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context):
            res[data.id] = data.cost_price * data.product_qty
        return res

    def amount_total_cost(self, cr, uid, ids, field, arg, context=None):
        #~ import ipdb;ipdb.set_trace();
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'total_cost_price': 0,
            }
            val = 0
            for line in order.total_cost:
                val += line.total_cost
            res[order.id] = val
        print res
        return res

    _columns = {
        'cost_price': fields.related('product_id', 'standard_price',type='char', size=64, relation="product.template", string="Cost Price"),
        'total_cost': fields.function(multiple_costprice_qty, type='integer'),
        'total_cost_price': fields.function(amount_total_cost,type='integer',string='Total Amount'),
        }



stock_move()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

