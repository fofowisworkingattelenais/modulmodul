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
import netsvc

class hr_payslip(osv.osv):
	_name = 'hr.payslip'
	_inherit = 'hr.payslip'
			

	_columns =	{
				'timesheet_karyawan_id' : fields.many2one(obj='hr.timesheet_karyawan', string='Timesheet Karyawan', domain=[('id','=',False)]),
				'detail_periode_gaji_id' : fields.many2one('hr.detail_periode_gaji', 'Periode Gaji', required=True, domain=[('id','=',False)]),
				}
				
	def onchange_detail_periode_gaji_id(self, cr, uid, ids, employee_id, detail_periode_gaji_id):
		"""
		Method on_change untuk field detail_periode_gaji_id
		"""
		
		obj_timesheet = self.pool.get('hr.timesheet_karyawan')
		
		domain =	{
					'timesheet_karyawan_id' : [('id','=',False)],
					}
					
		value =	{
				'timesheet_karyawan_id' : False,
				}
				
		kriteria = [('employee_id','=',employee_id),('detail_periode_kerja_id','=',detail_periode_gaji_id)]
		timesheet_ids = obj_timesheet.search(cr, uid, kriteria)
		
		if timesheet_ids:
			domain['timesheet_karyawan_id'] = [('id','in',timesheet_ids)]

			
		return {'value' : value, 'domain' : domain}	
		
	def onchange_karyawan_id(self, cr, uid, ids, employee_id):
		"""
		Method on_change untuk field employee_id
		"""
		
		obj_karyawan = self.pool.get('hr.employee')
		obj_detail_periode_gaji = self.pool.get('hr.detail_periode_gaji')
		
		domain =	{
					'timesheet_karyawan_id' : [('id','=',False)],
					'detail_periode_gaji_id' : [('id','=',False)],
					}
					
		value =	{
				'timesheet_karyawan_id' : False,
				'detail_periode_gaji_id' : False,
				}
				
		karyawan = obj_karyawan.browse(cr, uid, [employee_id])[0]
		periode_gaji_id = karyawan.contract_id.periode_gaji_id.id
		
		kriteria = [('periode_gaji_id','=',periode_gaji_id)]
		detail_periode_gaji_ids = obj_detail_periode_gaji.search(cr, uid, kriteria)
		
		if detail_periode_gaji_ids:
			domain['detail_periode_gaji_id'] = [('id','in',detail_periode_gaji_ids)]

			
		return {'value' : value, 'domain' : domain}
		
	def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, context):
		"""
		Overloading untuk menambahkan perhitungan timesheet
		"""
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
				
				
		# Memasukan hasil perhitungan absensi
		absensi = {}
		if payslip.timesheet_karyawan_id:
			if payslip.timesheet_karyawan_id.perhitungan_timesheet_ids:
				for perhitungan in payslip.timesheet_karyawan_id.perhitungan_timesheet_ids:
					absensi[perhitungan.kode] = perhitungan.hasil
		

		# Instanisasi object yang dapat digunakan sebagai formula dalam perhitungan gaji
		categories_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, categories_dict)
		input_obj = InputLine(self.pool, cr, uid, payslip.employee_id.id, inputs)		
		payslip_obj = Payslips(self.pool, cr, uid, payslip.employee_id.id, payslip)
		rules_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, rules)
		rate_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, rate_karyawan)
		absensi_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, absensi)
		
		localdict = {'categories': categories_obj, 'rules': rules_obj, 'payslip': payslip_obj,  'inputs': input_obj, 'rate' : rate_obj, 'absensi' : absensi_obj}

		structure_ids = self.pool.get('hr.contract').get_all_structures(cr, uid, contract_ids, context=context)

		rule_ids = self.list_jadwal_penggajian(cr, uid, payslip.id)
		rule_ids += self.list_perhitungan_pph_teratur_rule(cr, uid, payslip.id)

		if payslip.employee_id.tipe_pph == 'gross_up':
			rule_ids += self.list_perhitungan_pph_teratur_gross_up_rule(cr, uid, payslip.id)

		
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
		            #raise osv.except_osv('a', dict_rule_run[key])
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




