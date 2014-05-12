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


class wizard_import_perbaikan_data_product(osv.osv_memory):
	_name = 'titis.wizard_import_perbaikan_data_product'
	_description = 'Wizard Import Perbaikan Data Product'

		
	_columns = 	{
								'import_file' : fields.binary(string='File', required='True'),			
								}

	def import_data(self, cr, uid, ids, data, context=None):
		obj_wizard = self.pool.get('titis.wizard_import_perbaikan_data_product')
		obj_product = self.pool.get('product.product')
		
		import_data = obj_wizard.browse(cr, uid, ids)[0]
		
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(import_data.import_file))
		fileobj.seek(0)
		reader = csv.DictReader(fileobj, delimiter=',')

		for baris in reader:
			kriteria = [('default_code','=',baris['kode'])]
			product_ids = obj_product.search(cr, uid, kriteria)
			
			if product_ids:
				obj_product.write(cr, uid, product_ids, {'kategori_lama' : baris['kategori_lama']})
				
				
		
		return {'type': 'ir.actions.act_window_close'}
				
wizard_import_perbaikan_data_product()


