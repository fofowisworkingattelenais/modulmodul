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


class detail_form_1721_a(osv.osv):
	_name = 'hr.detail_form_1721_a'
	_description = 'Detail SPT Tahunan 1721-A'


	_columns = 	{
				'form_1721_a_id' : fields.many2one(obj='hr.form_1721_a', string='Form 1721-A'),
				'karyawan_id' : fields.many2one(obj='hr.employee', string='Karyawan', required=True),
				'npwp' : fields.char(string='NPWP', size=30, required=True),
				'penghasilan_bruto' : fields.float(string='Penghasilan Bruto', digits=(16,2), required=True),
				'pph_21_terutang' : fields.float(string='PPH 21 Terutang', digits=(16,2), required=True),
				'pph_ditanggung_pemerintah' : fields.float(string='PPH 21 Ditanggung pemerintah', digits=(16,2), required=True),
				}


detail_form_1721_a()
