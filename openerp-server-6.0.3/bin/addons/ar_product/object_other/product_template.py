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

class product_template(osv.osv):
	def default_categ_id(self, cr, uid, context={}):
		nama_kategori = context.get('nama_kategori', False)
		
		if not nama_kategori:
			return super(product_template, self)._default_category(cr, uid, context)
			
		kategori_ids = self.pool.get('product.category').search(cr, uid, [('name', '=', nama_kategori)])
		
		if not kategori_ids:
			return super(product_template, self)._default_category(cr, uid, context)
			
		return kategori_ids[0]
		
	def default_uom_id(self, cr, uid, context={}):
		nama_uom = context.get('nama_uom', False)
		
		if not nama_uom:
			return super(product_template, self)._get_uom_id(cr, uid, context)
			
		uom_ids = self.pool.get('product.uom').search(cr, uid, [('name', '=', nama_uom)])
		
		if not uom_ids:
			return super(product_template, self)._get_uom_id(cr, uid, context)
			
		return uom_ids[0]

	_name = 'product.template'
	_inherit = 'product.template'
	_defaults = {
		'categ_id' : default_categ_id,
		'uom_id' : default_uom_id,
		'uom_po_id' : default_uom_id,
		}

	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(product_template, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(product_template, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(product_template, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			

product_template()




