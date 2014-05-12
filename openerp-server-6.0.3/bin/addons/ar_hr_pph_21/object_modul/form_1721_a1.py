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


class form_1721_a1(osv.osv):
	_name = 'hr.form_1721_a1'
	_description = 'SPT Masa 1721-A1'
	
	def default_state(self, cr, uid, context={}):
		return 'draft'

	_columns = 	{
				'name' : fields.char(string='#SPT', size=30, required=True),
				'npwp_pemotong_pajak' : fields.char(string='NPWP Pemotong Pajak', size=30, required=True),
				'nama_pemotong_pajak' : fields.char(string='Nama Pemotong Pajak', size=100, required=True),
				'npwp_wajib_pajak' : fields.char(string='NPWP Wajib Pajak', size=30, required=True),
				'nama_wajib_pajak' : fields.char(string='Nama Wajib Pajak', size=100, required=True),
				'alamat_wajib_pajak' : fields.char(string='Alamat Wajib Pajak', size=255, required=True),
				'jabatan_id' : fields.many2one(string='Jabatan', obj='hr.job', required=True),
				'masa_pajak_mulai_id' : fields.many2one(string='Masa Pajak Mulai', obj='pajak.masa_pajak', required=True),
				'masa_pajak_akhir_id' : fields.many2one(string='Masa Pajak Akhir', obj='pajak.masa_pajak', required=True),
				'item_a_1' : fields.float(string='1. GAJI / PENSIUN ATAU THT / JHT', digits=(16,2)),
				'item_a_2' : fields.float(string='2. TUNJANGAN PPh', digits=(16,2)),
				'item_a_3' : fields.float(string='3. TUNJANGAN LAINNYA, UANG LEMBUR, DAN SEBAGAINYA', digits=(16,2)),
				'item_a_4' : fields.float(string='4. HONORARIUM DAN IMBALAN LAIN SEJENISNYA', digits=(16,2)),
				'item_a_5' : fields.float(string='5. PREMI ASURANSI YANG DIBAYAR PEMBERI KERJA', digits=(16,2)),
				'item_a_6' : fields.float(string='6. PENERIMAAN DALAM BENTUK NATURA DAN KENIKMATAN LAINNYA YANG DIKENAKAN PEMOTONGAN PPh PASAL 21', digits=(16,2)),
				'item_a_7' : fields.float(string='7. JUMLAH (1 s.d. 6)', digits=(16,2)),
				'item_a_8' : fields.float(string='8. TANTIEM, BONUS, GRATIFIKASI, JASA PRODUKSI, DAN THR', digits=(16,2)),
				'item_a_9' : fields.float(string='9. JUMLAH PENGHASILAN BRUTO (7 + 8)', digits=(16,2)),
				'item_a_10' : fields.float(string='10. BIAYA JABATAN / BIAYA PENSIUN ATAS PENGHASILAN PADA ANGKA 7', digits=(16,2)),
				'item_a_11' : fields.float(string='11. BIAYA JABATAN / BIAYA PENSIUN ATAS PENGHASILAN PADA ANGKA 8', digits=(16,2)),
				'item_a_12' : fields.float(string='12. IURAN PENSIUN ATAU IURAN THT/ JHT', digits=(16,2)),
				'item_a_13' : fields.float(string='13. JUMLAH PENGURANGAN (10 + 11 + 12)', digits=(16,2)),
				'item_a_14' : fields.float(string='14. JUMLAH PENGHASILAN NETO (9 - 13)', digits=(16,2)),
				'item_a_15' : fields.float(string='15. PENGHASILAN NETO MASA SEBELUMNYA', digits=(16,2)),
				'item_a_16' : fields.float(string='16. JUMLAH PENGHASILAN NETO UNTUK PENGHITUNGAN PPh PASAL 21 (SETAHUN/DISETAHUNKAN)', digits=(16,2)),
				'item_a_17' : fields.float(string='17. PENGHASILAN TIDAK KENA PAJAK (PTKP)', digits=(16,2)),
				'item_a_18' : fields.float(string='18. PENGHASILAN KENA PAJAK SETAHUN / DISETAHUNKAN (16 - 17)', digits=(16,2)),
				'item_a_19' : fields.float(string='19. PPh PASAL 21 ATAS PENGHASILAN KENA PAJAK SETAHUN/DISETAHUNKAN', digits=(16,2)),
				'item_a_20' : fields.float(string='20. PPh PASAL 21 YANG TELAH DIPOTONG MASA SEBELUMNYA', digits=(16,2)),
				'item_a_21' : fields.float(string='21. PPh PASAL 21 TERUTANG', digits=(16,2)),
				'item_a_22' : fields.float(string='22. PPh PASAL 21 DAN PPh PASAL 26 YANG TELAH DIPOTONG DAN DILUNASI', digits=(16,2)),
				'item_a_22a' : fields.float(string='22. PPh PASAL 21 DAN PPh PASAL 26 YANG TELAH DIPOTONG DAN DILUNASI', digits=(16,2)),
				'item_a_22b' : fields.float(string='22. PPh PASAL 21 DAN PPh PASAL 26 YANG TELAH DIPOTONG DAN DILUNASI', digits=(16,2)),
				'item_a_23' : fields.float(string='23. JUMLAH PPh PASAL 21', digits=(16,2)),
				'item_a_23a' : fields.boolean(string='23a.YANG KURANG DIPOTONG (21 - 22)'),
				'item_a_23b' : fields.boolean(string='23b.YANG LEBIH DIPOTONG (22 - 21)'),
				'item_a_24' : fields.float(string='JUMLAH TERSEBUT PADA ANGKA 23 TELAH', digits=(16,2)),
				'item_a_24a' : fields.boolean(string='24a. DIPOTONG DARI PEMBAYARAN GAJI'),
				'item_a_24a_masa_pajak_id' : fields.many2one(obj='pajak.masa_pajak', string='Masa Pajak'),
				'item_a_24b' : fields.boolean(string='24b. DIPERHITUNGKAN DENGAN PPh PASAL 21'),
				'item_a_24b_masa_pajak_id' : fields.many2one(obj='pajak.masa_pajak', string='Masa Pajak'),
				'pernyataan' : fields.selection(selection=[('pemotong','Pemotong Pajak'),('kuasa','Kuasa Wajib Pajak')], string='Pernyataan', required=True),
				'nama_pemotong' : fields.char(string='Nama', size=100, required=True),
				'npwp_pemotong' : fields.char(string='NPWP', size=30, required=True),
				'tanggal_pemotong' : fields.date(string='Tanggal', required=True),
				
				'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'),('batal','Batal')], string='Status', required=True, readonly=True),				
				}

	_defaults =	{
				'state' : default_state,
				}

form_1721_a1()
