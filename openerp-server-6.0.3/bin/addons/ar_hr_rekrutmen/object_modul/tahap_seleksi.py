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


class tahap_seleksi(osv.osv):
	_name = 'hr.tahap_seleksi'
	_description = 'Tahap Seleksi'
	_columns = 	{
				'proses_seleksi_id' : fields.many2one('hr.proses_seleksi', 'Proses Seleksi'),
				'seleksi_id' : fields.many2one('hr.seleksi', 'Seleksi', required=True),
				'urutan' : fields.integer('Urutan', required=True),
				}
				
tahap_seleksi()
