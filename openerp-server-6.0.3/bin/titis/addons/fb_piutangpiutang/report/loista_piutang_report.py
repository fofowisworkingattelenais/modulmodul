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

class loista_piutang_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(loista_piutang_report, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,
            'isi_laporan' : self.lines,
            'date_header' : self.get_date_header,
            'date_from' : self.get_from_date_header,
            'date_to' : self.get_to_date_header,


        })
        self.context = context

    def get_date_header(self, form):
        date_header = form['tanggal'][8:] + '-' + form['tanggal'][5:7] + '-' + form['tanggal'][:4]

        return date_header

    def get_from_date_header(self, form):
        date_header = form['from_date'][8:] + '-' + form['from_date'][5:7] + '-' + form['from_date'][:4]

        return date_header

    def get_to_date_header(self, form):
        date_header = form['to_date'][8:] + '-' + form['to_date'][5:7] + '-' + form['to_date'][:4]

        return date_header

    def get_ap_aging(self, due_date, tanggal):

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
        isi = []
        no = 1
        aging = ''
        tanggal_date_due = ''
        obj_account_invoice = self.pool.get('account.invoice')
        if form['partner_id'] == '0':
            kriteria = [ ('date_invoice', '>=', form['from_date']), ('date_invoice', '<=' ,form['to_date']),
                        ('type', '=', 'out_invoice'), ('state', '=', 'open'), ('journal_id', '=',form['journal_id'])]
        else:
            kriteria = [('date_invoice', '>=', form['from_date']), ('date_invoice', '<=', form['to_date']),
                        ('type', '=', 'out_invoice'), ('state', '=', 'open'), ('journal_id', '=', form['journal_id']), ('partner_id', '=', form['partner_id']) ]

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

                if self.get_ap_aging(aging, form['tanggal']) < 0:
                    res = {
                        'tgljatuh': '',
                        'tgljatuh30': '',
                        'tgljatuh60': '',
                        'tgljatuhlebih': '',
                        'belumjatuh': invoice.amount_total or 0,
                    }
                    isi.append(res)

                elif self.get_ap_aging(aging, form['tanggal']) <= 30:
                    res = {
                        'tgljatuh': invoice.amount_total or 0,
                        'tgljatuh30': '',
                        'tgljatuh60': '',
                        'tgljatuhlebih': '',
                        'belumjatuh': ''
                    }
                    isi.append(res)

                elif self.get_ap_aging(aging, form['tanggal']) > 30 and self.get_ap_aging(aging, form['tanggal']) <= 60:
                    res = {
                        'tgljatuh': '',
                        'tgljatuh30': invoice.amount_total or 0,
                        'tgljatuh60': '',
                        'tgljatuhlebih': '',
                        'belumjatuh': ''
                    }
                    isi.append(res)
                elif self.get_ap_aging(aging, form['tanggal']) > 60 and self.get_ap_aging(aging, form['tanggal']) <= 90:
                    res = {
                        'tgljatuh': '',
                        'tgljatuh30': '',
                        'tgljatuh60': invoice.amount_total or 0,
                        'tgljatuhlebih': '',
                        'belumjatuh': ''
                    }
                    isi.append(res)
                elif self.get_ap_aging(aging, form['tanggal']) > 90:
                    res = {
                        'tgljatuh': '',
                        'tgljatuh30': '',
                        'tgljatuh60': '',
                        'tgljatuhlebih': invoice.amount_total or 0,
                        'belumjatuh': ''
                    }
                    isi.append(res)

                result = {
                        'no' : no,
                        'supplier' : invoice.partner_id.name,
                        'no_invoice' : invoice.number,
                        'ap_amount' : invoice.amount_untaxed or 0,
                        'vat' : invoice.amount_tax or 0,
                        'acc_payable_balance' : invoice.amount_total or 0,
                        'ap_aging' : self.get_ap_aging(aging, form['tanggal']),
                        'exch_rate' : rate,
                        'symbol_invoice' : invoice.currency_id.symbol,
                        'symbol_company' : invoice.company_id.currency_id.symbol,
                        'date_invoice' : invoice.date_invoice[8:] + '-' + invoice.date_invoice[5:7] + '-' + invoice.date_invoice[:4],
                        'date_due' : tanggal_date_due,
                        'acc_payable_balance_rp' : invoice.amount_total * rate or 0,
                        'ref': invoice.reference,
                        'sales': invoice.user_id.name
                }
                result.update(res)

                no += 1
                self.isi_laporan.append(result)

        return self.isi_laporan

report_sxw.report_sxw('report.loista_piutang_report', 'account.invoice','addons/fb_piutangpiutang/report/loista_piutang_report.rml',parser=loista_piutang_report, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
