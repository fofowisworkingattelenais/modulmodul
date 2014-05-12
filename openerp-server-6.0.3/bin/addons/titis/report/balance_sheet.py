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


import xml
import copy
from operator import itemgetter
import time
import datetime
from report import report_sxw

class balance_sheet(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(balance_sheet, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.total_saldo_periode = 0
        self.total_saldo_fiscal_year = 0
        self.localcontext.update({
            'time': time,
            'isi_laporan' : self.lines,
            'tanggal_mulai' : self.get_tanggal_mulai,
            'tanggal_akhir' : self.get_tanggal_akhir,
            'periode' : self.get_periode,
            'periode_tabel_header' : self.get_periode_tabel_header,
            'tahun_sebelumnya' : self.get_tahun_sebelumnya,
        })
        self.context = context
        
    def get_periode(self, form):
        periode = ''
        obj_period = self.pool.get('account.period')
        
        kriteria = [ ('id','=', form['period_id']) ]
        
        period_ids = obj_period.search(self.cr, self.uid, kriteria)

        for period in obj_period.browse(self.cr, self.uid, period_ids):
            if period:
                periode = period.date_stop[8:] + ' ' + self.get_nama_periode(period.id) + ' ' + period.date_stop[:4] + ' DAN ' + '31 DESEMBER ' + str(int( period.date_stop[:4] )-1)
                
        return periode
        
    def get_nama_periode(self, period_id):
        obj_period = self.pool.get('account.period')
        nama_bulan = ''
        
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
        
    def get_nama_periode_singkatan(self, period_id):
        obj_period = self.pool.get('account.period')
        nama_bulan = ''
        
        bulan = {
                '01' : 'JAN',
                '02' : 'FEB',
                '03' : 'MAR',
                '04' : 'APR',
                '05' : 'MEI',
                '06' : 'JUN',
                '07' : 'JUL',
                '08' : 'AGS',
                '09' : 'SEPT',
                '10' : 'OKT',
                '11' : 'NOV',
                '12' : 'DES'
                }

        if period_id:
            period_ids = obj_period.search(self.cr, self.uid, [('id' , '=' , period_id)])

            for period in obj_period.browse(self.cr, self.uid, period_ids):
                cari_bulan = period.id and period.name[0:2]
                nama_bulan = bulan.get(cari_bulan, False)
                if not nama_bulan:
                    nama_bulan = '-'
        return nama_bulan
        
    def get_periode_tabel_header(self, form):
        periode = ''
        obj_period = self.pool.get('account.period')
        
        kriteria = [ ('id','=', form['period_id']) ]
        
        period_ids = obj_period.search(self.cr, self.uid, kriteria)

        for period in obj_period.browse(self.cr, self.uid, period_ids):
            if period:
                periode = self.get_nama_periode_singkatan(period.id) + '-' + period.date_stop[2:4]
                
        return periode
        
    def _get_fiscal_year(self, fiscal_year_id):
        tahun = ''
        obj_fiscal_years = self.pool.get('account.fiscalyear')
        
        if fiscal_year_id:
            fiscal_year_ids = obj_fiscal_years.search(self.cr, self.uid, [('id' , '=' , fiscal_year_id)])

            for fiscal_year in obj_fiscal_years.browse(self.cr, self.uid, fiscal_year_ids):
                tahun = fiscal_year.name
                return tahun        
                                           
        return tahun
        
    def get_tahun_sebelumnya(self, form):
        tahun_sebelumnya = ''
        obj_period = self.pool.get('account.period')
        
        kriteria = [ ('id','=', form['period_id']) ]
        
        period_ids = obj_period.search(self.cr, self.uid, kriteria)

        for period in obj_period.browse(self.cr, self.uid, period_ids):
            if period:
                tahun_sebelumnya = str(int( period.date_stop[:4] )-1)
                
        return tahun_sebelumnya
        
        
    def get_saldo_periode(self, period_id, account_id):
        saldo = 0
        obj_account_move_line = self.pool.get('account.move.line')
        
        move_line_ids = []
        
        sql_string =    """
                        SELECT  A.id AS id
                        FROM    account_move_line AS A
                        JOIN    account_move AS B ON A.move_id=B.id
                        WHERE   a.period_id = %s AND
                                A.account_id = %s AND
                                A.state = 'valid'
                        ORDER BY    B.date
                        """ % (period_id, account_id)
                        
        self.cr.execute(sql_string)
        for (move_id) in self.cr.fetchall():
            move_line_ids.append(move_id[0])
            
        if move_line_ids:
            for account_move_line in obj_account_move_line.browse(self.cr, self.uid, move_line_ids):
                saldo += (account_move_line.debit - account_move_line.credit)

        return saldo
        
    def get_saldo_fiscal_year(self, fiscal_year_id, account_id):
        saldo = 0
        move_line_ids = []
        list_period = []

        obj_account_move_line = self.pool.get('account.move.line')
        obj_fiscal_years = self.pool.get('account.fiscalyear')
        obj_period = self.pool.get('account.period')
        
        tahun = self._get_fiscal_year(fiscal_year_id)
        
        if tahun:
        
            tahun_sebelumnya = str(int(tahun) - 1)
            
            fiscal_year_id = obj_fiscal_years.search(self.cr, self.uid, [('name','=',tahun_sebelumnya)])
            if not fiscal_year_id:
                return False
            
            period_ids = obj_period.search(self.cr, self.uid, [('fiscalyear_id','=',fiscal_year_id)])
            
            for period in obj_period.browse(self.cr, self.uid, period_ids):
                list_period.append(period.id)
            
            sql_string =    """
                            SELECT  A.id AS id
                            FROM    account_move_line AS A
                            JOIN    account_move AS B ON A.move_id=B.id
                            WHERE   a.period_id in %s AND
                                    A.account_id = %s AND
                                    A.state = 'valid'
                            ORDER BY    B.date
                            """ % (tuple(list_period), account_id)
                            
            self.cr.execute(sql_string)
            for (move_id) in self.cr.fetchall():
                move_line_ids.append(move_id[0])
                
            if move_line_ids:
                for account_move_line in obj_account_move_line.browse(self.cr, self.uid, move_line_ids):
                    saldo += (account_move_line.debit - account_move_line.credit)

        return saldo
        
    def lines(self, form):
        def _process_child(accounts, parent, level):

            account_rec = [acct for acct in accounts if acct['id'] == parent][0] 
            
            saldo_periode = self.get_saldo_periode(form['period_id'], account_rec['id'])
            saldo_fiscal_year = self.get_saldo_fiscal_year(form['fiscal_year_id'], account_rec['id'])
            
            self.total_saldo_periode += saldo_periode
            self.total_saldo_fiscal_year += saldo_fiscal_year
            

            res = {
                'id' : account_rec['id'],
                'type' : account_rec['type'],
                'code' : account_rec['code'],
                'name' : account_rec['name'],
                'level' : level,
                'debit' : account_rec['debit'],
                'credit' : account_rec['credit'],
                'balance' : account_rec['balance'],
                'parent_id' : account_rec['parent_id'],
                'saldo_periode' : saldo_periode,
                'saldo_fiscal_year' : saldo_fiscal_year,
                }
                
            res1 = {
                'id' : 0,
                'type' : 'view',
                'code' : '',
                'name' : 'Total ' + account_rec['name'],
                'level' : level,
                'debit' : account_rec['debit'],
                'credit' : account_rec['credit'],
                'balance' : account_rec['balance'],
                'parent_id' : account_rec['parent_id'],
                'saldo_periode' : self.total_saldo_periode,
                'saldo_fiscal_year' : self.total_saldo_fiscal_year,
                }                                                         

            self.isi_laporan.append(res)          

            if account_rec['child_id']:
                level += 1
                for child in account_rec['child_id']:
                    _process_child(accounts, child, level)
                    
            if account_rec['type'] == 'view':
                self.isi_laporan.append(res1)

    
        obj_account_acoount = self.pool.get('account.account')
        obj_users = self.pool.get('res.users')
        
        ids = {}
        done = None
        level = 1
        user = obj_users.browse(self.cr, self.uid, [self.uid])[0]
              
        ctx = self.context.copy()
        ctx['date_from'] = self.get_tanggal_mulai(form)
        ctx['date_to'] =  self.get_tanggal_akhir(form)

        akun_aktiva_id = user.company_id.account_aktiva_id.id
        akun_kewajiban_id = user.company_id.account_kewajiban_id.id
        akun_ekuitas_id = user.company_id.account_ekuitas_id.id
        
        kriteria = [('id', 'in', [akun_aktiva_id, akun_kewajiban_id, akun_ekuitas_id])]
        ids = obj_account_acoount.search(self.cr, self.uid, kriteria)

        parents = ids
             
        child_ids = obj_account_acoount._get_children_and_consol(self.cr, self.uid, ids, ctx)

        if child_ids:
            ids = child_ids

        account_fields = ['type', 'code', 'name', 'debit', 'credit', 'balance', 'parent_id', 'child_id']
        accounts = obj_account_acoount.read(self.cr, self.uid, ids, account_fields, ctx)
     
        for parent in parents:
            level = 1
            
            _process_child(accounts, parent, level)

        return self.isi_laporan        
        
    def get_tanggal_mulai(self, form):
        obj_periode = self.pool.get('account.period')
        periode = obj_periode.browse(self.cr, self.uid, [form['period_id']])[0]
        
        return periode.fiscalyear_id.date_start
        
    def get_tanggal_akhir(self, form):
        obj_periode = self.pool.get('account.period')
        periode = obj_periode.browse(self.cr, self.uid, [form['period_id']])[0]
        
        return periode.date_stop   

report_sxw.report_sxw('report.balance_sheet', 'account.account','addons/titis/report/balance_sheet.rml',parser=balance_sheet, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
