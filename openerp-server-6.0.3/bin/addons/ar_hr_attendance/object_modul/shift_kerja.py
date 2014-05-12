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


class shift_kerja(osv.osv):
	_name = 'hr.shift_kerja'
	_description = 'Shift Kerja'

	def default_active(self, cr, uid, context={}):
		return True
		
	_columns = 	{
				'name' : fields.char(string='Shift', size=30, required=True),
				'jam_masuk' : fields.float(string='Jam Masuk', required=True),
				'jam_keluar' : fields.float(string='Jam Keluar', required=True),
				'mulai_istirahat' : fields.float(string='Mulai Istrirahat', required=True),
				'selesai_istirahat' : fields.float(string='Selesai Istirahat', required=True),	
				'active' : fields.boolean(string='Aktif'),
				'keterangan' : fields.text(string='Keterangan'),	
				}
				
	_defaults =	{
				'active' : default_active,
				}
				
shift_kerja()


