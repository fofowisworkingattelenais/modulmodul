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


class tarif_pph_21_non_npwp(osv.osv):
	_name = 'hr.tarif_pph_21_non_npwp'
	_description = 'Tarif PPH 21 Untuk Karyawan Non-NPWP'

		
	_columns = 	{
				'tahun_pajak_id' : fields.many2one(obj='pajak.tahun_pajak', string='Tahun Pajak', required=True),
				'dari_jumlah' : fields.float(string='Dari Jumlah', digits=(16,2), required=True),
				'sampai_jumlah' : fields.float(string='Sampai Jumlah', digits=(16,2), required=True),
				'tarif' : fields.float(string='Tarif (%)', digits=(16,2), required=True),
				'urutan' : fields.integer(string='Urutan', required=True),
				}


tarif_pph_21_non_npwp()
