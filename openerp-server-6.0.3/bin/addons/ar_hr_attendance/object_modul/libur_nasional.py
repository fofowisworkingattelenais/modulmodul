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


class libur_nasional(osv.osv):
	_name = 'hr.libur_nasional'
	_description = 'Libur Nasional'
	
	def default_active(self, cr, uid, context={}):
		return 1

		
		
	_columns = 	{
				'name' : fields.char(string='Hari Libur', size=100, required=True),
				'tanggal' : fields.date(string='Tanggal', required=True),				
				'active' : fields.boolean(string='Aktif'),
				'keterangan' : fields.text(string='Keterangan'),
				
				}
				
	_defaults =	{
				'active' : default_active,
				}
				
libur_nasional()


