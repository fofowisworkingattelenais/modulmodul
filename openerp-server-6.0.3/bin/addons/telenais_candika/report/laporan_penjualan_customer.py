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

import xml
import copy
from operator import itemgetter
import time
import datetime
from report import report_sxw

class laporan_penjualan_customer(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(laporan_penjualan_customer, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,
            'isi_laporan' : self.lines,
            'periode_mulai' : self.get_nama_periode_mulai,
            'periode_akhir' : self.get_nama_periode_akhir,
            'tahun_mulai' : self.get_fiscal_year_mulai,
            'tahun_akhir' : self.get_fiscal_year_akhir,
        })
        self.context = context
        
    def get_fiscal_year_mulai(self, form):
        tahun = ''
        obj_fiscal_years = self.pool.get('account.fiscalyear')
        obj_period = self.pool.get('account.period')
        period_id = form['period_mulai_id']
        
        if period_id:
            period_ids = obj_period.search(self.cr, self.uid, [('id' , '=' , period_id)])
            
            for period in obj_period.browse(self.cr, self.uid, period_ids):

                fiscal_year_ids = obj_fiscal_years.search(self.cr, self.uid, [('id' , '=' , period.fiscalyear_id.id)])

                for fiscal_year in obj_fiscal_years.browse(self.cr, self.uid, fiscal_year_ids):
                    tahun = fiscal_year.code
                    return tahun        
                                           
        return tahun

    def get_fiscal_year_akhir(self, form):
        tahun = ''
        obj_fiscal_years = self.pool.get('account.fiscalyear')
        obj_period = self.pool.get('account.period')
        period_id = form['period_akhir_id']
        
        if period_id:
            period_ids = obj_period.search(self.cr, self.uid, [('id' , '=' , period_id)])
            
            for period in obj_period.browse(self.cr, self.uid, period_ids):

                fiscal_year_ids = obj_fiscal_years.search(self.cr, self.uid, [('id' , '=' , period.fiscalyear_id.id)])

                for fiscal_year in obj_fiscal_years.browse(self.cr, self.uid, fiscal_year_ids):
                    tahun = fiscal_year.code
                    return tahun         
                                           
        return tahun
        
    def get_nama_periode_mulai(self, form):
        obj_period = self.pool.get('account.period')
        period_id = form['period_mulai_id']
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
        
    def get_nama_periode_akhir(self, form):
        obj_period = self.pool.get('account.period')
        period_id = form['period_akhir_id']
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
        
    def get_nama_brand(self, categ_id):
        nama_brand = ''
        obj_product_category = self.pool.get('product.category')
        
        if categ_id:
            categ_ids = obj_product_category.search(self.cr, self.uid, [('id' , '=' , categ_id)])
            
            for categ in obj_product_category.browse(self.cr, self.uid, categ_ids):
                nama_brand = categ.parent_id.parent_id.name
                                           
        return nama_brand
        
    def get_reg(self, period_mulai_id, period_akhir_id, partner_id, account_penjualan_id, product_id):
        query = {}
        req = 0
        i = 0

        sql_string =    """
                        SELECT 	SUM(A.quantity) AS qty
                        FROM 	account_move_line A 
                        JOIN    account_move B ON B.id = A.move_id
                        JOIN    product_product C ON C.id = A.product_id
                        WHERE 	B.state = 'posted' AND
                                A.partner_id = %s AND
                                A.account_id = %s AND
                                A.product_id = %s AND
                                B.period_id BETWEEN %s AND %s
                        """ % (partner_id, account_penjualan_id, product_id, period_mulai_id, period_akhir_id)
                        
        self.cr.execute(sql_string)
                        
        query = self.cr.dictfetchall()
        
        if i < len(query):
            while i < len(query):
                req = query[i]['qty']
                i += 1
    
        return req
        
    def get_cons(self, period_mulai_id, period_akhir_id, partner_id, account_konsiensi_penjualan_id, product_id):
        query = {}
        i = 0

        sql_string =    """
                        SELECT 	SUM(A.quantity) AS qty
                        FROM 	account_move_line A 
                        JOIN    account_move B ON B.id = A.move_id
                        JOIN    product_product C ON C.id = A.product_id
                        WHERE 	B.state = 'posted' AND
                                A.partner_id = %s AND
                                A.account_id = %s AND
                                A.product_id = %s AND
                                B.period_id BETWEEN %s AND %s
                        """ % (partner_id, account_konsiensi_penjualan_id, product_id, period_mulai_id, period_akhir_id)
                        
        self.cr.execute(sql_string)
                        
        query = self.cr.dictfetchall()
        
        if i < len(query):
            while i < len(query):
                req = query[i]['qty'] or 0
                i += 1
    
        return req
        
    def get_retur(self, period_mulai_id, period_akhir_id, partner_id, account_retur_id, product_id):
        query = {}
        i = 0

        sql_string =    """
                        SELECT 	SUM(A.quantity) * -1 AS qty
                        FROM 	account_move_line A 
                        JOIN    account_move B ON B.id = A.move_id
                        JOIN    product_product C ON C.id = A.product_id
                        WHERE 	B.state = 'posted' AND
                                A.partner_id = %s AND
                                A.account_id = %s AND
                                A.product_id = %s AND
                                B.period_id BETWEEN %s AND %s
                        """ % (partner_id, account_retur_id, product_id, period_mulai_id, period_akhir_id)
                        
        self.cr.execute(sql_string)
                        
        query = self.cr.dictfetchall()
        
        if i < len(query):
            while i < len(query):
                req = query[i]['qty'] or 0
                i += 1
    
        return req
        
    def get_diskon(self, period_mulai_id, period_akhir_id, partner_id, account_diskon_id, product_id):
        query = {}
        i = 0

        sql_string =    """
                        SELECT 	abs(SUM(A.debit-A.credit)) AS qty
                        FROM 	account_move_line A 
                        JOIN    account_move B ON B.id = A.move_id
                        JOIN    product_product C ON C.id = A.product_id
                        WHERE 	B.state = 'posted' AND
                                A.partner_id = %s AND
                                A.account_id = %s AND
                                A.product_id = %s AND
                                B.period_id BETWEEN %s AND %s
                        """ % (partner_id, account_diskon_id, product_id, period_mulai_id, period_akhir_id)
                        
        self.cr.execute(sql_string)
                        
        query = self.cr.dictfetchall()
        
        if i < len(query):
            while i < len(query):
                req = query[i]['qty'] or 0
                i += 1
    
        return req
        
    def get_gross(self, period_mulai_id, period_akhir_id, partner_id, account_penjualan_id, account_konsiensi_penjualan_id, account_retur_id, product_id):
        query = {}
        query_2 = {}
        i = 0
        x = 0

        sql_string =    """
                        SELECT 	abs(SUM(A.debit-A.credit)) AS qty
                        FROM 	account_move_line A 
                        JOIN    account_move B ON B.id = A.move_id
                        JOIN    product_product C ON C.id = A.product_id
                        WHERE 	B.state = 'posted' AND
                                A.partner_id = %s AND
                                A.account_id in (%s,%s) AND
                                A.product_id = %s AND
                                B.period_id BETWEEN %s AND %s
                        """ % (partner_id, account_penjualan_id, account_konsiensi_penjualan_id, product_id, period_mulai_id, period_akhir_id)
                        
        self.cr.execute(sql_string)
                        
        query = self.cr.dictfetchall()
        
        if i < len(query):
            while i < len(query):
                total_penjualan = query[i]['qty'] or 0
                i += 1
                
        if account_retur_id:
            sql_string_2 =    """
                            SELECT 	abs(SUM(A.debit-A.credit)) * -1 AS qty
                            FROM 	account_move_line A 
                            JOIN    account_move B ON B.id = A.move_id
                            JOIN    product_product C ON C.id = A.product_id
                            WHERE 	B.state = 'posted' AND
                                    A.partner_id = %s AND
                                    A.account_id = %s AND
                                    A.product_id = %s AND
                                    B.period_id BETWEEN %s AND %s
                            """ % (partner_id, account_retur_id, product_id, period_mulai_id, period_akhir_id)
                        
        self.cr.execute(sql_string_2)
                        
        query_2 = self.cr.dictfetchall()
        
        if x < len(query_2):
            while x < len(query_2):
                total_retur = query_2[x]['qty'] or 0
                x += 1
                
        if total_retur:
            total = total_penjualan + total_retur
        else:
            total = total_penjualan
    
        return total
        
    def lines (self, form):
        detail_laporan = []
        detail_sub_header = []
        move_ids = []
        query_header = {}  
        query_detail = {} 
        i = 0
        
        reg = 0
        cons = 0
        retur = 0
        gross = 0
        diskon = 0
        sub_total = 0
        
        total_sub_total_sub_header = 0
        total_diskon_sub_header = 0
        total_gross_sub_header = 0
        total_retur_sub_header = 0
        total_cons_sub_header = 0
        total_reg_sub_header = 0
        
        total_sub_total_header = 0
        total_diskon_header = 0
        total_gross_header = 0
        total_retur_header = 0
        total_cons_header = 0
        total_reg_header = 0
        
        obj_account_move_line = self.pool.get('account.move.line')
        obj_users = self.pool.get('res.users')
        
        user = obj_users.browse(self.cr, self.uid, [self.uid])[0]
        
        default_account_diskon_id = int(user.company_id.default_account_diskon_id.id)
        default_account_penjualan_id = int(user.company_id.default_account_penjualan_id.id)
        default_account_konsiensi_penjualan_id = int(user.company_id.default_account_konsiensi_penjualan_id.id)
        default_account_retur_id = int(user.company_id.default_account_retur_id.id)
        
        period_mulai_id = form['period_mulai_id']
        period_akhir_id = form['period_akhir_id']
        
        sql_header =    """
                        SELECT 	DISTINCT A.partner_id,
                                B.name,
                                B.ref 
                        FROM 	account_move_line A 
                        JOIN    res_partner B ON B.id = A.partner_id
                        WHERE 	A.partner_id is not null AND
                                A.period_id BETWEEN %s AND %s
                        """ % (period_mulai_id, period_akhir_id)
                        
        self.cr.execute(sql_header)
                        
        query_header = self.cr.dictfetchall()
        
        if i < len(query_header):
            while i < len(query_header):
                detail_sub_header = []
                y = 0
                
                sql_sub_header =    """
                                    SELECT 	DISTINCT D.categ_id,
                                            E.name
                                    FROM 	account_move_line A 
                                    JOIN    account_move B ON B.id = A.move_id
                                    JOIN    product_product C ON C.id = A.product_id
                                    JOIN	product_template D ON D.id = C.product_tmpl_id
                                    JOIN	product_category E ON E.id = D.categ_id
                                    WHERE 	B.state = 'posted' AND
                                            A.partner_id = %s AND
                                            A.period_id BETWEEN %s AND %s
                                """ % (query_header[i]['partner_id'],period_mulai_id, period_akhir_id)
                                
                self.cr.execute(sql_sub_header)
                                
                query_sub_header = self.cr.dictfetchall()
                
                if y < len(query_sub_header):
                    while y < len(query_sub_header):
            
                        detail_laporan = []
                        x = 0
                        sub_total = 0
                        
                        sql_detail =    """
                                        SELECT 	DISTINCT A.product_id,
                                                D.name,
                                                C.default_code
                                        FROM 	account_move_line A 
                                        JOIN    account_move B ON B.id = A.move_id
                                        JOIN    product_product C ON C.id = A.product_id
                                        JOIN	product_template D ON D.id = C.product_tmpl_id
                                        WHERE 	B.state = 'posted' AND
                                                A.partner_id = %s AND
                                                A.account_id in %s AND
                                                D.categ_id = %s AND
                                                A.period_id BETWEEN %s AND %s
                                        """ % (query_header[i]['partner_id'], (default_account_diskon_id, default_account_penjualan_id, default_account_konsiensi_penjualan_id, default_account_retur_id), query_sub_header[y]['categ_id'],period_mulai_id, period_akhir_id )
                                        
                        self.cr.execute(sql_detail)
                                        
                        query_detail = self.cr.dictfetchall()
                        
                        if x < len(query_detail):
                            while x < len(query_detail):
                                reg = self.get_reg(period_mulai_id, period_akhir_id, query_header[i]['partner_id'], default_account_penjualan_id, query_detail[x]['product_id'])
                                cons = self.get_cons(period_mulai_id, period_akhir_id, query_header[i]['partner_id'], default_account_konsiensi_penjualan_id, query_detail[x]['product_id'])
                                retur = self.get_retur(period_mulai_id, period_akhir_id, query_header[i]['partner_id'], default_account_retur_id, query_detail[x]['product_id'])
                                gross = self.get_gross(period_mulai_id, period_akhir_id, query_header[i]['partner_id'], default_account_penjualan_id, default_account_konsiensi_penjualan_id, default_account_retur_id, query_detail[x]['product_id'])
                                diskon = self.get_diskon(period_mulai_id, period_akhir_id, query_header[i]['partner_id'], default_account_diskon_id, query_detail[x]['product_id'])
                                
                                if diskon:
                                    sub_total = gross - diskon
                                else:
                                    sub_total = gross
                        
                                res_detail = {
                                            'kode_produk' : query_detail[x]['default_code'],
                                            'nama_produk' : query_detail[x]['name'],
                                            'reg' : reg,
                                            'cons' : cons,
                                            'retur' : retur,
                                            'gross' : gross,
                                            'diskon' : diskon,
                                            'sub_total' : sub_total
                                        }
                                        
                                detail_laporan.append(res_detail)
                                
                                total_sub_total_sub_header += sub_total
                                total_diskon_sub_header += diskon
                                total_gross_sub_header += gross
                                total_retur_sub_header += retur
                                total_cons_sub_header += cons
                                if reg:
                                    total_reg_sub_header += reg
                                
                                x+=1
                                
                        if query_detail:
                            res_sub_header = {
                                        'nama_categori' : query_sub_header[y]['name'],
                                        'nama_brand' : self.get_nama_brand(query_sub_header[y]['categ_id']),
                                        'detail' : detail_laporan,
                                        'total_sub_total_sub_header' : total_sub_total_sub_header,
                                        'total_diskon_sub_header' : total_diskon_sub_header,
                                        'total_gross_sub_header' : total_gross_sub_header,
                                        'total_retur_sub_header' : total_retur_sub_header,
                                        'total_cons_sub_header' : total_cons_sub_header,
                                        'total_reg_sub_header' : total_reg_sub_header
                                    }
                            
                            detail_sub_header.append(res_sub_header)
                            
                            total_sub_total_header += total_sub_total_sub_header
                            total_diskon_header += total_diskon_sub_header
                            total_gross_header += total_gross_sub_header
                            total_retur_header += total_retur_sub_header
                            total_cons_header += total_cons_sub_header
                            total_reg_header += total_reg_sub_header
                            
                            total_sub_total_sub_header = 0
                            total_diskon_sub_header = 0
                            total_gross_sub_header = 0
                            total_retur_sub_header = 0
                            total_cons_sub_header = 0
                            total_reg_sub_header = 0
                            
                        y+=1
                        
                if detail_sub_header:
                        
                    res = {
                                'partner_id' : query_header[i]['name'],
                                'partner_code' : '-',
                                'sub_header' : detail_sub_header,
                                'total_sub_total_header' : total_sub_total_header,
                                'total_diskon_header' : total_diskon_header,
                                'total_gross_header' : total_gross_header,
                                'total_retur_header' : total_retur_header,
                                'total_cons_header' : total_cons_header,
                                'total_reg_header' : total_reg_header
                            }
                    self.isi_laporan.append(res)
                    
                    total_sub_total_header = 0
                    total_diskon_header = 0
                    total_gross_header = 0
                    total_retur_header = 0
                    total_cons_header = 0
                    total_reg_header = 0 
                
                i+=1

        return self.isi_laporan 

report_sxw.report_sxw('report.laporan_penjualan_customer', 'account.move.line', 'addons/telenais_candika/report/laporan_penjualan_customer.rml', parser=laporan_penjualan_customer, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
