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


class status_karyawan_pajak(osv.osv):
	_name = 'hr.status_karyawan_pajak'
	_description = 'Status Karyawan Untuk PPH 21'

	def default_active(self, cr, uid, context={}):
		return 1
		
	_columns = 	{
				'name' : fields.char('Status Karyawan', size=30, required=True),
				'kode' : fields.char('Kode', size=10, required=True),
				'active' : fields.boolean('Aktif'),
				'keterangan' : fields.text('Keterangan'),
				}
				
	_defaults =	{
				'active' : default_active,
				}

status_karyawan_pajak()
