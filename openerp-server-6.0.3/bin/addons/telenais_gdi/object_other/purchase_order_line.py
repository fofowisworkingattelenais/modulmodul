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

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from osv import osv, fields
import netsvc
import pooler
from tools.translate import _
import decimal_precision as dp
from osv.orm import browse_record, browse_null



class purchase_order_line(osv.osv):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'

    def function_lenght_dummy(self, cr, uid, ids, field_name, args, context=None):
	    res = {}
	    obj_line = self.pool.get('purchase.order.line')
	
	    for line in obj_line.browse(cr, uid, ids):				
		    res[line.id] = line.lenght
		
	    return res
	
    def function_width_dummy(self, cr, uid, ids, field_name, args, context=None):
	    res = {}
	    obj_line = self.pool.get('purchase.order.line')
	
	    for line in obj_line.browse(cr, uid, ids):				
		    res[line.id] = line.lenght
		
	    return res			

    _columns = {
                            'lenght' : fields.float(string='Lenght', digits=(16,2)),
                            'width' : fields.float(string='Width', digits=(16,2)),
                            'lenght_dummy' : fields.function(fnct=function_lenght_dummy, string='Lenght', type='float', digits=(16,2), method=True, store=False),
                            'width_dummy' : fields.function(fnct=function_width_dummy, string='Width', type='float', digits=(16,2), method=True, store=False)
		    }
		
    def product_id_change(self, cr, uid, ids, pricelist, product, qty, uom, partner_id, date_order=False, fiscal_position=False, date_planned=False, name=False, price_unit=False, notes=False):
        obj_produk = self.pool.get('product.product')
        
        res = super(purchase_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom, partner_id, date_order, fiscal_position, date_planned, name, price_unit, notes)
        
        if product:
            produk = obj_produk.browse(cr, uid, [product])[0]
            res['value'].update({'lenght' : produk.lenght, 'lenght_dummy' : produk.lenght, 'width' : produk.width, 'width_dummy' : produk.width})
        return res			


purchase_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

