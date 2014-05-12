# -*- coding: utf-8 -*-
##############################################################################
#
#   Kustomsiasi modul hr_contract  
#
##############################################################################

import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from array import array

import netsvc
from osv import fields, osv
import tools
from tools.translate import _
import decimal_precision as dp
import addons

import logging as log
"""
def prev_bounds(cdate=False):
    when = date.fromtimestamp(time.mktime(time.strptime(cdate,"%Y-%m-%d")))
    this_first = date(when.year, when.month, 1)
    month = when.month + 1
    year = when.year
    if month > 12:
        month = 1
        year += 1
    next_month = date(year, month, 1)
    prev_end = next_month - timedelta(days=1)
    #log.info("this_first=%s, prev_end=%s, next_month=%s" % (this_first, prev_end, next_month))
    return this_first, prev_end

#custom employee
"""
class payment_category(osv.osv):
    _inherit = "hr.allounce.deduction.categoty"
    _columns = {
        'base': fields.selection([
                ('basic','basic'),
                ('gaji_pokok','gaji pokok'),
                ('uang_makan','uang makan'),
                ('uang_transport','uang transport'),
                ('uang_lembur','uang lembur'),    
                ('iuran_premi_kk','iuran premi kec kerja'),
                ('iuran_premi_jk','iuran premi jam kematian'),
                ('premi_jht','premi jht'),            
                ('formula_pph','formula pph'),
                ('formula_pph21','formula pph21'),
        ],'Based on', required=True, readonly=False),                     
        'printable': fields.boolean('Printable', required=False, help='Dicetak pada payslip'),
    }
    _defaults = {
        'printable': lambda *a: True,
        'base': lambda *a: 'basic',
    }

payment_category()

class hr_payslip_line(osv.osv):
    _inherit = "hr.payslip.line"
    _columns = {
        'amount_type':fields.selection([
            ('per','Percentage (%)'),
            ('fix','Fixed Amount'),
            ('fix_daily','Fixed Daily'),
            ('fix_hourly','Fixed Hourly'),
            ('func','Function Value'),
        ],'Amount Type', select=True, required=True),        
        'multiplier1': fields.float('Multiplier 1', digits=(16, 4), required=False),
        'multiplier2': fields.float('Multiplier 2', digits=(16, 4), required=False),
        
    }
hr_payslip_line()
    
