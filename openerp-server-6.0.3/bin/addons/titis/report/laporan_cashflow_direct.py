# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from report import report_sxw

class laporan_cashflow_direct(report_sxw.rml_parse):
    _name = 'report.laporan.cashflow.direct'

    def __init__(self, cr, uid, name, context):

        super(laporan_cashflow_direct, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,
            'get_fiscalyear': self._get_fiscal_year,
            'isi_laporan' : self.lines,
        })
        self.context = context
        
    def get_total_per_bulan(self, form, period, account_id, fiscal_year_id, tahun):
        total_str = '0.00'
        total_flt = 0.00
        
        obj_account_move_line = self.pool.get('account.move.line')
        period_id = []
        
        nama_period = period + '/' + tahun

        self.cr.execute("SELECT id FROM account_period WHERE name = '%s' AND fiscalyear_id = %s" % (str(nama_period), fiscal_year_id))
        period_id = self.cr.fetchone()
        
        move_line_ids = obj_account_move_line.search(self.cr, self.uid, [('account_id' , '=' , account_id),('period_id' , '=' , period_id)])

        if move_line_ids:
            for move_line in obj_account_move_line.browse(self.cr, self.uid, move_line_ids):
                total_flt += (move_line.debit - move_line.credit)
            return total_flt
        else:
            return total_str
            
    def get_total_semua_bulan(self, form, account_id, fiscal_year_id):
        total_str = '0.00'
        total_flt = 0
        
        obj_account_move_line = self.pool.get('account.move.line')
        obj_account_period = self.pool.get('account.period')
        
        period_ids = obj_account_period.search(self.cr, self.uid, [('fiscalyear_id' , '=' , fiscal_year_id)])
        
        for period in obj_account_period.browse(self.cr, self.uid, period_ids):
            move_line_ids = obj_account_move_line.search(self.cr, self.uid, [('account_id' , '=' , account_id),('period_id' , '=' , period.id)])
 
            for move_line in obj_account_move_line.browse(self.cr, self.uid, move_line_ids):
                total_flt += (move_line.debit - move_line.credit)
                
        if total_flt and total_flt > 0:
            return total_flt
        else:        
            return total_str

        
    def _get_fiscal_year(self, fiscal_year_id):
        tahun = ''
        obj_fiscal_years = self.pool.get('account.fiscalyear')
        
        if fiscal_year_id:
            fiscal_year_ids = obj_fiscal_years.search(self.cr, self.uid, [('id' , '=' , fiscal_year_id)])

            for fiscal_year in obj_fiscal_years.browse(self.cr, self.uid, fiscal_year_ids):
                tahun = fiscal_year.name
                return tahun        
                                           
        return tahun
        
    def lines(self, form):
        level = 1
        total_jan = 0
        total_feb = 0
        total_mar = 0
        total_apr = 0
        total_mei = 0
        total_jun = 0
        total_jul = 0
        total_aug = 0
        total_sep = 0
        total_okt = 0
        total_nov = 0
        total_des = 0
        total_semua_bulan = 0

        obj_account = self.pool.get('account.account')
        obj_period = self.pool.get('account.period')
        
        tahun = self._get_fiscal_year(form['fiscal_year_id'])
        
        kriteria = [('id', '=', form['account_id'])]
        parent_id = obj_account.search(self.cr, self.uid, kriteria)
        
        ctx = self.context.copy()

        child_ids = obj_account._get_children_and_consol(self.cr, self.uid, parent_id, ctx)

        if child_ids:
            ids = child_ids

        for account in obj_account.browse(self.cr, self.uid, ids):
        
            total_jan += float(self.get_total_per_bulan(form, '01', account.id, form['fiscal_year_id'], tahun))
            total_feb += float(self.get_total_per_bulan(form, '02', account.id, form['fiscal_year_id'], tahun))
            total_mar += float(self.get_total_per_bulan(form, '03', account.id, form['fiscal_year_id'], tahun))
            total_apr += float(self.get_total_per_bulan(form, '04', account.id, form['fiscal_year_id'], tahun))
            total_mei += float(self.get_total_per_bulan(form, '05', account.id, form['fiscal_year_id'], tahun))
            total_jun += float(self.get_total_per_bulan(form, '06', account.id, form['fiscal_year_id'], tahun))
            total_jul += float(self.get_total_per_bulan(form, '07', account.id, form['fiscal_year_id'], tahun))
            total_aug += float(self.get_total_per_bulan(form, '08', account.id, form['fiscal_year_id'], tahun))
            total_sep += float(self.get_total_per_bulan(form, '09', account.id, form['fiscal_year_id'], tahun))
            total_okt += float(self.get_total_per_bulan(form, '10', account.id, form['fiscal_year_id'], tahun))
            total_nov += float(self.get_total_per_bulan(form, '11', account.id, form['fiscal_year_id'], tahun))
            total_des += float(self.get_total_per_bulan(form, '12', account.id, form['fiscal_year_id'], tahun))
            total_semua_bulan += float(self.get_total_semua_bulan(form, account.id, form['fiscal_year_id']))
        
            if account.level < level:
            
                res = {
                    'id' : account.id,
                    'name' : 'Total',
                    'level' : account.level,
                    'jan' : total_jan,
                    'feb' : total_feb,
                    'mar' : total_mar,
                    'apr' : total_apr,
                    'mei' : total_mei,
                    'jun' : total_jun,
                    'jul' : total_jul,
                    'aug' : total_aug,
                    'sep' : total_sep,
                    'okt' : total_okt,
                    'nov' : total_nov,
                    'des' : total_des,
                    'total' : total_semua_bulan,
                    }

                self.isi_laporan.append(res)
                
                res = {
                    'id' : account.id,
                    'name' : account.name,
                    'level' : account.level,
                    'jan' : self.get_total_per_bulan(form, '01', account.id, form['fiscal_year_id'], tahun),
                    'feb' : self.get_total_per_bulan(form, '02', account.id, form['fiscal_year_id'], tahun),
                    'mar' : self.get_total_per_bulan(form, '03', account.id, form['fiscal_year_id'], tahun),
                    'apr' : self.get_total_per_bulan(form, '04', account.id, form['fiscal_year_id'], tahun),
                    'mei' : self.get_total_per_bulan(form, '05', account.id, form['fiscal_year_id'], tahun),
                    'jun' : self.get_total_per_bulan(form, '06', account.id, form['fiscal_year_id'], tahun),
                    'jul' : self.get_total_per_bulan(form, '07', account.id, form['fiscal_year_id'], tahun),
                    'aug' : self.get_total_per_bulan(form, '08', account.id, form['fiscal_year_id'], tahun),
                    'sep' : self.get_total_per_bulan(form, '09', account.id, form['fiscal_year_id'], tahun),
                    'okt' : self.get_total_per_bulan(form, '10', account.id, form['fiscal_year_id'], tahun),
                    'nov' : self.get_total_per_bulan(form, '11', account.id, form['fiscal_year_id'], tahun),
                    'des' : self.get_total_per_bulan(form, '12', account.id, form['fiscal_year_id'], tahun),
                    'total' : self.get_total_semua_bulan(form, account.id, form['fiscal_year_id']),
                    }
            
                level = 1
                
                total_jan = 0
                total_feb = 0
                total_mar = 0
                total_apr = 0
                total_mei = 0
                total_jun = 0
                total_jul = 0
                total_aug = 0
                total_sep = 0
                total_okt = 0
                total_nov = 0
                total_des = 0
                total_semua_bulan = 0
            
            else:
            
                res = {
                    'id' : account.id,
                    'name' : account.name,
                    'level' : account.level,
                    'jan' : self.get_total_per_bulan(form, '01', account.id, form['fiscal_year_id'], tahun),
                    'feb' : self.get_total_per_bulan(form, '02', account.id, form['fiscal_year_id'], tahun),
                    'mar' : self.get_total_per_bulan(form, '03', account.id, form['fiscal_year_id'], tahun),
                    'apr' : self.get_total_per_bulan(form, '04', account.id, form['fiscal_year_id'], tahun),
                    'mei' : self.get_total_per_bulan(form, '05', account.id, form['fiscal_year_id'], tahun),
                    'jun' : self.get_total_per_bulan(form, '06', account.id, form['fiscal_year_id'], tahun),
                    'jul' : self.get_total_per_bulan(form, '07', account.id, form['fiscal_year_id'], tahun),
                    'aug' : self.get_total_per_bulan(form, '08', account.id, form['fiscal_year_id'], tahun),
                    'sep' : self.get_total_per_bulan(form, '09', account.id, form['fiscal_year_id'], tahun),
                    'okt' : self.get_total_per_bulan(form, '10', account.id, form['fiscal_year_id'], tahun),
                    'nov' : self.get_total_per_bulan(form, '11', account.id, form['fiscal_year_id'], tahun),
                    'des' : self.get_total_per_bulan(form, '12', account.id, form['fiscal_year_id'], tahun),
                    'total' : self.get_total_semua_bulan(form, account.id, form['fiscal_year_id']),
                    }
                    
            level = account.level
                
            self.isi_laporan.append(res) 

        return self.isi_laporan                 

report_sxw.report_sxw('report.laporan.cashflow.direct', 'account.account','addons/titis/report/laporan_cashflow_direct.rml',parser=laporan_cashflow_direct, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
