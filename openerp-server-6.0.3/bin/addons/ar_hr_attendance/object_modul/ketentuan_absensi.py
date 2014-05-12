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
from datetime import date
import decimal_precision as dp
from tools.safe_eval import safe_eval as eval


class ketentuan_absensi(osv.osv):
	_name = 'hr.ketentuan_absensi'
	_description = 'Ketentuan Absensi'
	
	def default_active(self, cr, uid, context={}):
		return 1

	_columns = 	{
				'name' : fields.char(string='Ketentuan Absensi', size=100, required=True),
				'kode' : fields.char(string='Kode', size=30, required=True),
				'satuan_ukur_id' : fields.many2one(string='Satuan', obj='product.uom', required=True),				
				'active' : fields.boolean(string='Aktif'),
				'keterangan' : fields.text(string='Keterangan'),
				'perhitungan_python' : fields.text(string='Perhitungan Ketentuan'),				
				}
				
	_defaults =	{
				'active' : default_active,
				}
				
	def hitung_ketentuan(self, cr, uid, id, localdict, context=None):
		obj_ketentuan_absensi = self.pool.get('hr.ketentuan_absensi')
		
		ketentuan_absensi = obj_ketentuan_absensi.browse(cr, uid, [id])[0]
		
		
		#try:
		eval(ketentuan_absensi.perhitungan_python, localdict, mode='exec', nocopy=True)
		val =	{
				'name' : ketentuan_absensi.name,
				'kode' : ketentuan_absensi.kode,
				'satuan_ukur_id' : ketentuan_absensi.satuan_ukur_id.id,
				'hasil' : localdict['hasil'],
				}
				
		return val
		#except:
			#raise osv.except_osv('Perhitungan!', 'Perhitungan ketentuan salah')

ketentuan_absensi()


