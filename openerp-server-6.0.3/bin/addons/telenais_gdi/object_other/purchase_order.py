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



class purchase_order(osv.osv):
    _name = "purchase.order"
    _inherit = 'purchase.order'

    _columns = {
				    'chk_import' : fields.boolean(string='Import'),
		    }

    def action_picking_create(self,cr, uid, ids, *args):
        obj_picking = self.pool.get('stock.picking')
        obj_purchase = self.pool.get('purchase.order')
        
        picking_id = super(purchase_order, self).action_picking_create(cr, uid, ids, *args)   
        for purchase in obj_purchase.browse(cr, uid, ids):
            obj_picking.write(cr, uid, [picking_id], {'chk_import' : purchase.chk_import})
        return picking_id
        
purchase_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

