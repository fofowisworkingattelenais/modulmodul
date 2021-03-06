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


from datetime import time, date, datetime
from report import report_sxw

class department_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):

        super(department_report, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,
            'isi_laporan' : self.lines,
            'nama_budget' : self.get_nama_budget,
            'nama_analytic' : self.get_nama_analytic,
            'nama_periode' : self.get_nama_periode,
        })
        self.context = context
        
    def get_nama_periode(self, form):
        obj_period = self.pool.get('account.period')
        nama_bulan = ''
        period_id = form['period_id']
        
        bulan = {
                '01' : 'JANUARI',
                '02' : 'FEBRUARI',
                '03' : 'MARET',
                '04' : 'APRIL',
                '05' : 'MEI',
                '06' : 'JUNI',
                '07' : 'JULI',
                '08' : 'AGUSTUS',
                '09' : 'SEPTEMBER',
                '10' : 'OKTOBER',
                '11' : 'NOVEMBER',
                '12' : 'DESEMBER'
                }

        if period_id:
            period_ids = obj_period.search(self.cr, self.uid, [('id' , '=' , period_id)])

            for period in obj_period.browse(self.cr, self.uid, period_ids):
                cari_bulan = period.id and period.name[0:2]
                nama_bulan = bulan.get(cari_bulan, False)
                if not nama_bulan:
                    nama_bulan = '-'
        return nama_bulan
        
    def get_date_start(self, form):
        obj_period = self.pool.get('account.period')
        period_id = form['period_id']
      
        if period_id:
            period_ids = obj_period.search(self.cr, self.uid, [('id' , '=' , period_id)])

            for period in obj_period.browse(self.cr, self.uid, period_ids):
               return period.date_start
               
    def get_date_stop(self, form):
        obj_period = self.pool.get('account.period')
        period_id = form['period_id']
      
        if period_id:
            period_ids = obj_period.search(self.cr, self.uid, [('id' , '=' , period_id)])

            for period in obj_period.browse(self.cr, self.uid, period_ids):
               return period.date_stop
        
    def get_nama_budget(self, form):
        nama_budget = ''
        obj_account_budget = self.pool.get('crossovered.budget')
        
        kriteria = [ ('id','=',form['crossovered_budget_id']) ]
        
        budget_line_ids = obj_account_budget.search(self.cr, self.uid, kriteria)
        
        for budget in obj_account_budget.browse(self.cr, self.uid, budget_line_ids):
            if budget:
                nama_budget = budget.name

        return nama_budget   
        
    def get_nama_analytic(self, form):
        nama_analytic = ''
        obj_account_analytic = self.pool.get('account.analytic.account')
        
        kriteria = [ ('id','=',form['analytic_account_id']) ]
        
        analytic_line_ids = obj_account_analytic.search(self.cr, self.uid, kriteria)
        
        for analytic in obj_account_analytic.browse(self.cr, self.uid, analytic_line_ids):
            if analytic:
                nama_analytic = analytic.name

        return nama_analytic
        
    def get_realisasi_sampai_bulan_ini(self, date_stop, crossovered_budget_id, analytic_account_id):
        realisasi_sampai_bulan_ini = 0.00
        obj_account_budget_lines = self.pool.get('crossovered.budget.lines')
        
        kriteria = [ ('crossovered_budget_id','=', crossovered_budget_id),('analytic_account_id','=', analytic_account_id),('date_to','<=',date_stop) ]
        
        budget_line_ids = obj_account_budget_lines.search(self.cr, self.uid, kriteria)
        
        for budget_line in obj_account_budget_lines.browse(self.cr, self.uid, budget_line_ids):
            if budget_line:
                realisasi_sampai_bulan_ini += budget_line.practical_amount
        return realisasi_sampai_bulan_ini
        
    def get_budget_sampai_bulan_ini(self, date_stop, crossovered_budget_id, analytic_account_id):
        budget_sampai_bulan_ini = 0.00
        obj_account_budget_lines = self.pool.get('crossovered.budget.lines')
        
        kriteria = [ ('crossovered_budget_id','=', crossovered_budget_id),('analytic_account_id','=', analytic_account_id),('date_to','<=',date_stop) ]
        
        budget_line_ids = obj_account_budget_lines.search(self.cr, self.uid, kriteria)
        
        for budget_line in obj_account_budget_lines.browse(self.cr, self.uid, budget_line_ids):
            if budget_line:
                budget_sampai_bulan_ini += budget_line.planned_amount
        return budget_sampai_bulan_ini
        
    def lines (self, form):
        date_start = self.get_date_start(form)
        date_stop = self.get_date_stop(form)
        obj_account_budget_lines = self.pool.get('crossovered.budget.lines')
        crossovered_budget_id = form['crossovered_budget_id']
        
        kriteria = [ ('crossovered_budget_id','=',crossovered_budget_id),('date_from','>=',date_start),('date_to','<=',date_stop) ]
        
        budget_line_ids = obj_account_budget_lines.search(self.cr, self.uid, kriteria)
        
        for budget_line in obj_account_budget_lines.browse(self.cr, self.uid, budget_line_ids):
            res = {
                        'no_account' : budget_line.general_budget_id.code,
                        'uraian' : budget_line.general_budget_id.name,
                        'realisasi_bulan_ini' : budget_line.practical_amount or 0.00,
                        'budget_bulan_ini' : budget_line.planned_amount or 0.00,
                        'persentase_bulan_ini' : budget_line.percentage or 0,
                        'realisasi_sd_bulan_ini' : self.get_realisasi_sampai_bulan_ini(date_stop, crossovered_budget_id, budget_line.analytic_account_id.id),
                        'budget_sd_bulan_ini' : self.get_budget_sampai_bulan_ini(date_stop, crossovered_budget_id, budget_line.analytic_account_id.id),
                        'persentase_sd_bulan_ini' : '-',
                      
                    }
            self.isi_laporan.append(res)

        return self.isi_laporan     

report_sxw.report_sxw('report.department_report', 'account.account','addons/titis/report/department_report.rml',parser=department_report, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
