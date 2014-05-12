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

class laporan_account_receivable_by_customer(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):

        super(laporan_account_receivable_by_customer, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,
            'isi_laporan' : self.lines,
            'date_header' : self.get_date_header,
        })
        self.context = context
        
    def get_date_header(self, form):
        date_header = form['tanggal'][8:] + '-' + form['tanggal'][5:7] + '-' + form['tanggal'][:4]
        
        return date_header
        
    def get_ar_aging(self, due_date, tanggal):
        
        tanggal_jatuh_tempo = date(int(due_date[0:4]),int(due_date[5:7]),int(due_date[8:10]))
        tanggal_dipilih = date(int(tanggal[0:4]),int(tanggal[5:7]),int(tanggal[8:10]))
        
        ord_tanggal_jatuh_tempo = tanggal_jatuh_tempo.toordinal()
        ord_tanggal_dipilih = tanggal_dipilih.toordinal()
        
        ap_aging = ord_tanggal_dipilih - ord_tanggal_jatuh_tempo

        return ap_aging
        
    def get_currency_rate(self, currency_id, company_currency_id, date_invoice):
        obj_currency = self.pool.get('res.currency')

        rate = obj_currency.compute(self.cr, self.uid, currency_id, company_currency_id, 1,round=True, context={'date' : date_invoice})

        return rate
        
    def lines(self, form):
        no = 1
        aging = ''
        total_sales_received = 0
        obj_account_invoice = self.pool.get('account.invoice')
        
        kriteria = ['|',('date_due','<',form['tanggal']),('date_invoice','<',form['tanggal']),('type','=', 'out_invoice'),('state','=','open'),('partner_id','=',form['partner_id'])]
        
        invoice_ids = obj_account_invoice.search(self.cr, self.uid, kriteria)
        
        if invoice_ids:
            for invoice in obj_account_invoice.browse(self.cr, self.uid, invoice_ids):
                rate = self.get_currency_rate(invoice.currency_id.id, invoice.company_id.currency_id.id, invoice.date_invoice)
                total_sales_received = rate * (invoice.amount_total - invoice.residual)
                if invoice.date_due:
                    aging = invoice.date_due
                elif invoice.date_invoice:
                    aging = invoice.date_invoice
                res = { 
                        'no' : no,
                        'client' : invoice.partner_id.name,
                        'no_invoice' : invoice.number,
                        'sales' : invoice.amount_untaxed or 0,
                        'vat' : invoice.amount_tax or 0,
                        'total' : invoice.amount_total or 0,
                        'ar_aging' : self.get_ar_aging(aging, form['tanggal']),
                        'symbol_invoice' : invoice.currency_id.symbol,
                        'symbol_company' : invoice.company_id.currency_id.symbol,
                        'date_invoice' : invoice.date_invoice[8:] + '-' + invoice.date_invoice[5:7] + '-' + invoice.date_invoice[:4],
                        'exch_rate' : rate,
                        'total_sales_received' : total_sales_received,
                        'ar_balance' : (rate * invoice.amount_total) - total_sales_received
                }
                no += 1
                self.isi_laporan.append(res)

        return self.isi_laporan

report_sxw.report_sxw('report.laporan_account_receivable_by_customer', 'account.invoice','addons/titis/report/laporan_account_receivable_by_customer.rml',parser=laporan_account_receivable_by_customer, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
