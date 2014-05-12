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

from osv import fields, osv
from tools.translate import _
import decimal_precision as dp

class wizard_split_requsition_line(osv.osv_memory):
	_name = 'gdi.wizard_split_purchase_requsition'
	_description = 'Wizard Split Purchase Requsition'
	
	_columns = {
        'quantity': fields.float('Quantity',digits_compute=dp.get_precision('Product UOM')),
    }
	_defaults = {
		'quantity': lambda *x: 0,
	}
	
	def split(self, cr, uid, data, context=None):

		purchase_requisition_line_obj = self.pool.get('purchase.requisition.line')
		
		purchase_requisition_obj = self.pool.get('purchase.requisition')
		
		records_id = context and context.get('active_ids', False)
		
		company = self.pool.get('res.users').browse(cr, uid, uid, context).company_id
	
		quantity = self.browse(cr, uid, data[0], context=context).quantity or 0.0
		
		for purchase_requisition_line in purchase_requisition_line_obj.browse(cr, uid, records_id, context=context):
			if quantity > purchase_requisition_line.product_qty:
				raise osv.except_osv(_('Error!'),  _('Total quantity after split exceeds the quantity to split ' \
									'for this product: "%s" (id: %d)') % \
									(purchase_requisition_line.product_id.name, purchase_requisition_line.product_id.id,))
									
			quantity_rest = purchase_requisition_line.product_qty - quantity
			
			purchase_requisition_line_obj.write(cr, uid, [purchase_requisition_line.id], {
					'product_qty': quantity_rest,
                })
			
			purchase_requsition_line= {
				'product_id': purchase_requisition_line.product_id.id,
				'product_uom_id': purchase_requisition_line.product_uom_id.id,
				'product_qty': quantity,
				'company_id': company.id,
				'requisition_id' : purchase_requisition_line.requisition_id.id,
				}
			new_purchase_requisition_line_id = purchase_requisition_line_obj.create(cr,uid,purchase_requsition_line)
			
		return {'type': 'ir.actions.act_window_close'}
		
wizard_split_requsition_line()


