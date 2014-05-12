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
from osv import osv
import locale

class laporan_sales_report_customer(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):

        super(laporan_sales_report_customer, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.tanggal_mulai = ''
        self.tanggal_akhir = ''
        self.jml_total_inv_rp = 0
        self.jml_sub_total = 0
        self.jml_total_sales_rp = 0
        self.jml_total_inv = 0
        self.localcontext.update({
            'time': time,
			'tanggal_mulai' : self.get_tanggal_mulai,   
			'tanggal_akhir' : self.get_tanggal_akhir, 
            'isi_laporan' : self.lines,
            'jml_total_inv_rp' : self.get_jml_total_inv_rp,
            'jml_total_sales_rp' : self.get_jml_total_sales_rp,
            'jml_sub_total' : self.get_jml_sub_total,
            'jml_total_inv' : self.get_jml_total_inv,
            'locale':locale,
        })
        self.context = context
    
    def lines (self, form):
        obj_invoice = self.pool.get('account.invoice')
        obj_currency = self.pool.get('res.currency')
        down_pymt = 0
        sub_total = 0
        jml_total_inv_rp = 0
        jml_total_sales_rp = 0
        jml_sub_total = 0
        jml_total_inv = 0
        exct_rate = 0

        invoice_ids = obj_invoice.search(self.cr, self.uid, [('partner_id', '=', form['konsumen_id']), ('type', '=', 'out_invoice'), ('date_invoice','>=',form['tanggal_mulai']), ('date_invoice','<=',form['tanggal_akhir']), ('state','in',('open','paid'))])
        
        no = 1
        for invoice in obj_invoice.browse(self.cr, self.uid, invoice_ids):
            exct_rate = obj_currency.compute(self.cr, self.uid, invoice.currency_id.id, invoice.company_id.currency_id.id, 1,round=True, context={'date' : invoice.date_invoice})
            jml_sub_total = invoice.amount_untaxed - down_pymt
            jml_total_inv = jml_sub_total + invoice.amount_tax

            res = {
                        'no' : no,
                        'simbol_currency' : invoice.currency_id.symbol,
                        'client' : invoice.partner_id.name,
                        'project_code' : '',
                        'ipc_number' : '',
                        'description' : invoice.name,
                        'date_invoice' : invoice.date_invoice,
                        'number_invoice' : invoice.number,
                        'sales' : invoice.amount_untaxed,
                        'down_pymt' : down_pymt,
                        'sub_total' : jml_sub_total,
                        'vat' : invoice.amount_tax,
                        'total_inv' : jml_total_inv,
                        'exct_rate' : exct_rate,
                        'total_inv_rp' : jml_total_inv * exct_rate,
                        'total_sales_rp' :  jml_sub_total * exct_rate,
                    }
            no = no + 1
            self.isi_laporan.append(res)
            self.jml_total_inv_rp += jml_total_inv * exct_rate
            self.jml_total_sales_rp += jml_sub_total * exct_rate
        return self.isi_laporan

    def get_jml_total_sales_rp(self, form):
        return self.jml_total_sales_rp

    def get_jml_total_inv_rp(self, form):
        return self.jml_total_inv_rp

    def get_jml_sub_total(self, form):
        return self.jml_sub_total

    def get_jml_total_inv(self, form):
        return self.jml_total_inv

    def get_tanggal_mulai(self, form):
        tanggal_mulai = '%s/%s/%s' % (form['tanggal_mulai'][8:10], form['tanggal_mulai'][5:7], form['tanggal_mulai'][0:4]) 
        return tanggal_mulai

    def get_tanggal_akhir(self, form):
        tanggal_akhir = '%s/%s/%s' % (form['tanggal_akhir'][8:10], form['tanggal_akhir'][5:7], form['tanggal_akhir'][0:4]) 
        return tanggal_akhir

report_sxw.report_sxw('report.laporan_sales_report_customer', 'account.invoice','addons/titis/report/laporan_sales_report_customer.rml',parser=laporan_sales_report_customer, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
