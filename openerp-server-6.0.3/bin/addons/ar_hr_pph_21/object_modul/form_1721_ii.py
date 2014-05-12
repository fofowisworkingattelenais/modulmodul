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


class form_1721_ii(osv.osv):
	_name = 'hr.form_1721_ii'
	_description = 'SPT Massa 1721-II'


	_columns = 	{
				'name' : fields.char(string='# Internal', size=30, required=True),
				'masa_pajak_id' : fields.many2one(obj='pajak.masa_pajak', string='Masa Pajak', required=True),
				'keterangan' : fields.text(string='Keterangan'),
				'detail_keluar_form_1721_ii_ids' : fields.one2many(obj='hr.detail_keluar_form_1721_ii', fields_id='form_1721_ii_id', string='Pegawai Tetap Yang Keluar'),
				'detail_masuk_form_1721_ii_ids' : fields.one2many(obj='hr.detail_masuk_form_1721_ii', fields_id='form_1721_ii_id', string='Pegawai Tetap Yang Keluar'),
				'detail_npwp_form_1721_ii_ids' : fields.one2many(obj='hr.detail_npwp_form_1721_ii', fields_id='form_1721_ii_id', string='Pegawai Yang Baru Memiliki NPWP'),
				}


form_1721_ii()

class detail_keluar_form_1721_ii(osv.osv):
	_name = 'hr.detail_keluar_form_1721_ii'
	_description = 'Detail Pegawai Tetap Yang Keluar SPT Massa 1721-II'


	_columns = 	{
				'form_1721_ii_id' : fields.many2one(obj='hr.form_1721_ii', string='Form 1721-II'),
				'karyawan_id' : fields.many2one(obj='hr.employee', string='Nama Wajib Pajak', required=True),
				'npwp' : fields.char(string='NPWP', size=30, required=True),
				'penghasilan_bruto' : fields.float(string='Penghasilan Bruto', digits=(16,2), required=True),
				'pph_terutang' : fields.float(string='PPH 21 dan/atau 21 Terutang', digits=(16,2), required=True),
				}


detail_keluar_form_1721_ii()

class detail_masuk_form_1721_ii(osv.osv):
	_name = 'hr.detail_masuk_form_1721_ii'
	_description = 'Detail Pegawai Tetap Yang Masuk SPT Massa 1721-II'


	_columns = 	{
				'form_1721_ii_id' : fields.many2one(obj='hr.form_1721_ii', string='Form 1721-II'),
				'karyawan_id' : fields.many2one(obj='hr.employee', string='Nama Wajib Pajak', required=True),
				'npwp' : fields.char(string='NPWP', size=30, required=True),
				'jumlah_tanggungan' : fields.integer(string='Jumlah Tanggungan', required=True),
				}


detail_masuk_form_1721_ii()

class detail_npwp_form_1721_ii(osv.osv):
	_name = 'hr.detail_npwp_form_1721_ii'
	_description = 'Detail Pegawai Yang Baru Memiliki NPWP SPT Massa 1721-II'


	_columns = 	{
				'form_1721_ii_id' : fields.many2one(obj='hr.form_1721_ii', string='Form 1721-II'),
				'karyawan_id' : fields.many2one(obj='hr.employee', string='Nama Wajib Pajak', required=True),
				'npwp' : fields.char(string='NPWP', size=30, required=True),
				'tanggal_terdaftar' : fields.date(string='Tanggal Terdaftar', required=True),
				}


detail_npwp_form_1721_ii()
