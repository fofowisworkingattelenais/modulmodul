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


class wizard_import_product(osv.osv_memory):
	_name = 'gdi.wizard_import_product'
	_description = 'Wizard Import Product'

	_columns = 	{
				'import_file' : fields.binary(string='File', required='True'),
				}
				
	def get_id(self, cr, uid, object_name, field_name):
		id_object = []
		
		obj_id = self.pool.get(object_name)
		
		kriteria = [('name','=',field_name)]
		
		obj_ids = obj_id.search(cr, uid, kriteria)
		
		for obj in obj_id.browse(cr,uid,obj_ids):
			if obj:
				id_object = obj.id
			else:
				raise osv.except_osv(_('Error'), _('Data %s in %s is not defined !')%(field_name,object_name,))
		return id_object
		
	def get_cost_method(self, cr, uid, field_name):
		method_name = []
		
		if field_name == 'Standard Price':
			method_name = 'standard'
		else:
			method_name = 'average'
		return method_name
		
	def get_procure_method(self, cr, uid, field_name):
		method_name = []
		
		if field_name == 'Make to Stock':
			method_name = 'make_to_stock'
		else:
			method_name = 'make_to_order'
		return method_name
		
	def get_supply_method(self, cr, uid, field_name):
		method_name = []
		
		if field_name == 'Produce':
			method_name = 'produce'
		else:
			method_name = 'buy'
		return method_name

	def get_type(self, cr, uid, field_name):
		hasil = ''
		
		if field_name == 'Stockable Product':
			hasil = 'product'
		elif field_name == 'Consumable':
			hasil = 'consu'
		elif field_name == 'Service':
			hasil = 'service'
		return hasil
		
	def get_valuation(self, cr, uid, field_name):
		method_name = []
		
		if field_name == 'Periodical (manual)':
			method_name = 'manual_periodic'
		else:
			method_name = 'real_time'
		return method_name

	def import_csv(self, cr, uid, ids, data, context=None):
		obj_wizard = self.pool.get('gdi.wizard_import_product')
		obj_product = self.pool.get('product.product')
		
		import_data = obj_wizard.browse(cr, uid, ids)[0]
		
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(import_data.import_file))
		fileobj.seek(0)
		reader = csv.DictReader(fileobj, delimiter=',')

		for baris in reader:
			kriteria = [('default_code','=',baris['default_code'])]
			product_ids = obj_product.search(cr, uid, kriteria)
			
			if not product_ids:
				val =   {
						'default_code' : baris['default_code'],
						'name' : baris['name'],
						'mes_type' : baris['mes_type'],
						'uom_po_id' : self.get_id(cr, uid, 'product.uom',baris['uom_po_id']),
						'uom_id': self.get_id(cr, uid, 'product.uom',baris['uom_id']),
						'type': self.get_type(cr, uid, baris['type']),
						'standard_price': baris['standard_price'],
						'cost_method': self.get_cost_method(cr, uid, baris['cost_method']),
						'company_id': self.get_id(cr, uid, 'res.company',baris['company_id']),
						'valuation': self.get_valuation(cr, uid, baris['valuation']),
						'procure_method': self.get_procure_method(cr, uid, baris['procure_method']),
						'supply_method': self.get_supply_method(cr, uid, baris['supply_method']),
						'categ_id': self.get_id(cr, uid, 'product.category',baris['categ_id']),
						'purchase_ok': baris['purchase_ok'],
						'sale_ok': baris['sale_ok'],
						'purchase_requisition' : baris['purchase_requisition'],
						'currency_standard_id' :  self.get_id(cr, uid, 'res.currency',baris['currency_standard_id']),
						'currency_list_id' :  self.get_id(cr, uid, 'res.currency',baris['currency_list_id']),
						}
				obj_product.create(cr, uid, val)
		return {'type': 'ir.actions.act_window_close'}
wizard_import_product()


