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


class detail_pola_kerja(osv.osv):
	_name = 'hr.detail_pola_kerja'
	_description = 'Detail Pola Kerja'


	def default_kerja(self, cr, uid, context={}):
		return 'masuk'
				
	_columns = 	{
				'name' : fields.integer(string='Hari Ke', required=True),
				'kerja' : fields.selection(selection=[('masuk','Masuk'),('libur','Libur')], string='Masuk Kerja', required=True),
				'shift_kerja_id' : fields.many2one(obj='hr.shift_kerja', string='Shift Kerja'),
				'pola_kerja_id' : fields.many2one(string='Pola Kerja', obj='hr.pola_kerja'),
				}
				
	_defaults =	{
				'kerja' : default_kerja,
				}
				
detail_pola_kerja()