class hr_payslip(osv.osv):
    '''
    Custom Pay Slip
    '''
    _inherit = 'hr.payslip'
    #override
    def _calculate(self, cr, uid, ids, field_names, arg, context=None):
        #log.info("field_names=%s;arg=%s" % (field_names, arg))
        def calc_pph_progressive(cr, pkp):
            #hitung pph berdasarkan tarif progresif
            query = "SELECT tarif,pkp FROM hr_pph_tarif ORDER BY pkp "
            cr.execute(query)            
            _pkp = pkp
            _total = 0              
            for rec in cr.fetchall():
                rate_percent = rec[0]/100                
                rate_pkp = rec[1]                
                #log.info("_pkp=%s;_total=%s" % (_pkp, _total))
                if _pkp <= rate_pkp:
                    _total += _pkp * rate_percent 
                    break
                else:
                    _total += rate_pkp * rate_percent                    
                    _pkp -= rate_pkp
                
                #log.info("rate=%s" % (str(rate)))
            return _total
        
        def get_bruto_pph_total(cr, employee_id, year, max_month):
            res = 0.0
            try:        
                query = "SELECT SUM(a.basic + a.allounce + a.pph_allounce) \
                        FROM hr_payslip a \
                            WHERE a.employee_id = %s AND extract(year from a.date) = %s AND extract(month from a.date) <= %s " % (employee_id, year, max_month)
                #log.info("query=%s" % query)
                cr.execute(query)                
                record = cr.fetchall()             
                res = record[0][0]   
            except Exception, e:    
                raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % (e))
                                           
            return res
        
        def get_allow_deduct_intax_pph(cr, slip_id):
            res = {'allowance':0,'deduction':0}
            try:        
                query = "SELECT \
                            SUM(CASE WHEN a.base <> 'gaji_pokok' AND a.type = 'allowance' THEN a.total ELSE 0 END), \
                            SUM(CASE WHEN a.base <> 'gaji_pokok' AND a.type = 'deduction' THEN a.total ELSE 0 END) \
                        FROM hr_payslip_line a \
                            WHERE a.slip_id = %s AND a.base <> 'gaji_pokok' \
                            AND a.category_id in ( \
                                SELECT category_id FROM hr_pph_salary_head_pph_allow \
                            )" % (slip_id)
                cr.execute(query)                
                record = cr.fetchall()
                #tunjangan
                res['allowance'] = record[0][0]
                #deduction
                res['deduction'] = record[0][1]
            except Exception, e:    
                raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % (e))
                                           
            return res
        
        def get_occupy_expense(cr):
            res = {'rate':0.0,'max':0.0} 
            try:           
                query = "SELECT amount, maximum FROM hr_pph_occupy_expense"
                cr.execute(query)                
                record = cr.fetchall()
                res['rate'] = record[0][0]
                res['max'] = record[0][1]
            except Exception, e:    
                raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % (e))
              
            return res
        
        def get_prev_cumulative_pph(cr, slip_date_curr):
            res = 0
            #try:            
            slip_date = datetime.strptime(slip_date_curr, '%Y-%m-%d')
            if slip_date.month > 1:
                #log.info("slip_date.year=%s, slip_date.month - 1=%s, slip_date.day=%s" % (slip_date.year, slip_date.month - 1, slip_date.day))
                yearmon = date(slip_date.year, slip_date.month - 1, slip_date.day).strftime('%Y%m')
                query = "SELECT cumulative_pph FROM hr_payslip WHERE to_char(date,'YYYYMM') = '%s' " % yearmon
                #log.info("query=%s" % query)  
                cr.execute(query)
                record = cr.fetchall()
                if len(record) > 0:
                    res = record[0][0]                    
            #except Exception, e:    
            #    raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % (e))
              
            return res
                       
        def compute_pph_allow_normal(cr, slip):
            intax_allow = 0
            basic=0
            allowance = 0
            deduction = 0
            #try:
            #gaji pokok                
            basic = slip.employee_id.contract_id.wage            
            if basic <= 0:
                raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % ('basic salary undefined!'))
            
            #get allow & deduction
            allowdeduct = get_allow_deduct_intax_pph(cr, slip.id)
            #tunjangan                 
            allowance = allowdeduct['allowance']
            #potongan
            deduction = allowdeduct['deduction']            
            
            #pendapatan kotor
            bruto = basic + allowance            
                        
            #ambil biaya jabatan
            occupy_exp = get_occupy_expense(cr)
            #percent                
            occupy_rate = occupy_exp['rate']
            #maximum amount 
            occupy_max = occupy_exp['max']         
            
            #hitung biaya jabatan percent / maximum
            occupy_exp_amount = (occupy_rate/100) * bruto                
            if occupy_exp_amount > occupy_max: occupy_exp_amount = occupy_max
                 
            #netto 1 tahun
            netto = (bruto - occupy_exp_amount) * 12
                        
            #golongan ptkp
            try:
                ptkp = slip.employee_id.gol_ptkp.ptkp
            except Exception, e:    
                raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % ('golongan ptkp undefined (setting in contract)'))
                        
            #tidak kena pajak
            if netto < ptkp:
                return 0
                        
            #pendapatan kena pajak 
            pkp = netto - ptkp
            log.info("pkp_normal=%s" % (pkp))
            #calculate pph progressive
            _pph_total = calc_pph_progressive(cr,pkp)
            _pph_total_month = _pph_total / 12    
            #pph terhutang
            intax_allow = _pph_total_month
            #except Exception, e:
            #    raise osv.except_osv(_('Variable Error !'), _('Variable Error 14: %s ') % (e))
                
            #log.info("intax_allow=%s" % (intax_allow))            
            return intax_allow
        
        def compute_pph_allow_december(cr, slip, cumulative_pph):
            intax_allow = 0
            basic=0
            allowance = 0
            deduction = 0
            #try:
            #gaji pokok                
            basic = slip.employee_id.contract_id.wage            
            if basic <= 0:
                raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % ('basic salary undefined!'))
            
            #get allow & deduction
            allowdeduct = get_allow_deduct_intax_pph(cr, slip.id)
            #tunjangan                 
            allowance = allowdeduct['allowance']
            #potongan
            deduction = allowdeduct['deduction']            
            
            #bruto current month (december), tunj pph = 0
            pph_allow_dec = compute_pph_allow_normal(cr, slip)
            log.info("pph_allow_dec=%s" % pph_allow_dec)
            bruto_pph = basic + allowance + pph_allow_dec 
            log.info("bruto_pph=%s" % bruto_pph)
            #pendapatan kotor 12 bulan
            slip_date = datetime.strptime(slip.date, '%Y-%m-%d')
            #terhitung 11 bulan
            bruto_pph_total = get_bruto_pph_total(cr, slip.employee_id.id, slip_date.year, 11)
            #tambah bruto_pph bulan desember            
            bruto_pph_total += bruto_pph         
            log.info("bruto_pph_total=%s" % bruto_pph_total)    
            #ambil biaya jabatan
            occupy_exp = get_occupy_expense(cr)
            #percent                
            occupy_rate = occupy_exp['rate']
            #maximum amount 
            occupy_max = occupy_exp['max']                
            
            #hitung biaya jabatan percent / maximum
            occupy_exp_amount = (occupy_rate/100) * bruto_pph                
            if occupy_exp_amount > occupy_max: occupy_exp_amount = occupy_max
                 
            #netto 1 tahun
            netto_pph_total = bruto_pph_total - occupy_exp_amount - deduction
            log.info("netto_pph_total=%s" % netto_pph_total)            
            #golongan ptkp
            try:
                ptkp = slip.employee_id.gol_ptkp.ptkp
            except Exception, e:    
                raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % ('golongan ptkp undefined'))
                        
            #tidak kena pajak
            if netto_pph_total < ptkp:
                return 0
                        
            #pendapatan kena pajak 
            pkp_total = netto_pph_total - ptkp
            log.info("pkp_total=%s" % pkp_total)
            
            #log.info("pkp=%s" % (pkp))
            _pph_total = calc_pph_progressive(cr, pkp_total)
            log.info("_pph_total=%s" % _pph_total)
            log.info("cumulative_pph=%s" % cumulative_pph)            
            _pph_december = _pph_total - cumulative_pph
            log.info("_pph_december=%s" % _pph_december)     
            #pph terhutang
            intax_allow = _pph_december     
            #except Exception, e:
            #    raise osv.except_osv(_('Variable Error !'), _('Variable Error 14: %s ') % (e))
                
            #log.info("intax_allow=%s" % (intax_allow))            
            return intax_allow
        
        def compute_pph_allow_less_1y(cr, slip, month_to_calc):
            intax_allow = 0
            basic=0
            allowance = 0
            deduction = 0
            #try:
            #gaji pokok                
            basic = slip.employee_id.contract_id.wage            
            if basic <= 0:
                raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % ('basic salary undefined!'))
            
            #get allow & deduction
            allowdeduct = get_allow_deduct_intax_pph(cr, slip.id)
            #tunjangan                 
            allowance = allowdeduct['allowance']
            #potongan
            deduction = allowdeduct['deduction']            
            
            #pendapatan kotor
            pph_allow_current = compute_pph_allow_normal(cr, slip)
            bruto_pph = basic + allowance + pph_allow_current            
                        
            #ambil biaya jabatan
            occupy_exp = get_occupy_expense(cr)
            #percent                
            occupy_rate = occupy_exp['rate']
            #maximum amount 
            occupy_max = occupy_exp['max']         
            
            #hitung biaya jabatan percent / maximum
            occupy_exp_amount = (occupy_rate/100) * bruto_pph                
            if occupy_exp_amount > occupy_max: occupy_exp_amount = occupy_max / 12
            #pendapatan bersih bulan berjalan     
            netto_pph = bruto_pph - occupy_exp_amount -deduction
            #pendapatan bersih 1th
            netto_pph_1y = netto_pph * month_to_calc 
                        
            #golongan ptkp
            try:
                ptkp = slip.employee_id.gol_ptkp.ptkp
            except Exception, e:    
                raise osv.except_osv(_('Variable Error !'), _('Variable Error : %s ') % ('golongan ptkp undefined (setting in contract)'))
                        
            #tidak kena pajak
            if netto_pph_1y < ptkp:
                return 0
                        
            #pendapatan kena pajak 
            pkp = netto_pph_1y - ptkp
            #log.info("pkp_1y=%s" % (pkp))
            #calculate pph progressive
            _pph_total = calc_pph_progressive(cr,pkp)
            _pph_total_month = _pph_total / 12    
            #pph terhutang
            intax_allow = _pph_total_month
            #except Exception, e:
            #    raise osv.except_osv(_('Variable Error !'), _('Variable Error 14: %s ') % (e))
                
            #log.info("intax_allow=%s" % (intax_allow))            
            return intax_allow
        
        
        slip_line_obj = self.pool.get('hr.payslip.line')
        register_pool = self.pool.get('company.contribution')
        res = {}
        uang_makan = 0
        uang_transport = 0
        for rs in self.browse(cr, uid, ids, context=context):
            #log.info("rs=%s" % rs)
            #mode perhitungan pph gross/gross_up
            tax_mode = rs.employee_id.contract_id.tax_mode
            join_date = datetime.strptime(rs.employee_id.contract_id.date_start, '%Y-%m-%d')
            cumulative_pph = 0.0            
            pph_allow = 0.0
            allow = 0.0
            deduct = 0.0
            others = 0.0
            obj = {
                'basic':rs.basic,
                'gaji_pokok':rs.basic,
                'uang_makan':0.0,
                'uang_transport':0.0,
                'uang_lembur':0.0,
                'iuran_premi_kk':0.0,
                'iuran_premi_jk':0.0,
                'premi_jht':0.0,
                'formula_pph':False,
                'formula_pph21':False
            }
            if rs.igross > 0:
                obj['gross'] = rs.igross
                obj['gaji_pokok'] = rs.igross
            if rs.inet > 0:
                obj['net'] = rs.inet
            for line in rs.line_ids:                
                base = line.category_id.base                     
                #tunjangan pph hanya untuk gross_up
                if base == 'formula_pph' and tax_mode != 'gross_up': continue
                           
                amount = 0.0
                #log.info("base=%s,line.amount_type=%s;tax_mode=%s" % (base, line.amount_type, tax_mode))                
                if base in ('gaji_pokok','uang_makan','uang_transport','uang_lembur',
                            'formula_pph','iuran_premi_kk', 'iuran_premi_jk','premi_jht'):
                    if line.amount_type == 'per':
                        if base == 'gaji_pokok':
                            try:
                                amount = line.amount * eval(str(line.category_id.base), obj)
                            except Exception, e:
                                raise osv.except_osv(_('Variable Error !'), _('Variable Error 7: %s ') % (e))
                        elif base == 'uang_makan': amount = rs.late_days * line.amount * uang_makan
                        elif base == 'uang_transport': amount = rs.late_days * line.amount * uang_transport
                        elif base == 'iuran_premi_kk': amount = rs.basic * line.amount
                        elif base == 'iuran_premi_jk': amount = rs.basic * line.amount
                        elif base == 'premi_jht': amount = rs.basic * line.amount                
                        elif base == 'formula_pph': 
                            prev_cumulative_pph = get_prev_cumulative_pph(cr, rs.date)
                            #awal tahun
                            jan = date(date.today().year, 1, 1)
                            #masuk kerja >= 1 thn
                            if join_date.strftime('%Y%m') < jan.strftime('%Y%m'):
                                #pph akhir tahun (desember)
                                if datetime.strptime(rs.date, '%Y-%m-%d').month == 12:
                                    pph_allow = compute_pph_allow_december(cr, rs, prev_cumulative_pph)
                                else:
                                    #pph normal
                                    pph_allow = compute_pph_allow_normal(cr, rs)
                            else:
                                #masuk kerja setelah januari / < 1 thn
                                month_to_calc = (12 - join_date.month) + 1
                                log.info("month_to_calc=%s;join_date.month=%s" % (month_to_calc, join_date.month))
                                pph_allow = compute_pph_allow_less_1y(cr, rs, month_to_calc)                          
                                    
                            cumulative_pph =  pph_allow + prev_cumulative_pph
                            amount = pph_allow 
                            
                            
                
                    elif line.amount_type == 'fix_daily':
                        #multiplier berisi hari telah bekerja
                        if base == 'uang_makan':
                            amount = line.amount * line.multiplier1
                            uang_makan = line.amount 
                            #log.info("total_uang_makan=%s" % total_uang_makan)
                        elif base == 'uang_transport':      
                            amount = line.amount * line.multiplier1
                            uang_transport = line.amount
                            #log.info("total_uang_tranport=%s" % total_uang_transport)
                    elif line.amount_type == 'fix_hourly':
                        if base == 'uang_lembur':      
                            amount = line.amount * line.multiplier2                            
                else:                    
                    if line.amount_type == 'per':
                        try:
                            amount = line.amount * eval(str(line.category_id.base), obj)
                        except Exception, e:
                            raise osv.except_osv(_('Variable Error !'), _('Variable Error 7: %s ') % (e))
                    elif line.amount_type in ('fix', 'func'):
                        amount = line.amount
                
                                            
                cd = line.category_id.code.lower()
                obj[cd] = amount
                contrib = 0.0
                #dihitung hanya jika selain gaji pokok
                if base != 'gaji_pokok':
                    if line.type == 'allowance':
                        allow += amount
                        others += contrib
                        amount -= contrib
                    elif line.type == 'deduction':
                        deduct += amount
                        others -= contrib
                        amount += contrib
                    elif line.type == 'advance':
                        others += amount
                    elif line.type == 'loan':
                        others += amount
                    elif line.type == 'otherpay':
                        others += amount

                company_contrib = 0.0
                for contrib_line in line.category_id.contribute_ids:
                    company_contrib += register_pool.compute(cr, uid, contrib_line.id, amount, context)

                slip_line_obj.write(cr, uid, [line.id], {'total':amount, 'company_contrib':company_contrib}, context=context)
            #log.info("rs.overtimes=%s" % rs.overtimes)                 
                       
            record = {
                'allounce':allow,
                'deduction':deduct,
                'grows':rs.basic + allow,
                'net':rs.basic + allow - deduct,
                'other_pay':others,
                'total_pay':rs.basic + allow - deduct,
                'pph_allounce': pph_allow,
                'cumulative_pph':cumulative_pph
            }
            res[rs.id] = record
        return res
        
    #override
    def compute_sheet(self, cr, uid, ids, context=None):
        func_pool = self.pool.get('hr.payroll.structure')
        slip_line_pool = self.pool.get('hr.payslip.line')
        holiday_pool = self.pool.get('hr.holidays')
        sequence_obj = self.pool.get('ir.sequence')
        
        if context is None:
            context = {}
        date = self.read(cr, uid, ids, ['date'], context=context)[0]['date']
        
        def get_sheet_id_by_employee_and_month(cr, employee_id, month):            
            try:            
                id = 0
                cr.execute('SELECT s.id \
                    FROM hr_timesheet_sheet_sheet s \
                    WHERE s.employee_id = %s AND extract(month from date_to) = %s ',(employee_id, month)) 
                for record in cr.fetchall():
                    id = record[0]                                
            
            except Exception, e:
                raise osv.except_osv(_('Variable Error !'), _('Variable Error: %s') % (e))
            
            return id
                
        def get_sheet(cr, employee_id, month):            
            try:            
                sheet = {}
                cr.execute('SELECT s.id, s.date_from, s.date_to \
                    FROM hr_timesheet_sheet_sheet s \
                    WHERE s.employee_id = %s AND extract(month from date_to) = %s ',(employee_id, month)) 
                for record in cr.fetchall():
                    sheet['id'] = record[0]
                    sheet['date_from'] = datetime.strptime(record[1], '%Y-%m-%d')
                    sheet['date_to'] = datetime.strptime(record[2], '%Y-%m-%d')
                if len(sheet.keys()) == 0: return False
                return sheet
            
            except Exception, e:
                raise osv.except_osv(_('Variable Error !'), _('Variable Error: %s') % (e))
            
            return False
        
        def get_worked_days(cr, employee_id, date_from, date_to, schedule_arr = None):
            worked_days = []            
            try:       
                query = "SELECT a.id, a.name, a.day \
                        FROM hr_attendance a \
                        WHERE a.action = '%s' AND a.employee_id = %d AND a.day BETWEEN '%s' AND '%s'  " % ('sign_in',employee_id, date_from.strftime('%Y-%m-%d'), date_to.strftime('%Y-%m-%d'))
                    
                #log.info("query=%s" % query)        
                cr.execute(query)
                if schedule_arr:
                    for record in cr.fetchall():
                        if datetime.strptime(record[2], '%Y-%m-%d').weekday() in schedule_arr:
                            worked_days.append(record)
            except Exception, e:
                raise osv.except_osv(_('Variable Error !'), _('Variable Error: %s') % (e))
            
            return worked_days                              
            
        #Check for the Holidays
        
        def get_days(start, end, month, year, calc_day):
            import datetime
            count = 0
            for day in range(start, end):
                if datetime.date(year, month, day).weekday() == calc_day:
                    count += 1
            return count
                
        for slip in self.browse(cr, uid, ids, context=context):
            
            old_slip_ids = slip_line_pool.search(cr, uid, [('slip_id','=',slip.id)], context=context)
            slip_line_pool.unlink(cr, uid, old_slip_ids, context=context)
            update = {}
            ttyme = datetime.fromtimestamp(time.mktime(time.strptime(slip.date,"%Y-%m-%d")))

            #dates = prev_bounds(slip.date)
            #get sheet
            sheet = get_sheet(cr, slip.employee_id.id, ttyme.month )
            if sheet == False:
                raise osv.except_osv(_('Variable Error !'), 'No timesheet defined for employee %s at %s ' % (slip.employee_id.name, slip.date))
            
            
            #log.info("slip.employee_id=%s, slip.date=%s, sheet=%s" % (slip.employee_id, slip.date, sheet))
            
            days_arr = []                        
            try:
                for d in slip.employee_id.contract_id.working_hours.attendance_ids: days_arr.append(int(d.dayofweek))                    
            except Exception, e:
                raise osv.except_osv(_('Variable Error !'), 'Working schedule not found.')    
                           
            worked_days = get_worked_days(cr, slip.employee_id.id, sheet['date_from'], sheet['date_to'], days_arr)
            
            #overtime_hours
            overtime_hours = 0
            sheet_pool = self.pool.get('hr_timesheet_sheet.sheet')
            for sheet_obj in sheet_pool.browse(cr, uid, [sheet['id']], context=context):
                overtime_hours = sheet_obj.total_overtimes
                
            contracts = self.get_contract(cr, uid, slip.employee_id, date, context)
            if contracts.get('id', False) == False:
                update.update({
                    'basic': round(0.0),
                    'basic_before_leaves': round(0.0),
                    'name':'Salary Slip of %s for %s' % (slip.employee_id.name, tools.ustr(ttyme.strftime('%B-%Y'))),
                    'state':'draft',
                    'contract_id':False,
                    'company_id':slip.employee_id.company_id.id
                })
                self.write(cr, uid, [slip.id], update, context=context)
                continue

            contract = slip.employee_id.contract_id
            sal_type = contract.wage_type_id.type
            function = contract.struct_id.id
            #mode perhitungan pph gross/gross_up
            tax_mode = contract.tax_mode
            
            lines = []
            if function:
                func = func_pool.read(cr, uid, function, ['line_ids'], context=context)
                lines = slip_line_pool.browse(cr, uid, func['line_ids'], context=context)

            #lines += slip.employee_id.line_ids
            
            ad = []
            all_per = 0.0
            ded_per = 0.0
            all_fix = 0.0
            ded_fix = 0.0
            
            uang_lembur = contract.wage / 173
            #custom
            obj = {
               'basic':0.0,
               'gaji_pokok':contract.wage,
               'uang_makan':contract.food_allounce,
               'uang_transport':contract.trans_allounce,
               'uang_lembur':uang_lembur,               
               'iuran_premi_kk':0.0,
               'iuran_premi_jk':0.0,
               'premi_jht':0.0,
               'formula_pph':False,
               'formula_pph21':False
            }
            
            if contract.wage_type_id.type == 'gross':
                obj['gross'] = contract.wage
                update['igross'] = contract.wage
            if contract.wage_type_id.type == 'net':
                obj['net'] = contract.wage
                update['inet'] = contract.wage
            if contract.wage_type_id.type == 'basic':
                obj['basic'] = contract.wage
                update['basic'] = contract.wage
                
           
            for line in lines:                                
                base = False
                base = line.category_id.base
                #tunjangan pph hanya untuk gross_up
                if base == 'formula_pph' and tax_mode != 'gross_up':
                    continue
                
                cd = line.code.lower()
                obj[cd] = line.amount or 0.0

            for line in lines:                
                base = False
                base = line.category_id.base
                #tunjangan pph hanya untuk gross_up                
                if base == 'formula_pph' and tax_mode != 'gross_up':
                    continue
                
                if line.category_id.code in ad:
                    continue
                
                ad.append(line.category_id.code)
                cd = line.category_id.code.lower()
                calculate = False
                try:
                    exp = line.category_id.condition
                    calculate = eval(exp, obj)
                except Exception, e:
                    raise osv.except_osv(_('Variable Error !'), _('Variable Error 1: %s ') % (e))

                if not calculate:
                    continue

                percent = 0.0
                value = 0.0                
