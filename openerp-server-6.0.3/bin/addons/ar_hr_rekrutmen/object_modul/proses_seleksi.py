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


class proses_seleksi(osv.osv):
	_name = 'hr.proses_seleksi'
	_description = 'Proses Seleksi'
	
	def default_active(self, cr, uid, context={}):
		return 1
		
	_columns = 	{
				'name' : fields.char('Proses Seleksi', size=100, required=True),
				'kode' : fields.char('Kode', size=30),
				'active' : fields.boolean('Aktif'),
				'tahap_seleksi_ids' : fields.one2many('hr.tahap_seleksi', 'proses_seleksi_id', 'Tahap Seleksi'),
				}
		
	_defaults = {
				'active' : default_active,
				}
				
	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi_create', 'aman')
		
		if situasi == 'aman':
			return super(proses_seleksi, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi_copy', 'aman')
		
		if situasi == 'aman':
			return super(proses_seleksi, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi_unlink', 'aman')
		
		if situasi == 'aman':
			return super(proses_seleksi, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			
	def write(self, cr, uid, values, context={}):
		# Overriding method write
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi_write', 'aman')
		
		if situasi == 'aman':
			return super(proses_seleksi, self).write(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa diedit')				
		
proses_seleksi()
