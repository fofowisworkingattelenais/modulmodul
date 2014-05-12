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

class sequence_bulan(osv.osv):
	_name = 'base.sequence_bulan'
	_description = 'Sequence Per Bulan'
	_columns =	{
							'sequence_id' : fields.many2one(string='Sequence', obj='ir.sequence'),
							'tahun' : fields.integer(string='Tahun', required=True),
							'bulan_id' : fields.many2one(string='Bulan', obj='base.bulan', required=True),
							'sequence_bulan_id' : fields.many2one(string='Sequence Bulanan', obj='ir.sequence'),
							}
						
	_sql_constraints = [
		    ('sequence_bulan_unik', 'unique(sequence_id, tahun, bulan_id)', 'Hanya boleh ada satu sequence tiap bulannya !'),
	]  							
							


			

sequence_bulan()