#                company_contrib = 0.0    
                #log.info('base=%s, sal_type=%s, line.amount_type=%s, contract.food_allounce=%d, contract.trans_allounce=%d, overtime_hours=%s, iuran_premi_kk=%s,premi_jht=%s' % (base, sal_type,line.amount_type,contract.food_allounce,contract.trans_allounce, overtime_hours, contract.iuran_premi_kk, contract.premi_jht))
                try:
                    #Please have a look at the configuration guide.
                    amt = eval(base, obj)                    
                except Exception, e:
                    raise osv.except_osv(_('Variable Error !'), _('Variable Error 2: %s') % (e))

                if base in ('gaji_pokok','uang_makan','uang_transport','uang_lembur',
                            'formula_pph','iuran_premi_kk', 'iuran_premi_jk','premi_jht'):
                    #begin custom
                    if sal_type in ('gross', 'net'):
                        if line.amount_type == 'per':
                            if base == 'gaji_pokok': 
                                percent = line.amount
                                if amt > 1:
                                    value = percent * amt
                                elif amt > 0 and amt <= 1:
                                    percent = percent * amt
                                if value > 0:
                                    percent = 0.0
                            else:
                                if base == 'uang_makan': percent = contract.food_allounce_deduct
                                elif base == 'uang_transport': percent = contract.trans_allounce_deduct
                                elif base == 'iuran_premi_kk': percent = contract.iuran_premi_kk
                                elif base == 'iuran_premi_jk': percent = contract.iuran_premi_jk
                                elif base == 'premi_jht': percent = contract.premi_jht
                                elif base == 'formula_pph': percent = 1.0
                                line.amount = percent
                            
                        elif line.amount_type == 'fix_daily':
                            if base == 'uang_makan':
                                value = contract.food_allounce
                            elif base == 'uang_transport':      
                                value = contract.trans_allounce                            
                            line.amount = value
                        elif line.amount_type == 'fix_hourly':
                            if base == 'uang_lembur':
                                value = uang_lembur
                            line.amount = value    
                    else:
                        if line.amount_type == 'per':
                            if base == 'gaji_pokok': value = line.amount
                            else:
                                if base == 'uang_makan': line.amount = contract.food_allounce_deduct
                                elif base == 'uang_transport': line.amount = contract.trans_allounce_deduct
                                elif base == 'iuran_premi_kk': line.amount = contract.iuran_premi_kk
                                elif base == 'iuran_premi_jk': line.amount = contract.iuran_premi_jk
                                elif base == 'premi_jht': line.amount = contract.premi_jht
                                elif base == 'formula_pph': line.amount = 1.0
                                value = line.amount
                        elif line.amount_type == 'fix_daily':
                            if base == 'uang_makan':
                                line.amount = contract.food_allounce
                            elif base == 'uang_transport':      
                                line.amount = contract.trans_allounce
                            value = line.amount
                        elif line.amount_type == 'fix_hourly':
                            if base == 'uang_lembur':
                                line.amount = uang_lembur    
                            value = line.amount
                    #end custom
                    
                else:
                    if sal_type in ('gross', 'net'):
                        if line.amount_type == 'per':
                            percent = line.amount
                            if amt > 1:
                                value = percent * amt
                            elif amt > 0 and amt <= 1:
                                percent = percent * amt
                            if value > 0:
                                percent = 0.0
                        elif line.amount_type == 'fix':
                            value = line.amount
                        elif line.amount_type == 'func':
                            value = slip_line_pool.execute_function(cr, uid, line.id, amt, context)
                            line.amount = value                            
                    else:
                        if line.amount_type in ('fix', 'per'):
                            value = line.amount
                        elif line.amount_type == 'func':
                            value = slip_line_pool.execute_function(cr, uid, line.id, amt, context)
                            line.amount = value
                                                
                #total dihitung hanya jika selain gaji pokok
                if base != 'gaji_pokok':                    
                    if line.type == 'allowance':
                        all_per += percent
                        all_fix += value                    
                    elif line.type == 'deduction':
                        ded_per += percent
                        ded_fix += value                
                                        
                vals = {
                    'amount':line.amount,
                    'slip_id':slip.id,
                    'employee_id':False,
                    'function_id':False,
                    'base':base,
                    'multiplier1': len(worked_days),
                    'multiplier2': overtime_hours
                }
                slip_line_pool.copy(cr, uid, line.id, vals, {})
            
            if sal_type in ('gross', 'net'):                
                sal = contract.wage
                if sal_type == 'net':
                    sal += ded_fix
                sal -= all_fix
                per = 0.0
                if sal_type == 'net':
                    per = (all_per - ded_per)
                else:
                    per = all_per
                if per <=0:
                    per *= -1
                final = (per * 100) + 100
                basic = (sal * 100) / final
            else:
                basic = contract.wage

            number = sequence_obj.get(cr, uid, 'salary.slip')
            update.update({
                'deg_id':function,
                'number':number,
                'basic': round(basic),
                'basic_before_leaves': round(basic),
                'name':'Salary Slip of %s for %s' % (slip.employee_id.name, tools.ustr(ttyme.strftime('%B-%Y'))),
                'state':'draft',
                'contract_id':contract.id,
                'company_id':slip.employee_id.company_id.id
            })
                
            for line in slip.employee_id.line_ids:                                
                #tunjangan pph hanya untuk gross_up
                if base == 'formula_pph' and tax_mode != 'gross_up':
                    continue
                
                vals = {
                    'amount':line.amount,
                    'slip_id':slip.id,
                    'employee_id':False,
                    'function_id':False,
                    'base':base,
                    'multiplier1': len(worked_days),                    
                    'multiplier2': overtime_hours
                }                
                slip_line_pool.copy(cr, uid, line.id, vals, {})

            self.write(cr, uid, [slip.id], update, context=context)
            
        for slip in self.browse(cr, uid, ids, context=context):
            if not slip.contract_id:
                continue

            basic_before_leaves = slip.basic
            working_day = 0
            off_days = 0
            late_days = 0
            overtime_hours = 0
            overtime_fee = 0
            #begin custom variables: working_day, off_day, total_off
            #range diambil dari timesheet
                        
            #log.info(slip.employee_id.contract_id.working_hours.attendance_ids)
            #store workingtime value
            days_arr = [] 
            #days_sign_limit
            days_sign_limit = {}
            try:
                for d in slip.employee_id.contract_id.working_hours.attendance_ids: 
                    days_arr.append(int(d.dayofweek))
                    days_sign_limit[int(d.dayofweek)] = d.hour_from
                                        
            except Exception, e:
                raise osv.except_osv(_('Variable Error !'), 'Working schedule not found.')
            
            #total jumlah hari                        
            total_day = (sheet['date_to'] - sheet['date_from']).days + 1
            total_off = 0
            d = sheet['date_from']
            delta = timedelta(days=1)
            while d <= sheet['date_to']:
                if d.weekday() not in days_arr: 
                    total_off += 1                
                d += delta
            #total hari kerja
            working_day = total_day - total_off
            
            #total hari telah berkeja
            worked_days = get_worked_days(cr, slip.employee_id.id, sheet['date_from'], sheet['date_to'], days_arr)
            #hitung jumlah hari terlambat
            for w in worked_days:
                sign_in_date = datetime.strptime(w[1], '%Y-%m-%d %H:%M:%S')                
                if days_sign_limit[sign_in_date.weekday()] < sign_in_date.hour:                 
                    late_days += 1
            
            #total jumlah jam lebur
            sheet_pool = self.pool.get('hr_timesheet_sheet.sheet')
            for sheet_obj in sheet_pool.browse(cr, uid, [sheet['id']], context=context):
                overtime_hours = sheet_obj.total_overtimes
            
            #overtime_fee            
            #try:
            #    overtime_fee = (contract.wage / 173) * overtime_hours                                
            #except Exception, e:
            #    raise osv.except_osv(_('Variable Error !'), _('Variable Error: %s') % (e))     
            #end custom
            
            perday = slip.net / working_day
            total = 0.0
            leave = 0.0
            leave_ids = self._get_leaves(cr, uid, slip, slip.employee_id, context)
            total_leave = 0.0
            paid_leave = 0.0
            #BEGIN HOLIDAY
            for hday in holiday_pool.browse(cr, uid, leave_ids, context=context):
                if not hday.holiday_status_id.head_id:
                    raise osv.except_osv(_('Error !'), _('Please check configuration of %s, payroll head is missing') % (hday.holiday_status_id.name))

                res = {
                    'slip_id':slip.id,
                    'name':hday.holiday_status_id.name + '-%s' % (hday.number_of_days),
                    'code':hday.holiday_status_id.code,
                    'amount_type':'fix',
                    'category_id':hday.holiday_status_id.head_id.id,
                    'sequence':hday.holiday_status_id.head_id.sequence
                }
                days = hday.number_of_days
                if hday.number_of_days < 0:
                    days = hday.number_of_days * -1
                total_leave += days
                if hday.holiday_status_id.type == 'paid':
                    paid_leave += days
                    continue
