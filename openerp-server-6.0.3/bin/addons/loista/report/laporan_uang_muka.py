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

class laporan_uang_muka(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(laporan_uang_muka, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,
            'isi_laporan' : self.lines,
            'date_from' : self.get_date_header,
            'date_to' : self.get_date_to,
        })
        self.context = context

    def get_date_header(self, form):
        date_header = form['date_from'][8:] + '-' + form['date_from'][5:7] + '-' + form['date_from'][:4]

        return date_header

    def get_date_to(self, form):
        date_to = form['date_to'][8:] + '-' + form['date_to'][5:7] + '-' + form['date_to'][:4]

        return date_to


    def get_ap_aging(self, due_date, date_from):

        tanggal_jatuh_tempo = date(int(due_date[0:4]),int(due_date[5:7]),int(due_date[8:10]))
        tanggal_dipilih = date(int(date_from[0:4]),int(date_from[5:7]),int(date_from[8:10]))

        ord_tanggal_jatuh_tempo = tanggal_jatuh_tempo.toordinal()
        ord_tanggal_dipilih = tanggal_dipilih.toordinal()

        ap_aging = ord_tanggal_dipilih - ord_tanggal_jatuh_tempo

        return ap_aging

    def get_currency_rate(self, currency_id, company_currency_id, date_invoice):
        obj_currency = self.pool.get('res.currency')

        rate = obj_currency.compute(self.cr, self.uid, currency_id, company_currency_id, 1,round=True, context={'date' : date_invoice})

        return rate

    def lines(self, form):
        isi = []
        no = 1
        aging = ''
        tanggal_date_due = ''
        obj_account_invoice = self.pool.get('account.invoice')
        print form['date_from']
        kriteria = [('date_invoice','>=',form['date_from']),('date_invoice','<=',form['date_to']),('type','=', 'in_invoice'),('state','=','paid'),('journal_id','=',form['journal'][0])]

        invoice_ids = obj_account_invoice.search(self.cr, self.uid, kriteria)

        if invoice_ids:
            for invoice in obj_account_invoice.browse(self.cr, self.uid, invoice_ids):
                rate = self.get_currency_rate(invoice.currency_id.id, invoice.company_id.currency_id.id, invoice.date_invoice)
                if invoice.date_due:
                    aging = invoice.date_due
                    tanggal_date_due = invoice.date_due[8:] + '-' + invoice.date_due[5:7] + '-' + invoice.date_due[:4] or '-'
                elif invoice.date_invoice:
                    aging = invoice.date_invoice
                    tanggal_date_due = '-'

                res = {
                        'no' : no,
                        'supplier' : invoice.partner_id.name,
                        'no_invoice' : invoice.number,
                        'ap_amount' : invoice.amount_untaxed or 0,
                        'vat' : invoice.amount_tax or 0,
                        'acc_payable_balance' : invoice.amount_total or 0,
                        'ap_aging' : self.get_ap_aging(aging, form['date_from']),
                        'exch_rate' : rate,
                        'symbol_invoice' : invoice.currency_id.symbol,
                        'symbol_company' : invoice.company_id.currency_id.symbol,
                        'date_invoice' : invoice.date_invoice[8:] + '-' + invoice.date_invoice[5:7] + '-' + invoice.date_invoice[:4],
                        'date_due' : tanggal_date_due,
                        'acc_payable_balance_rp' : invoice.amount_total * rate or 0,
                        'ref': invoice.reference,
                }
                no += 1
                self.isi_laporan.append(res)

        return self.isi_laporan

report_sxw.report_sxw('report.laporan_uang_muka', 'account.invoice','addons/loista/report/laporan_uang_muka.rml',parser=laporan_uang_muka, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
