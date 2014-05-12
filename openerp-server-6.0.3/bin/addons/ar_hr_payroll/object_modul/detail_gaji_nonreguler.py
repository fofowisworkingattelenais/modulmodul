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


class detail_gaji_nonreguler(osv.osv):
	_name = 'hr.detail_gaji_nonreguler'
	_description = 'Detail Gaji Non Reguler'
	

		
		
	_columns = 	{
				'gaji_nonreguler_id' : fields.many2one(obj='hr.gaji_nonreguler', string='Gaji Non-Reguler'),
				'employee_id' : fields.many2one(obj='hr.employee', string='Karyawan', required=True),
				'eksekusi_penggajian_id' : fields.many2one(obj='hr.eksekusi_penggajian', string='Eksekusi Penggajian', readonly=True),
				}


				
		
		
				

				
detail_gaji_nonreguler()