#                    res['name'] = hday.holiday_status_id.name + '-%s' % (days)
#                    res['amount'] = perday * days
#                    res['type'] = 'allowance'
#                    leave += days
#                    total += perday * days

                elif hday.holiday_status_id.type == 'halfpaid':
                    paid_leave += (days / 2)
                    res['name'] = hday.holiday_status_id.name + '-%s/2' % (days)
                    res['amount'] = perday * (days/2)
                    total += perday * (days/2)
                    leave += days / 2
                    res['type'] = 'deduction'
                else:
                    res['name'] = hday.holiday_status_id.name + '-%s' % (days)
                    res['amount'] = perday * days
                    res['type'] = 'deduction'
                    leave += days
                    total += perday * days

                slip_line_pool.create(cr, uid, res, context=context)
            #END HOLIDAY
                
            basic = basic - total
#           leaves = total
            update.update({
                'basic':basic,
                'basic_before_leaves': round(basic_before_leaves),
                'leaves':total,
                'holiday_days':leave,
                'worked_days': len(worked_days), #working_day - leave
                'working_days':working_day,
                'late_days':late_days,
                'lates':0,
                'overtime_hours':overtime_hours
            })
            self.write(cr, uid, [slip.id], update, context=context)
        return True
    _columns = {                
        'overtime_hours': fields.float('Overtimes', readonly=True),        
        'late_days': fields.float('No of Lates', readonly=True),
        'lates': fields.float('Late Deductions', readonly=True,  digits_compute=dp.get_precision('Account')),        
        'grows': fields.function(_calculate, method=True, store=True, multi='dc', string='Gross Salary', digits_compute=dp.get_precision('Account')),
        'net': fields.function(_calculate, method=True, store=True, multi='dc', string='Net Salary', digits_compute=dp.get_precision('Account')),
        'allounce': fields.function(_calculate, method=True, store=True, multi='dc', string='Allowance', digits_compute=dp.get_precision('Account')),
        'deduction': fields.function(_calculate, method=True, store=True, multi='dc', string='Deduction', digits_compute=dp.get_precision('Account')),
        'other_pay': fields.function(_calculate, method=True, store=True, multi='dc', string='Others', digits_compute=dp.get_precision('Account')),
        'total_pay': fields.function(_calculate, method=True, store=True, multi='dc', string='Total Payment', digits_compute=dp.get_precision('Account')),
        'pph_allounce': fields.function(_calculate, method=True, store=True, type="float", multi='dc', string='Pph Allowance', digits_compute=dp.get_precision('Account')),
        'cumulative_pph': fields.function(_calculate, method=True, store=True, type="float", multi='dc', string='Cumulative Pph', digits_compute=dp.get_precision('Account')),
    }
    
