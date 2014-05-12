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

class tahun_pajak(osv.osv):
	_name = 'pajak.tahun_pajak'
	_inherit = 'pajak.tahun_pajak'
	
	_columns =	{
				'tarif_biaya_jabatan' : fields.float(string='Tarif Biaya Jabatan (%)', digits=(16,2)),
				'max_biaya_jabatan' : fields.float(string='Maksimum Biaya Jabatan', digits=(16,2)),
				'tarif_pph21_npwp_ids' : fields.one2many(obj='hr.tarif_pph_21_npwp', fields_id='tahun_pajak_id', string='Tarif PPH 21 Karyawan NPWP'),
				'tarif_pph21_npwp_non_ids' : fields.one2many(obj='hr.tarif_pph_21_non_npwp', fields_id='tahun_pajak_id', string='Tarif PPH 21 Karyawan Non-NPWP'),
				}





tahun_pajak()




