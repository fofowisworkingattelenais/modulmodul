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

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from osv import fields, osv
from osv.orm import browse_record, browse_null
from tools.translate import _


class wizard_purchase_requsition_line_united(osv.osv_memory):
	_name = 'gdi.wizard_purchase_requsition'
	_description = 'Wizard Purchase Requsition Line United'
	
	_columns = {
		'partner_id': fields.many2one('res.partner', 'Partner', required=True,domain=[('supplier', '=', True)]),
		'partner_address_id':fields.many2one('res.partner.address', 'Address', required=True),
    }
    
	def onchange_partner_id(self, cr, uid, ids, partner_id):
		if not partner_id:
			return {}
		addr = self.pool.get('res.partner').address_get(cr, uid, [partner_id], ['default'])
		part = self.pool.get('res.partner').browse(cr, uid, partner_id)
		return {'value':{'partner_address_id': addr['default']}}
		
	def cek_warehouse(self, cr, uid, record_ids):
		purchase_requisition_line_obj = self.pool.get('purchase.requisition.line')
		purchase_requisition_obj = self.pool.get('purchase.requisition')
		stock_warehouse_obj = self.pool.get('stock.warehouse')
		location_id = []
		next_location_id = []

		for purchase_requisition_line in purchase_requisition_line_obj.browse(cr, uid, record_ids):

			kriteria = [('id','=',purchase_requisition_line.requisition_id.id)]
			purchase_requisition_ids = purchase_requisition_obj.search(cr, uid, kriteria)
			
			for purchase_requisition in purchase_requisition_obj.browse(cr, uid, purchase_requisition_ids):
				if location_id == []:
					location_id = stock_warehouse_obj.read(cr, uid, [purchase_requisition.warehouse_id.id], ['lot_input_id'])[0]['lot_input_id'][0]
				else:
					next_location_id = stock_warehouse_obj.read(cr, uid, [purchase_requisition.warehouse_id.id], ['lot_input_id'])[0]['lot_input_id'][0]
					if location_id <> next_location_id:
						return False
		return {'location_id':location_id , 'warehouse_id':purchase_requisition.warehouse_id.id}

	def united(self, cr, uid, ids, context=None):
		order_obj = self.pool.get('purchase.order')
		order_line_obj = self.pool.get('purchase.order.line')
		partner_obj = self.pool.get('res.partner')
		purchase_requisition_line_obj = self.pool.get('purchase.requisition.line')
		pricelist_obj = self.pool.get('product.pricelist')
		prod_obj = self.pool.get('product.product')
		purchase_requisition_obj = self.pool.get('purchase.requisition')
		acc_pos_obj = self.pool.get('account.fiscal.position')
		
		if context is None:
			context = {}
		record_ids = context and context.get('active_ids', False)
		
		location_id = self.cek_warehouse(cr, uid, record_ids)['location_id']
		
		warehouse_id = self.cek_warehouse(cr, uid, record_ids)['warehouse_id']
		
		if not location_id:
			raise osv.except_osv('PERINGATAN', 'Every records in purchase requsition line does not have the same warehouse')
		
		if record_ids:
			data =  self.read(cr, uid, ids)
			company = self.pool.get('res.users').browse(cr, uid, uid, context).company_id
			partner_id = data[0]['partner_id']
			
			supplier_data = partner_obj.browse(cr, uid, partner_id, context=context)
			
			address_id = partner_obj.address_get(cr, uid, [partner_id], ['delivery'])['delivery']
			list_line=[]
			purchase_order_line={}

			for purchase_requisition_line in purchase_requisition_line_obj.browse(cr, uid, record_ids, context=context):
				state = 'draft'
				partner_list = sorted([(partner.sequence, partner) for partner in  purchase_requisition_line.product_id.seller_ids if partner])
				partner_rec = partner_list and partner_list[0] and partner_list[0][1] or False
				uom_id = purchase_requisition_line.product_uom_id.id
				
				newdate = datetime.today() - relativedelta(days=company.po_lead)
				delay = partner_rec and partner_rec.delay or 0.0
				
				if delay:
					newdate -= relativedelta(days=delay)
				
				partner = partner_rec and partner_rec.name or supplier_data
				pricelist_id = partner.property_product_pricelist_purchase and partner.property_product_pricelist_purchase.id or False
				price = pricelist_obj.price_get(cr, uid, [pricelist_id], purchase_requisition_line.product_id.id, purchase_requisition_line.product_qty, False, {'uom': uom_id})[pricelist_id]
				product = prod_obj.browse(cr, uid, purchase_requisition_line.product_id.id, context=context)
				
				if not list_line:

					purchase_order_line= {
							'name': product.partner_ref,
							'product_qty': purchase_requisition_line.product_qty,
							'product_id': purchase_requisition_line.product_id.id,
							'product_uom': purchase_requisition_line.product_uom_id.id,
							'price_unit': price,
							'date_planned': newdate.strftime('%Y-%m-%d %H:%M:%S'),
							'notes': product.description_purchase,
					}
					
					taxes_ids = purchase_requisition_line.product_id.product_tmpl_id.supplier_taxes_id
					taxes = acc_pos_obj.map_tax(cr, uid, partner.property_account_position, taxes_ids)
					purchase_order_line.update({
						'taxes_id': [(6,0,taxes)]
						})
					list_line.append(purchase_order_line)
					
				else:
					i = 0
					for x in list_line:
						if x['product_id'] == purchase_requisition_line.product_id.id and x['product_uom'] == purchase_requisition_line.product_uom_id.id:
							list_line[i]['product_qty'] += purchase_requisition_line.product_qty
							state = 'update'
						i += 1
							
					if state <> 'update':
							
						purchase_order_line= {
								'name': product.partner_ref,
								'product_qty': purchase_requisition_line.product_qty,
								'product_id': purchase_requisition_line.product_id.id,
								'product_uom': uom_id,
								'price_unit': price,
								'date_planned': newdate.strftime('%Y-%m-%d %H:%M:%S'),
								'notes': product.description_purchase,
						}
					
						taxes_ids = purchase_requisition_line.product_id.product_tmpl_id.supplier_taxes_id
						taxes = acc_pos_obj.map_tax(cr, uid, partner.property_account_position, taxes_ids)
						purchase_order_line.update({
							'taxes_id': [(6,0,taxes)]
							})
						list_line.append(purchase_order_line)
				purchase_requisition_line_obj.write(cr, uid, [purchase_requisition_line.id], {'chk_line': True})
				
			purchase_id = order_obj.create(cr, uid, {
				'partner_id': partner_id,
				'partner_address_id': address_id,
				'pricelist_id': pricelist_id,
				'company_id': company.id,
				'fiscal_position': partner.property_account_position and partner.property_account_position.id or False,
				'warehouse_id': warehouse_id,
				'location_id':location_id,
			})
			order_ids=[]
			for order_line in list_line:
				order_line.update({
					'order_id': purchase_id
					})
				order_line_obj.create(cr,uid,order_line)
		return {'type': 'ir.actions.act_window_close'}
wizard_purchase_requsition_line_united()


