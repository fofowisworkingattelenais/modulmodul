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
from tools.safe_eval import safe_eval as eval


class detail_ketentuan_cuti(osv.osv):
	_name = 'hr.detail_ketentuan_cuti'
	_description = 'Detail Ketentuan Absensi'
	
	def function_jumlah_digunakan(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_detail = self.pool.get('hr.detail_ketentuan_cuti')
		
		for detail in obj_detail.browse(cr, uid, ids):
			jumlah = 0
			if detail.cuti_kerja_ids:
				for cuti in detail.cuti_kerja_ids:
					if cuti.tanggal_mulai == cuti.tanggal_akhir:
						jumlah += 1
					else:
						dt_tanggal_mulai = date(int(cuti.tanggal_mulai[0:4]), int(cuti.tanggal_mulai[5:7]), int(cuti.tanggal_mulai[8:10]))
						dt_tanggal_akhir = date(int(cuti.tanggal_akhir[0:4]), int(cuti.tanggal_akhir[5:7]), int(cuti.tanggal_akhir[8:10]))
						ord_tanggal_mulai = dt_tanggal_mulai.toordinal()
						ord_tanggal_akhir = dt_tanggal_akhir.toordinal()
						jumlah += 1 + (ord_tanggal_akhir-ord_tanggal_mulai)
			res[detail.id] = jumlah
			
		return res

	_columns = 	{
				'ketentuan_cuti_id' : fields.many2one(obj='hr.ketentuan_cuti', string='Ketentuan Cuti'),
				'kode_absen_id' : fields.many2one(obj='hr.kode_absen', string='Jenis Cuti', required=True, domain=[('jenis_absen_id.tipe','=','cuti')]),
				'jumlah_diperbolehkan' : fields.integer(string='Jumlah Diperbolehkan'),
				'jumlah_digunakan' : fields.function(fnct=function_jumlah_digunakan, type='integer', string='Jumlah Digunakan', method=True, store=False),
				'cuti_kerja_ids' : fields.one2many(obj='hr.cuti_kerja', fields_id='detail_ketentuan_cuti_id', string='Cuti Kerja', readonly=True),
				}


detail_ketentuan_cuti()