hr_payslip()

class hr_contract(osv.osv):
    _inherit = "hr.contract"    
    def compute_basic(self, cr, uid, ids, context=None):
        res = {}
        if context is None:
            context = {}
        ids += context.get('employee_structure', [])

        slip_line_pool = self.pool.get('hr.payslip.line')

        for contract in self.browse(cr, uid, ids, context=context):
            #mode perhitungan pph gross/gross_up
            tax_mode = contract.tax_mode 
            
            all_per = 0.0
            ded_per = 0.0
            all_fix = 0.0
            ded_fix = 0.0
            #custom
            uang_lembur = contract.wage / 173
            obj = {
               'basic':0.0,
               'gaji_pokok':contract.wage,
               'uang_makan':contract.food_allounce,
               'uang_transport':contract.trans_allounce ,
               'uang_lembur':uang_lembur,               
               'iuran_premi_kk':0.0,
               'iuran_premi_jk':0.0,
               'premi_jht':0.0,
               'formula_pph':False,
               'formula_pph21':False
               
            }
            
            update = {}
            if contract.wage_type_id.type == 'gross':
                obj['gross'] = contract.wage
                update['gross'] = contract.wage
            if contract.wage_type_id.type == 'net':
                obj['net'] = contract.wage
                update['net'] = contract.wage
            if contract.wage_type_id.type == 'basic':
                obj['basic'] = contract.wage
                update['basic'] = contract.wage
                        

            sal_type = contract.wage_type_id.type
