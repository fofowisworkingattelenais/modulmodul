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
import pooler

	

class hr_payslip(osv.osv):
	_name = 'hr.payslip'
	_inherit = 'hr.payslip'
					
		
	def function_masa_pajak_id(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_masa_pajak = self.pool.get('pajak.masa_pajak')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			masa_pajak_ = False
			
			masa_pajak_ids = obj_masa_pajak.find(cr, uid, payslip.date_to, context)
			
			if masa_pajak_ids:
				masa_pajak_id = masa_pajak_ids[0]
				
			res[payslip.id] = masa_pajak_id
			
		return res
		
	def function_tahun_pajak_id(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			tahun_pajak_id = False
			if payslip.masa_pajak_id:
				tahun_pajak_id = payslip.masa_pajak_id.tahun_pajak_id.id
			res[payslip.id] = tahun_pajak_id		
				
		return res	

		
	def function_jumlah_bulan(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_masa_pajak = self.pool.get('pajak.masa_pajak')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			hasil = 0.0
			if payslip.masa_pajak_id:
				masa_pajak_ids = obj_masa_pajak.masa_pajak_sebelum(cr, uid, payslip.masa_pajak_id.id)
				if masa_pajak_ids:
					hasil += len(masa_pajak_ids)
			res[payslip.id] = hasil + 1.00		
				
		return res
		
	def function_total_thp(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = payslip.total_pendapatan_teratur + payslip.total_pendapatan_tidak_teratur + payslip.total_tunjangan_pph - payslip.total_potongan - payslip.total_asuransi - payslip.total_pensiun - payslip.total_pph
			
		return res
		
	def function_total_pendapatan_teratur(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			hasil = 0.0
			if payslip.detail_pendapatan_teratur_ids:
				for pendapatan_teratur in payslip.detail_pendapatan_teratur_ids:
					hasil += pendapatan_teratur.total
			res[payslip.id] = hasil
			
		return res
		
	def function_total_pendapatan_tidak_teratur(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			hasil = 0.0
			if payslip.detail_pendapatan_tidak_teratur_ids:
				for pendapatan_tidak_teratur in payslip.detail_pendapatan_tidak_teratur_ids:
					hasil += pendapatan_tidak_teratur.total
			res[payslip.id] = hasil
			
		return res		
		
	def function_total_asuransi(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			hasil = 0.0
			if payslip.detail_asuransi_ids:
				for asuransi in payslip.detail_asuransi_ids:
					hasil += asuransi.total
			res[payslip.id] = hasil
			
		return res	
		
	def function_total_pensiun(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			hasil = 0.0
			if payslip.detail_pensiun_ids:
				for pensiun in payslip.detail_pensiun_ids:
					hasil += pensiun.total
			res[payslip.id] = hasil
			
		return res
	
		
	def function_slip_sebelum_ids(self, cr, uid, ids, field_name, args, context=None):					

		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = []
			kriteria = [('employee_id','=',payslip.employee_id.id),('tanggal_slip','<=',payslip.tanggal_slip),('id','!=',payslip.id)]
			slip_ids = obj_payslip.search(cr, uid, kriteria)
			if slip_ids:
				for slip in obj_payslip.browse(cr, uid, slip_ids):
					res[payslip.id].append(slip.id)

		return res
		
	def function_total_pph(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.employee_id.tipe_pph == 'gross_up':
				res[payslip.id] = payslip.total_pph_gross_up
			else:
				res[payslip.id] = payslip.total_pph_non_gross_up
			
		return res
		
	def function_total_tunjangan_pph(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.employee_id.tipe_pph == 'gross_up':
				res[payslip.id] = payslip.total_pph_non_gross_up
			else:
				res[payslip.id] = 0.00
			
		return res					
		
	def function_total_pph_gross_up(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.perhitungan_pph_teratur_gross_up_ids:
				res[payslip.id] += payslip.perhitungan_pph_teratur_gross_up_ids[len(payslip.perhitungan_pph_teratur_gross_up_ids)-1].total
			
		return res
		
	def function_total_pph_non_gross_up(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		obj_payslip_line = self.pool.get('hr.payslip.line')
		obj_user = self.pool.get('res.users')
		
		user = obj_user.browse(cr, uid, [uid])[0]
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = 0.0
			if payslip.perhitungan_pph_teratur_ids:

				res[payslip.id] += payslip.perhitungan_pph_teratur_ids[len(payslip.perhitungan_pph_teratur_ids)-1].total
			
		return res
		
	def function_total_thp(self, cr, uid, ids, field_name, args, context=None):					
		res = {}
		obj_payslip = self.pool.get('hr.payslip')
		
		for payslip in obj_payslip.browse(cr, uid, ids):
			res[payslip.id] = payslip.total_pendapatan_teratur + payslip.total_pendapatan_tidak_teratur  + payslip.total_tunjangan_pph - payslip.total_potongan - payslip.total_asuransi - payslip.total_pensiun - payslip.total_pph + payslip.total_potongan_perusahaan + payslip.total_asuransi_perusahaan + payslip.total_pensiun_perusahaan
			
		return res																								
		
								
											
		
				
			

	_columns =	{
				'total_thp' : fields.function(fnct=function_total_thp, string='Total THP', type='float', digits=(16,2), method=True, store=False),
				'masa_pajak_id': fields.function(function_masa_pajak_id, method=True, store=True, type='many2one', relation='pajak.masa_pajak', string='Masa Pajak'),
				'tahun_pajak_id': fields.function(function_tahun_pajak_id, method=True, type='many2one', relation='pajak.tahun_pajak', string='Tahun Pajak'),
				'jumlah_bulan': fields.function(function_jumlah_bulan, method=True, type='float', string='Jumlah Bulan'),
				'perhitungan_pph_teratur_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Perhitungan PPH Pendapatan Teratur', readonly=True, domain=[('category_id.parent_id.code', '=', 'PPH21A')], states={'draft':[('readonly',False)]}),
				'perhitungan_pph_tidak_teratur_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Perhitungan PPH Pendapatan Teratur + Tidak Teratur', domain=[('category_id.parent_id.code', '=', 'PPH21B')], readonly=True, states={'draft':[('readonly',False)]}),						
				'perhitungan_pph_teratur_gross_up_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Perhitungan Gross-Up PPH Pendapatan Teratur', domain=[('category_id.parent_id.code', '=', 'PPH21B')], readonly=True, states={'draft':[('readonly',False)]}),
				'perhitungan_pph_tidak_teratur_gross_up_ids': fields.one2many('hr.payslip.line', 'slip_id', 'Perhitungan Gross-Up PPH Pendapatan Teratur + Tidak Teratur', domain=[('category_id.parent_id.code', '=', 'PPH21D')], readonly=True, states={'draft':[('readonly',False)]}),						
				
				
				'total_asuransi': fields.function(function_total_asuransi, method=True, type='float', string='Total Asuransi'),
				'total_pensiun': fields.function(function_total_pensiun, method=True, type='float', string='Total Pensiun'),
				'total_thp' : fields.function(fnct=function_total_thp, string='Total THP', type='float', digits=(16,2), method=True, store=False),

				
				# Pendapatan teratur
				'total_pendapatan_teratur': fields.function(function_total_pendapatan_teratur, method=True, type='float', string='Total Pendapatan Teratur'),

				# Pendapatan Tidak Teratur	
				'total_pendapatan_tidak_teratur': fields.function(function_total_pendapatan_tidak_teratur, method=True, type='float', string='Total Pendapatan Tidak Teratur'),
				
				'total_pph': fields.function(function_total_pph, method=True, type='float', string='Total PPH'),
				'total_tunjangan_pph': fields.function(function_total_tunjangan_pph, method=True, type='float', string='Total Tunjangan PPH'),
				'total_pph_non_gross_up': fields.function(function_total_pph_non_gross_up, method=True, type='float', string='Total PPH Non Gross-Up'),				
				'total_pph_gross_up': fields.function(function_total_pph_gross_up, method=True, type='float', string='Total PPH Gross-Up'),

				
				'slip_sebelum_ids' : fields.function(function_slip_sebelum_ids, method=True, type='many2many', string='Slip Gaji Sebelum', relation='hr.payslip'),
				}

	def list_perhitungan_pph_non_gross_up_rule(self, cr, uid, payslip_id):
		"""
		Mengembalikan list dari salary rule untuk perhitungan pph non gross-up
		"""
		obj_payslip = self.pool.get('hr.payslip')
		
		payslip = obj_payslip.browse(cr, uid, [payslip_id])[0]
		
		a = []
		
		# Ambil perhitungan PPH 21 dari struktur gaji kontrak
		if payslip.contract_id.struct_id.perhitungan_pph_non_gross_up_ids:
			for pph in payslip.contract_id.struct_id.perhitungan_pph_non_gross_up_ids:
				a.append((pph.id, pph.sequence, False))
				
		#TODO: Tambahkan tambahkan perhitungan PPH 21 Non Gross-Up dari history aktif
			
		
		return a

		
	def list_perhitungan_pph_gross_up_rule(self, cr, uid, payslip_id):
		"""
		Mengembalikan list dari salary rule untuk perhitungan pph untuk pendapatan teratur gross-up
		"""
		obj_payslip = self.pool.get('hr.payslip')
		
		payslip = obj_payslip.browse(cr, uid, [payslip_id])[0]
		
		a = []
		
		if payslip.contract_id.struct_id.perhitungan_pph_gross_up_ids:
			for pph in payslip.contract_id.struct_id.perhitungan_pph_gross_up_ids:
				a.append((pph.id, pph.sequence, False))
				
		#TODO: Tambahkan tambahkan perhitungan PPH 21 Non Gross-Up dari history aktif
			
		return a
											
		
	def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, context):
		def _sum_salary_rule_category(localdict, category, amount):
		    if category.parent_id:
		        localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
		    localdict['categories'].dict[category.code] = category.code in localdict['categories'].dict and localdict['categories'].dict[category.code] + amount or amount
		    return localdict

		class BrowsableObject(object):
		    def __init__(self, pool, cr, uid, employee_id, dict):
		        self.pool = pool
		        self.cr = cr
		        self.uid = uid
		        self.employee_id = employee_id
		        self.dict = dict

		    def __getattr__(self, attr):
		        return attr in self.dict and self.dict.__getitem__(attr) or 0.0

		class InputLine(BrowsableObject):
		    """a class that will be used into the python code, mainly for usability purposes"""
		    def sum(self, code, from_date, to_date=None):
		        if to_date is None:
		            to_date = datetime.now().strftime('%Y-%m-%d')
		        result = 0.0
		        self.cr.execute("SELECT sum(amount) as sum\
		                    FROM hr_payslip as hp, hr_payslip_input as pi \
		                    WHERE hp.employee_id = %s AND hp.state = 'done' \
		                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
		                   (self.employee_id, from_date, to_date, code))
		        res = self.cr.fetchone()[0]
		        return res or 0.0

		class WorkedDays(BrowsableObject):
		    """a class that will be used into the python code, mainly for usability purposes"""
		    def _sum(self, code, from_date, to_date=None):
		        if to_date is None:
		            to_date = datetime.now().strftime('%Y-%m-%d')
		        result = 0.0
		        self.cr.execute("SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours\
		                    FROM hr_payslip as hp, hr_payslip_worked_days as pi \
		                    WHERE hp.employee_id = %s AND hp.state = 'done'\
		                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
		                   (self.employee_id, from_date, to_date, code))
		        return self.cr.fetchone()

		    def sum(self, code, from_date, to_date=None):
		        res = self._sum(code, from_date, to_date)
		        return res and res[0] or 0.0

		    def sum_hours(self, code, from_date, to_date=None):
		        res = self._sum(code, from_date, to_date)
		        return res and res[1] or 0.0

		class Payslips(BrowsableObject):
		    """a class that will be used into the python code, mainly for usability purposes"""

		    def sum(self, code, from_date, to_date=None):
		        if to_date is None:
		            to_date = datetime.now().strftime('%Y-%m-%d')
		        self.cr.execute("SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)\
		                    FROM hr_payslip as hp, hr_payslip_line as pl \
		                    WHERE hp.employee_id = %s AND hp.state = 'done' \
		                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s",
		                    (self.employee_id, from_date, to_date, code))
		        res = self.cr.fetchone()
		        return res and res[0] or 0.0

		#we keep a dict with the result because a value can be overwritten by another rule with the same code
		result_dict = {}
		rules = {}
		categories_dict = {}
		blacklist = []
		payslip_obj = self.pool.get('hr.payslip')
		inputs_obj = self.pool.get('hr.payslip.worked_days')
		obj_rule = self.pool.get('hr.salary.rule')
		payslip = payslip_obj.browse(cr, uid, payslip_id, context=context)
		    
		inputs = {}
		for input_line in payslip.input_line_ids:
		    inputs[input_line.code] = input_line
			
			
		# Memasukan data rate karyawan ke dalam perhitungan slip gaji
		# Masukan rate pada struktur dulu kemudian append/update dengan rate pada history
		rate_karyawan = {}
		
		if payslip.struct_id.rate_structure_ids:
			for rate_struktur in payslip.struct_id.rate_structure_ids:
				rate_karyawan[rate_struktur.jenis_rate_id.kode] = rate_struktur

		if payslip.contract_id.rate_karyawan_ids:		
			for rate_line in payslip.contract_id.rate_karyawan_ids:
				rate_karyawan[rate_line.jenis_rate_id.kode] = rate_line

		# Instanisasi object yang dapat digunakan sebagai formula dalam perhitungan gaji
		categories_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, categories_dict)
		input_obj = InputLine(self.pool, cr, uid, payslip.employee_id.id, inputs)		
		payslip_obj = Payslips(self.pool, cr, uid, payslip.employee_id.id, payslip)
		rules_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, rules)
		rate_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, rate_karyawan)
		
		localdict = {'categories': categories_obj, 'rules': rules_obj, 'payslip': payslip_obj,  'inputs': input_obj, 'rate' : rate_obj}

		structure_ids = self.pool.get('hr.contract').get_all_structures(cr, uid, contract_ids, context=context)

		rule_ids = self.list_jadwal_penggajian(cr, uid, payslip.id)
		rule_ids += self.list_perhitungan_pph_non_gross_up_rule(cr, uid, payslip.id)

		if payslip.employee_id.tipe_pph == 'gross_up':
			rule_ids += self.list_perhitungan_pph_gross_up_rule(cr, uid, payslip.id)

		
		# Membuat dict
		dict_rule_run = {}
		for b in rule_ids:
		    dict_rule_run[b[0]] = b[2]  
		
		
		#run the rules by sequence
		sorted_rule_ids = [id for id, sequence, d in sorted(rule_ids, key=lambda x:x[1])]

		
		localdict.update({'pool' : self.pool, 'uid' : uid, 'cr' : cr})

		for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
		    employee = contract.employee_id
		    localdict.update({'employee': employee, 'contract': contract})
		    for rule in obj_rule.browse(cr, uid, sorted_rule_ids, context=context):
		        #kode asli 
		        #key = rule.code + '-' + str(contract.id)
		        
		        key = rule.id
		        
		        localdict['result'] = None
		        localdict['result_qty'] = 1.0
		        #check if the rule can be applied
		        if obj_rule.satisfy_condition(cr, uid, rule.id, localdict, context=context) and rule.id not in blacklist:
		            #compute the amount of the rule
		            amount, qty, rate = obj_rule.compute_rule(cr, uid, rule.id, localdict, context=context)
		            #check if there is already a rule computed with that code
		            previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
		            #set/overwrite the amount computed for this rule in the localdict
		            tot_rule = amount * qty * rate / 100.0
		            localdict[rule.code] = tot_rule
		            rules[rule.code] = rule
		            #sum the amount for its salary category
		            localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
		            #create/overwrite the rule in the temporary results
		            result_dict[key] = {
		                'salary_rule_id': rule.id,
		                'contract_id': contract.id,
		                'name': rule.name,
		                'code': rule.code,
		                'category_id': rule.category_id.id,
		                'sequence': rule.sequence,
		                'appears_on_payslip': rule.appears_on_payslip,
		                'condition_select': rule.condition_select,
		                'condition_python': rule.condition_python,
		                'condition_range': rule.condition_range,
		                'condition_range_min': rule.condition_range_min,
		                'condition_range_max': rule.condition_range_max,
		                'amount_select': rule.amount_select,
		                'amount_fix': rule.amount_fix,
		                'amount_python_compute': rule.amount_python_compute,
		                'amount_percentage': rule.amount_percentage,
		                'amount_percentage_base': rule.amount_percentage_base,
		                'register_id': rule.register_id.id,
		                'amount': amount,
		                'employee_id': contract.employee_id.id,
		                'quantity': qty,
		                'rate': rate,
		                'eksekusi_penggajian_id' : dict_rule_run[key],
		            }
		        else:
		            #blacklist this rule and its children
		            blacklist += [id for id, seq in self.pool.get('hr.salary.rule')._recursive_search_of_rules(cr, uid, [rule], context=context)]

		result = [value for code, value in result_dict.items()]
		return result
	


hr_payslip()




