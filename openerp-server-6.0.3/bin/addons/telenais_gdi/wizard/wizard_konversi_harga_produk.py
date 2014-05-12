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
import csv
import tools
import base64
from tempfile import TemporaryFile


class wizard_konversi_harga_produk(osv.osv_memory):
	_name = 'gdi.wizard_konversi_harga_produk'
	_description = 'Wizard Konversi Harga Produk'
	
	def default_price_to_convert(self, cr, uid, ids, context={}):
		return 'both'

	_columns = 	{
				'currency_from_id' : fields.many2one(obj='res.currency', string='Currency From', required='True'),
				'currency_to_id' : fields.many2one(obj='res.currency', string='Currency To', required='True'),
				'price_to_convert' : fields.selection(selection=[('standard','Cost Price'),('list','Sale Price'),('both','Both')], string='Price To Convert', required=True),
				}
				
	_defaults =	{
							'price_to_convert' : default_price_to_convert,
							}

	def konversi_currency(self, cr, uid, ids, context=None):
		product_ids = context.get('active_ids')
		obj_currency = self.pool.get('res.currency')
		obj_product = self.pool.get('product.product')
		obj_product_template = self.pool.get('product.template')
		obj_wizard = self.pool.get('gdi.wizard_konversi_harga_produk')

		data = obj_wizard.browse(cr, uid, ids)[0]

		if not product_ids:
			return {'type': 'ir.actions.act_window_close'}
						
		if data.price_to_convert == 'standard':
			kriteria = [('id','in',product_ids),('currency_standard_id','=',data.currency_from_id.id)]
		elif data.price_to_convert == 'list':
			kriteria = [('id','in',product_ids),('currency_list_id','=',data.currency_from_id.id)]
		else:
			kriteria = [('id','in',product_ids),'|',('currency_standard_id','=',data.currency_from_id.id),('currency_list_id','=',data.currency_from_id.id)]
			
		produk_ids = obj_product.search(cr, uid, kriteria)
		
		if not produk_ids:
			return {'type': 'ir.actions.act_window_close'}
			
		for product in obj_product.browse(cr, uid, produk_ids):			
			val = {}
			standard_price = obj_currency.compute(cr, uid, data.currency_from_id.id, data.currency_to_id.id, product.product_tmpl_id.standard_price, round=True, context={})
			list_price = obj_currency.compute(cr, uid, data.currency_from_id.id, data.currency_to_id.id, product.product_tmpl_id.list_price, round=True, context={})

			if data.price_to_convert == 'standard':
				val.update({'standard_price' : standard_price, 'currency_standard_id' : data.currency_to_id.id})
			elif data.price_to_convert == 'list':
				val.update({'list_price' : list_price, 'currency_list_id' : data.currency_to_id.id})
			else:
				val.update({'standard_price' : standard_price, 'list_price' : list_price, 'currency_standard_id' : data.currency_to_id.id, 'currency_list_id' : data.currency_to_id.id})
				
			obj_product.write(cr, uid, product.id, val)

		return {'type': 'ir.actions.act_window_close'}

wizard_konversi_harga_produk()