#            function = contract.struct_id.id
            lines = contract.struct_id.line_ids
            if not contract.struct_id:
                res[contract.id] = obj['basic']
                continue

            ad = []
            for line in lines:                              
                base = line.category_id.base                  
                #tunjangan pph hanya untuk gross_up
                if base == 'formula_pph' and tax_mode != 'gross_up':
                    continue
                
                cd = line.code.lower()
                obj[cd] = line.amount or 0.0

            for line in lines:                        
                base = False
                base = line.category_id.base                        
                #tunjangan pph hanya untuk gross_up
                if base == 'formula_pph' and tax_mode != 'gross_up':
                    continue
                
                if line.category_id.code in ad:
                    continue
                ad.append(line.category_id.code)
                cd = line.category_id.code.lower()
                calculate = False
                try:
                    exp = line.category_id.condition
                    calculate = eval(exp, obj)
                except Exception, e:
                    raise osv.except_osv(_('Variable Error !'), _('Variable Error: %s test1') % (e))

                if not calculate:
                    continue

                percent = 0.0
                value = 0.0
#                company_contrib = 0.0
                try:
                    #Please have a look at the configuration guide.
                    amt = eval(base, obj)
                except Exception, e:
                    raise osv.except_osv(_('Variable Error !'), _('Variable Error: %s test2') % (e))
                
                #log.info("base=%s;sal_type=%s;line.amount_type=%s" % (base,sal_type,line.amount_type))
                if base in ('gaji_pokok', 'uang_makan', 'uang_transport', 'uang_lembur',
                            'formula_pph','iuran_premi_kk', 'iuran_premi_jk','premi_jht'):
                    #begin custom
                    if sal_type in ('gross', 'net'):                        
                        if line.amount_type == 'per':
                            if base == 'gaji_pokok':
                                percent = line.amount
                                if amt > 1:
                                    value = percent * amt
                                elif amt > 0 and amt <= 1:
                                    percent = percent * amt
                                if value > 0:
                                    percent = 0.0
                            else:
                                if base == 'uang_makan': percent = contract.food_allounce_deduct
                                elif base == 'uang_transport': percent = contract.trans_allounce_deduct
                                elif base == 'iuran_premi_kk': percent = contract.iuran_premi_kk
                                elif base == 'iuran_premi_jk': percent = contract.iuran_premi_jk
                                elif base == 'premi_jht': percent = contract.premi_jht
                                elif base == 'formula_pph': percent = 1.0
                                line.amount = percent
                            
                        elif line.amount_type == 'fix_daily':
                            if base == 'uang_makan':
                                value = contract.food_allounce
                            elif base == 'uang_transport':      
                                value = contract.trans_allounce
                        elif line.amount_type == 'fix_hourly':
                            if base == 'uang_lembur':      
                                value = uang_lembur        
                    else:
                        if line.amount_type == 'per':      
                            if base == 'gaji_pokok':
                                value = line.amount
                            else:                       
                                if base == 'uang_makan': line.amount = contract.food_allounce_deduct
                                elif base == 'uang_transport': line.amount = contract.trans_allounce_deduct
                                elif base == 'iuran_premi_kk': line.amount = contract.iuran_premi_kk
                                elif base == 'iuran_premi_jk': line.amount = contract.iuran_premi_jk
                                elif base == 'premi_jht': line.amount = contract.premi_jht
                                elif base == 'formula_pph': line.amount = 1.0
                                value = line.amount
                            
                        elif line.amount_type == 'fix_daily':
                            if base == 'uang_makan':
                                value = contract.food_allounce
                            elif base == 'uang_transport':      
                                value = contract.trans_allounce
                        elif line.amount_type == 'fix_hourly':
                            if base == 'uang_lembur':      
                                value = uang_lembur
                                
                    #end custom
                else:
                    if sal_type in ('gross', 'net'):
                        if line.amount_type == 'per':
                            percent = line.amount
                            if amt > 1:
                                value = percent * amt
                            elif amt > 0 and amt <= 1:
                                percent = percent * amt
                            if value > 0:
                                percent = 0.0
                        elif line.amount_type == 'fix':
                            value = line.amount
                        elif line.amount_type == 'func':
                            value = slip_line_pool.execute_function(cr, uid, line.id, amt, context)
                            line.amount = value                            
                    else:
                        if line.amount_type in ('fix', 'per'):
                            value = line.amount
                        elif line.amount_type == 'func':
                            value = slip_line_pool.execute_function(cr, uid, line.id, amt, context)
                            line.amount = value
                
                #dihitung jika hanya selain gaji pokok
                if base != 'gaji_pokok':                    
                    if line.type == 'allowance':
                        all_per += percent
                        all_fix += value
                    elif line.type == 'deduction':
                        ded_per += percent
                        ded_fix += value
                    
            if sal_type in ('gross', 'net'):
                sal = contract.wage
                if sal_type == 'net':
                    sal += ded_fix
                sal -= all_fix
                per = 0.0
                if sal_type == 'net':
                    per = (all_per - ded_per)
                else:
                    per = all_per
                if per <=0:
                    per *= -1
                final = (per * 100) + 100
                basic = (sal * 100) / final
            else:
                basic = contract.wage

            res[contract.id] = basic

        return res

    def _calculate_salary(self, cr, uid, ids, field_names, arg, context=None):
        res = self.compute_basic(cr, uid, ids, context=context)
        vals = {}
        for rs in self.browse(cr, uid, ids, context=context):
            tax_mode = rs.employee_id.contract_id.tax_mode
            
            allow = 0.0
            deduct = 0.0
            others = 0.0
            
            obj = {
                'basic':res[rs.id],                
                'gaji_pokok':rs.wage,
                'uang_makan':0.0,
                'uang_transport':0.0,
                'uang_lembur':0.0, 
                'gross':0.0, 
                'net':0.0,                
                'iuran_premi_kk':0.0,
                'iuran_premi_jk':0.0,
                'premi_jht':0.0,
                'formula_pph':1.0,
                'formula_pph21':1.0,
            }
            
            if rs.wage_type_id.type == 'gross':
                obj['gross'] = rs.wage
            if rs.wage_type_id.type == 'net':
                obj['net'] = rs.net

            if not rs.struct_id:
                if self.check_vals(obj['basic'], obj['gross']):
                    obj['gross'] = obj['basic'] = obj['net']
                elif self.check_vals(obj['gross'], obj['net']):
                    obj['gross']= obj['net'] = obj['basic']
                elif self.check_vals(obj['net'], obj['basic']):
                    obj['net'] = obj['basic'] = obj['gross']
                
                record = {
                    'advantages_gross':0.0,
                    'advantages_net':0.0,
                    'basic':obj['basic'],
                    'gross':obj['gross'],
                    'net':obj['net']
                }
                vals[rs.id] = record
                continue

            for line in rs.struct_id.line_ids:     
                base = line.category_id.base                           
                #tunjangan pph hanya untuk gross_up                
                if base == 'formula_pph' and tax_mode != 'gross_up':
                    continue
                
                amount = 0.0
                if line.amount_type == 'per':
                    try:                        
                        amount = line.amount * eval(str(line.category_id.base), obj)                        
                    except Exception, e:
                        raise osv.except_osv(_('Variable Error !'), _('Variable Error: %s ') % (e))
                elif line.amount_type in ('fix', 'func'):
                    amount = line.amount
                cd = line.category_id.code.lower()
                obj[cd] = amount
                
                #hanya dihitung jika selain gaji pokok
                if base != 'gaji_pokok':
                    if line.type == 'allowance':
                        allow += amount
                    elif line.type == 'deduction':
                        deduct += amount
                    elif line.type == 'advance':
                        others += amount
                    elif line.type == 'loan':
                        others += amount
                    elif line.type == 'otherpay':
                        others += amount
            record = {
                'advantages_gross':round(allow),
                'advantages_net':round(deduct),
                'basic':obj['basic'],
                'gross':round(obj['basic'] + allow),
                'net':round(obj['basic'] + allow - deduct)
            }
            vals[rs.id] = record

        return vals
    _columns = {
        'basic': fields.function(_calculate_salary, method=True, store=True, multi='dc', type='float', string='Basic Salary', digits=(14,2)),
        'gross': fields.function(_calculate_salary, method=True, store=True, multi='dc', type='float', string='Gross Salary', digits=(14,2)),
        'net': fields.function(_calculate_salary, method=True, store=True, multi='dc', type='float', string='Net Salary', digits=(14,2)),
        'advantages_net': fields.function(_calculate_salary, method=True, store=True, multi='dc', type='float', string='Deductions', digits=(14,2)),
        'advantages_gross': fields.function(_calculate_salary, method=True, store=True, multi='dc', type='float', string='Allowances', digits=(14,2)),
    }
hr_contract()
