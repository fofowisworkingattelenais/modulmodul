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


class form_1721_induk(osv.osv):
	_name = 'hr.form_1721_induk'
	_description = 'Formulir 1721 Induk'
	
	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def function_karyawan_tetap(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_form = self.pool.get('hr.form_1721_induk')
		for form in obj_form.browse(cr, uid, ids):
			res[form.id] = 	{
							'jumlah_penerima_penghasilan_6' : 0,
							'jumlah_penghasilan_bruto_6' : 0.0,
							'jumlah_pajak_terutang_6' : 0.0,
							}
			jumlah_karyawan_tetap = 0
			penghasilan = 0.00
			pph = 0.00
			karyawan_tetap = []
			if form.payslip_ids:
				for payslip in form.payslip_ids:
					if payslip.employee_id.status_karyawan == 'tetap':
						if payslip.employee_id.id not in karyawan_tetap:
							karyawan_tetap.append(payslip.employee_id.id)
							jumlah_karyawan_tetap += 1
						pph += payslip.total_pph
						penghasilan += payslip.total_pendapatan_teratur + payslip.total_pendapatan_tidak_teratur + payslip.total_asuransi
			res[form.id]['jumlah_penerima_penghasilan_6'] = jumlah_karyawan_tetap
			res[form.id]['jumlah_penghasilan_bruto_6'] = penghasilan
			res[form.id]['jumlah_pajak_terutang_6'] = pph
		return res
		
	def function_karyawan_tidak_tetap(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_form = self.pool.get('hr.form_1721_induk')
		for form in obj_form.browse(cr, uid, ids):
			res[form.id] = 	{
							'jumlah_penerima_penghasilan_8' : 0,
							'jumlah_penghasilan_bruto_8' : 0.0,
							'jumlah_pajak_terutang_8' : 0.0,
							}
			jumlah_karyawan = 0
			penghasilan = 0.00
			pph = 0.00
			karyawan = []
			if form.payslip_ids:
				for payslip in form.payslip_ids:
					if payslip.employee_id.status_karyawan == 'kontrak':
						if payslip.employee_id.id not in karyawan:
							karyawan.append(payslip.employee_id.id)
							jumlah_karyawan += 1
						pph += payslip.total_pph
						penghasilan += payslip.total_pendapatan_teratur + payslip.total_pendapatan_tidak_teratur + payslip.total_asuransi
			res[form.id]['jumlah_penerima_penghasilan_8'] = jumlah_karyawan
			res[form.id]['jumlah_penghasilan_bruto_8'] = penghasilan
			res[form.id]['jumlah_pajak_terutang_8'] = pph
		return res	
		
	def function_jumlah_pendapatan(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_form = self.pool.get('hr.form_1721_induk')
		for form in obj_form.browse(cr, uid, ids):
			res[form.id] = 	{
							'jumlah_penerima_penghasilan' : 0,
							'jumlah_penghasilan_bruto' : 0.0,
							'jumlah_pajak_terutang' : 0.0,
							}		
			res[form.id]['jumlah_penerima_penghasilan'] = form.jumlah_penerima_penghasilan_6 + form.jumlah_penerima_penghasilan_7 + form.jumlah_penerima_penghasilan_8 + form.jumlah_penerima_penghasilan_9 + form.jumlah_penerima_penghasilan_10 + form.jumlah_penerima_penghasilan_11 + form.jumlah_penerima_penghasilan_12 + form.jumlah_penerima_penghasilan_13 + form.jumlah_penerima_penghasilan_14 + form.jumlah_penerima_penghasilan_15 + form.jumlah_penerima_penghasilan_16 + form.jumlah_penerima_penghasilan_17 + form.jumlah_penerima_penghasilan_18 + form.jumlah_penerima_penghasilan_19
			res[form.id]['jumlah_penghasilan_bruto'] = form.jumlah_penghasilan_bruto_6 + form.jumlah_penghasilan_bruto_7 + form.jumlah_penghasilan_bruto_8 + form.jumlah_penghasilan_bruto_9 + form.jumlah_penghasilan_bruto_10 + form.jumlah_penghasilan_bruto_11 + form.jumlah_penghasilan_bruto_12 + form.jumlah_penghasilan_bruto_13 + form.jumlah_penghasilan_bruto_14 + form.jumlah_penghasilan_bruto_15 + form.jumlah_penghasilan_bruto_16 + form.jumlah_penerima_penghasilan_17 + form.jumlah_penghasilan_bruto_18 + form.jumlah_penghasilan_bruto_19
			res[form.id]['jumlah_pajak_terutang'] = form.jumlah_pajak_terutang_6 + form.jumlah_pajak_terutang_7 + form.jumlah_pajak_terutang_8 + form.jumlah_pajak_terutang_9 + form.jumlah_pajak_terutang_10 + form.jumlah_pajak_terutang_11 + form.jumlah_pajak_terutang_12 + form.jumlah_pajak_terutang_13 + form.jumlah_pajak_terutang_14 + form.jumlah_pajak_terutang_15 + form.jumlah_pajak_terutang_16 + form.jumlah_penerima_penghasilan_17 + form.jumlah_pajak_terutang_18 + form.jumlah_pajak_terutang_19
		return res
		
	def function_item_24(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_form = self.pool.get('hr.form_1721_induk')
		for form in obj_form.browse(cr, uid, ids):
			res[form.id] = form.item_21 + form.item_22 + form.item_23
		return res
			

	_columns = 	{
				'name' : fields.char(string='# SPT', size=30, required=True),
				'jenis_spt' : fields.selection(selection=[('normal','Normal'),('pembetulan','Pembetulan')], string='Jenis SPT', required=True),
				'pembetulan_ke' : fields.integer(string='Pembetulan Ke'),
				'masa_pajak_id' : fields.many2one(obj='pajak.masa_pajak', string='Masa Pajak', required=True),
				'npwp' : fields.char(string='NPWP', size=30, required=True),
				'company_id' : fields.many2one(string='Perusahaan', obj='res.company', required=True),
				
				'jumlah_penerima_penghasilan_6' : fields.function(fnct=function_karyawan_tetap, type='integer', multi='item6', store=False, method=True, string='6. Pegawai Tetap'),
				'jumlah_penghasilan_bruto_6' : fields.function(fnct=function_karyawan_tetap, type='float', multi='item6', store=False, method=True, string='Pegawai Tetap', digits=(16,2)),
				'jumlah_pajak_terutang_6' : fields.function(fnct=function_karyawan_tetap, type='float', multi='item6', store=False, method=True, string='Pegawai Tetap', digits=(16,2)),
				
				'jumlah_penerima_penghasilan_7' : fields.integer(string='7. Penerima Penghasilan Berkala'),
				'jumlah_penghasilan_bruto_7' : fields.float(string='Penerima Penghasilan Berkala', digits=(16,2)),
				'jumlah_pajak_terutang_7' : fields.float(string='Penerima Penghasilan Berkala', digits=(16,2)),	
				
				'jumlah_penerima_penghasilan_8' : fields.function(fnct=function_karyawan_tidak_tetap, type='integer', multi='item8', store=False, method=True, string='8. Pegawai Tidak Tetap'),
				'jumlah_penghasilan_bruto_8' : fields.function(fnct=function_karyawan_tidak_tetap, type='float', multi='item8', store=False, method=True, string='Pegawai Tidak Tetap', digits=(16,2)),
				'jumlah_pajak_terutang_8' : fields.function(fnct=function_karyawan_tidak_tetap, type='float', multi='item8', store=False, method=True, string='Pegawai Tidak Tetap', digits=(16,2)),	
				
				'jumlah_penerima_penghasilan_9' : fields.integer(string='9. Distribusi MLM'),
				'jumlah_penghasilan_bruto_9' : fields.float(string='Distribusi MLM', digits=(16,2)),
				'jumlah_pajak_terutang_9' : fields.float(string='Distribusi MLM', digits=(16,2)),
				
				'jumlah_penerima_penghasilan_10' : fields.integer(string='10. Petugas Dinas Luar Asuransi'),
				'jumlah_penghasilan_bruto_10' : fields.float(string='Petugas Dinas Luar Asuransi', digits=(16,2)),
				'jumlah_pajak_terutang_10' : fields.float(string='Petugas Dinas Luar Asuransi', digits=(16,2)),	
				
				'jumlah_penerima_penghasilan_11' : fields.integer(string='11. Penjaja Barang dagangan'),
				'jumlah_penghasilan_bruto_11' : fields.float(string='Penjaja Barang dagangan', digits=(16,2)),
				'jumlah_pajak_terutang_11' : fields.float(string='Penjaja Barang dagangan', digits=(16,2)),																		
				
				'jumlah_penerima_penghasilan_12' : fields.integer(string='12. Tenaga Ahli'),
				'jumlah_penghasilan_bruto_12' : fields.float(string='Tenaga Ahli', digits=(16,2)),
				'jumlah_pajak_terutang_12' : fields.float(string='Tenaga Ahli', digits=(16,2)),					
				
				'jumlah_penerima_penghasilan_13' : fields.integer(string='13. Anggota Dewan Komisaris'),
				'jumlah_penghasilan_bruto_13' : fields.float(string='Anggota Dewan Komisaris', digits=(16,2)),
				'jumlah_pajak_terutang_13' : fields.float(string='Anggota Dewan Komisaris', digits=(16,2)),					
				
				'jumlah_penerima_penghasilan_14' : fields.integer(string='14. Mantan Pegawai'),
				'jumlah_penghasilan_bruto_14' : fields.float(string='Mantan Pegawai', digits=(16,2)),
				'jumlah_pajak_terutang_14' : fields.float(string='Mantan Pegawai', digits=(16,2)),	
				
				'jumlah_penerima_penghasilan_15' : fields.integer(string='15. Pegawai Yang Melakukan Penarikan Dana Pensiun'),
				'jumlah_penghasilan_bruto_15' : fields.float(string='Pegawai Yang Melakukan Penarikan Dana Pensiun', digits=(16,2)),
				'jumlah_pajak_terutang_15' : fields.float(string='Pegawai Yang Melakukan Penarikan Dana Pensiun', digits=(16,2)),									
				
				'jumlah_penerima_penghasilan_16' : fields.integer(string='16. Peserta Kegiatan'),
				'jumlah_penghasilan_bruto_16' : fields.float(string='Peserta Kegiatan', digits=(16,2)),
				'jumlah_pajak_terutang_16' : fields.float(string='Peserta Kegiatan', digits=(16,2)),					
				
				'jumlah_penerima_penghasilan_17' : fields.integer(string='17. Bukan Pegawai yang Menerima Penghasilan yang Bersifat Berkesinambungan'),
				'jumlah_penghasilan_bruto_17' : fields.float(string='Bukan Pegawai yang Menerima Penghasilan yang Bersifat Berkesinambungan', digits=(16,2)),
				'jumlah_pajak_terutang_17' : fields.float(string='Bukan Pegawai yang Menerima Penghasilan yang Bersifat Berkesinambungan', digits=(16,2)),					
				
				'jumlah_penerima_penghasilan_18' : fields.integer(string='18. Bukan Pegawai yang Menerima Penghasilan yang Tidak Bersifat Berkesinambungan'),
				'jumlah_penghasilan_bruto_18' : fields.float(string='Bukan Pegawai yang Menerima Penghasilan yang Tidak Bersifat Berkesinambungan', digits=(16,2)),
				'jumlah_pajak_terutang_18' : fields.float(string='Bukan Pegawai yang Menerima Penghasilan yang Tidak Bersifat Berkesinambungan', digits=(16,2)),					
				
				'jumlah_penerima_penghasilan_19' : fields.integer(string='19. Pegawai atau Pemberi Jasa sebagai Wajib Pajak Luar Negeri'),
				'jumlah_penghasilan_bruto_19' : fields.float(string='Pegawai atau Pemberi Jasa sebagai Wajib Pajak Luar Negeri', digits=(16,2)),
				'jumlah_pajak_terutang_19' : fields.float(string='Pegawai atau Pemberi Jasa sebagai Wajib Pajak Luar Negeri', digits=(16,2)),	
				
				'jumlah_penerima_penghasilan' : fields.function(fnct=function_jumlah_pendapatan, type='integer', multi='jumlah', store=False, method=True, string='20. Jumlah'),
				'jumlah_penghasilan_bruto' : fields.function(fnct=function_jumlah_pendapatan, type='float', multi='jumlah', store=False, method=True, string='Jumlah', digits=(16,2)),
				'jumlah_pajak_terutang' : fields.function(fnct=function_jumlah_pendapatan, type='float', multi='jumlah', store=False, method=True, string='Jumlah', digits=(16,2)),									
				
				'item_21' : fields.float(string='21. PPH Jan S.D. Des', digits=(16,2)),	
				'item_22' : fields.float(string='22. STP PPH 21', digits=(16,2)),
				'item_23' : fields.float(string='23. Kelebihan Setor PPH 21 Dari Masa Pajak', digits=(16,2)),		
				'item_24' : fields.function(fnct=function_item_24, type='float', method=True, store=False, string='24. Jumlah (angka 21 + angka 22 + angka 23)', digits=(16,2)),
				
				'item_25' : fields.float(string='25. PPh Pasal 21 dan/atau Pasal 26 yang Kurang (Lebih) Disetor', digits=(16,2)),
				'item_25a' : fields.float(string='25a. Penyetoran dengan SSP PPh Pasal 21 Ditanggung Pemerintah ', digits=(16,2)),
				'item_25b' : fields.float(string='25b. Penyetoran dengan SSP ', digits=(16,2)),	
				
				'item_26' : fields.float(string='26. PPh Pasal 21 dan/atau Pasal 26 yang Kurang (Lebih) Disetor pada SPT yang Dibetulkan', digits=(16,2)),				
				'item_27' : fields.float(string='27. PPh Pasal 21 dan/atau Pasal 26 yang Kurang (Lebih) Disetor karena pembetulan', digits=(16,2)),	
				'item_28_masa_pajak_id' : fields.many2one(string='28. Masa Pajak', obj='pajak.masa_pajak'),
				
				'jumlah_penerima_penghasilan_29' : fields.integer(string='29. Penerima Uang Pesangon'),
				'jumlah_penghasilan_bruto_29' : fields.float(string='29. Penerima Uang Pesangon', digits=(16,2)),
				'jumlah_pajak_terutang_29' : fields.float(string='29. Penerima Uang Pesangon', digits=(16,2)),				
				
				'jumlah_penerima_penghasilan_30' : fields.integer(string='30. Pejabat Negara'),
				'jumlah_penghasilan_bruto_30' : fields.float(string='30. Pejabat Negara', digits=(16,2)),
				'jumlah_pajak_terutang_30' : fields.float(string='30. Pejabat Negara', digits=(16,2)),				
				
				'jumlah_penerima_penghasilan_31' : fields.integer(string='31. Jumlah Bagian C'),
				'jumlah_penghasilan_bruto_31' : fields.float(string='31. Jumlah Bagian C', digits=(16,2)),
				'jumlah_pajak_terutang_31' : fields.float(string='31. Jumlah Bagian C', digits=(16,2)),	
				
				'item_d_a' : fields.boolean(string='a. Surat Setoran Pajak'),
				'item_d_b' : fields.boolean(string='b. Surat Setoran Pajak PPh Pasal 21 DTP'),
				'item_d_c' : fields.boolean(string='c. Surat Kuasa Khusus/Surat Keterangan Kematian'),
				'item_d_d' : fields.boolean(string='d. Daftar Bukti Pemotongan Pajak Penghasilan Tidak Final'),
				'item_d_e' : fields.boolean(string='e. Daftar Bukti Pemotongan Pajak Penghasilan Final'),
				'item_d_f' : fields.boolean(string='f. Formulir 1721 – I'),
				'item_d_g' : fields.boolean(string='g. Formulir 1721 – II'),
				'item_d_h' : fields.boolean(string='h. Daftar Biaya untuk Wajib Pajak yang Tidak Wajib Menyampaikan SPT Tahunan PPh Badan'),
				'item_d_i' : fields.boolean(string='i. '),
				'item_d_i_keterangan' : fields.char(string='i. ', size=255),
				
				'pernyataan' : fields.selection(selection=[('pemotong','Pemotong Pajak'),('kuasa','Kuasa Wajib Pajak')], string='Pernyataan', required=True),
				'nama_pemotong' : fields.char(string='Nama', size=100, required=True),
				'npwp_pemotong' : fields.char(string='NPWP', size=30, required=True),
				'tanggal_pemotong' : fields.date(string='Tanggal', required=True),
				
				'payslip_ids' : fields.many2many(obj='hr.payslip', rel='rel_payslip_1721_induk', id1='payslip_id', id2='form1721_id', string='Slip Gaji'),
				
				'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'),('batal','Batal')], string='Status', required=True, readonly=True),
							
				}
				
	_defaults =	{
				'state' : default_state,
				}


form_1721_induk()
