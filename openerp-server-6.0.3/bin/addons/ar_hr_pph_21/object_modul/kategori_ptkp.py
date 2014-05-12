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


class kategori_ptkp(osv.osv):
	_name = 'hr.kategori_ptkp'
	_description = 'Kategori PTKP'

	def default_active(self, cr, uid, context={}):
		return 1
		
	_columns = 	{
				'name' : fields.char('Kategori PTKP', size=30, required=True),
				'kode' : fields.char('Kode', size=10, required=True),
				'ptkp_tahunan' : fields.float('PTKP Per Tahun', Digits=(16,2), required=True),
				'active' : fields.boolean('Aktif'),
				'keterangan' : fields.text('Keterangan'),
				}
				
	_defaults =	{
				'active' : default_active,
				}

kategori_ptkp()
