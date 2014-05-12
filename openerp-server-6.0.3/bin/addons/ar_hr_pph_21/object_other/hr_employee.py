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

class hr_employee(osv.osv):
	_name = 'hr.employee'
	_inherit = 'hr.employee'

	_columns =	{
				'kategori_ptkp_id' : fields.many2one('hr.kategori_ptkp', 'Kategori PTKP'),
				'tipe_pph' : fields.selection(selection=[('gross','Gross'),('net','Net'),('gross_up','Gross-Up')], string='Tipe PPH'),
				'status_karyawan_pajak_id' : fields.many2one(obj='hr.status_karyawan_pajak', string='Status Karyawan'),
				'pn_kumulatif_sebelum' : fields.float('Penghasilan Netto Sebelumnya', Digits=(16,2)),
				'pph_kumutalif_sebelum' : fields.float('PPH 21 Sebelumnya', Digits=(16,2)),
				'masa_pajak_bergabung_ids': fields.many2one(obj='pajak.masa_pajak', string='Masa Pajak Bergabung', readonly=True),
				}

	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_employee, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_employee, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(hr_employee, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			

hr_employee()




