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
##############################################################################

import wizard
from osv import fields, osv
from datetime import date
import netsvc
from tools.translate import _


class wizard_batch_product_change(osv.osv_memory):
	_name = 'titis.wizard_batch_product_change'
	_description = 'Wizard Batch Product Change'

		
	_columns = 	{
								'categ_id' : fields.many2one(obj='product.category', string='Product Category', domain=[('type','=','normal')]),
								'uom_id' : fields.many2one(obj='product.uom', string='Product UoM'),
								'uom_po_id' : fields.many2one(obj='product.uom', string='Product Purchase UOM'),								
								}

	def change_product_data(self, cr, uid, ids, data, context=None):
		obj_product = self.pool.get('product.product')
		
		
		wizard = self.browse(cr, uid, ids)[0]
		res = {}
		
		if wizard.categ_id:
			res.update({'categ_id' : wizard.categ_id.id})
		
		if wizard.uom_id:
			res.update({'uom_id' : wizard.uom_id.id})
			
		if wizard.uom_po_id:
			res.update({'uom_po_id' : wizard.uom_po_id.id})
			
		if wizard.uom_id and wizard.uom_po_id:
			if wizard.uom_id.category_id.id != wizard.uom_po_id.category_id.id:
				raise osv.except_osv('Warning!', 'UoM and Purchase UoM should be on same category')
	
		
		obj_product.write(cr, uid, data['active_ids'], res)
		
		
		return {'type': 'ir.actions.act_window_close'}
				
wizard_batch_product_change()


