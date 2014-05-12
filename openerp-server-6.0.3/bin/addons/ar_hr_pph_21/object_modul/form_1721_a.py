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


class form_1721_a(osv.osv):
	_name = 'hr.form_1721_a'
	_description = 'SPT Tahunan 1721-A'


	_columns = 	{
				'name' : fields.char(string='# Internal', size=30, required=True),
				'tahun_pajak_id' : fields.many2one(obj='pajak.tahun_pajak', string='Tahun Takwim', required=True),
				'npwp_pemotong_pajak' : fields.char(string='NPWP Pemotong Pajak', size=30, required=True),
				'nama_pemotong_pajak' : fields.char(string='Nama Pemotong Pajak', size=100, required=True),
				'keterangan' : fields.text(string='Keterangan'),
				'detail_form_1721_a_ids' : fields.one2many(obj='hr.detail_form_1721_a', fields_id='form_1721_a_id', string='Detail'),
				}


form_1721_a()
