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

from dateutil import parser
import xml
import copy
from operator import itemgetter
import time
import datetime
import re
from report import report_sxw

class trial_balance(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(trial_balance, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.isi_beginning = []
        self.localcontext.update({
            'time': time,
            'isi_laporan': self.lines,
            # 'periode' : self.get_periode,
            'isi_beginning': self.get_begin_bal,
        })
        self.context = context

    def get_periode(self, form):
        periode = ''
        date_start = ''
        date_stop = ''

        obj_period = self.pool.get('account.period')

        kriteria = [ ('id','=', form['period_id']) ]

        period_ids = obj_period.search(self.cr, self.uid, kriteria)

        for period in obj_period.browse(self.cr, self.uid, period_ids):
            if period:
                date_start = period.date_start[8:] + '-' + period.date_start[5:7] + '-' + period.date_start[:4]
                date_stop = period.date_stop[8:] + '-' + period.date_stop[5:7] + '-' + period.date_stop[:4]
                periode = date_start + ' - ' + date_stop

        return periode

    def get_date_start(self, form):
        date_start = ''

        obj_period = self.pool.get('account.period')

        kriteria = [ ('id','=', form['period_id']) ]

        period_ids = obj_period.search(self.cr, self.uid, kriteria)

        for period in obj_period.browse(self.cr, self.uid, period_ids):
            if period:
                date_start = period.date_start

        return date_start

    def get_date_stop(self, form):
        date_stop = ''

        obj_period = self.pool.get('account.period')

        kriteria = [ ('id','=', form['period_id']) ]

        period_ids = obj_period.search(self.cr, self.uid, kriteria)

        for period in obj_period.browse(self.cr, self.uid, period_ids):
            if period:
                date_stop = period.date_stop

        return date_stop

    def get_begin_bal(self,form):
        saldo_awal = []

        ctx = self.context.copy()
        ctx['date_begin'] = form['date_from']

        ids = self.pool.get('account.account').search(self.cr, self.uid, [('type', '<>', '')])
        begin = self.pool.get('account.account').browse(self.cr, self.uid, ids, ctx)
        for beg_bal in begin:
            res = {
                'begin_debit': beg_bal.debit,
                'begin_credit': beg_bal.credit
            }
            saldo_awal.append(res)
        return saldo_awal


    def get_ending_bal(self, form):
        saldo_akhir= []

        ctx = self.context.copy()
        ctx['date_end'] = form['date_to']


        ids = self.pool.get('account.account').search(self.cr, self.uid, [('type', '<>', '')])
        begin = self.pool.get('account.account').browse(self.cr, self.uid, ids, ctx)

        for end_bal in begin:
            res = {
                'end_debit': end_bal.debit,
                'end_credit': end_bal.credit
            }
            saldo_akhir.append(res)
        return saldo_akhir

    def lines(self, form):
        ctx = self.context.copy()
        # ctx['date_from'] = self.get_date_start(form)
        # ctx['date_to'] =  self.get_date_stop(form)
        ctx['date_from'] = form['date_from']
        ctx['date_to'] = form['date_to']

        debit_awal = []
        credit_awal = []
        debit_akhir = []
        credit_akhir = []

        begining = self.get_begin_bal(form)
        # ending = self.get_ending_bal(form)

        # for j in range(0, len(ending)):
        #     debit_end = ending[j]['end_debit']
        #     credit_end = ending[j]['end_credit']

            # debit_akhir.append(debit_end)
            # credit_akhir.append(credit_end)
        # debit_e = 0
        # credit_e = 0

        for i in range(0, len(begining)):
            debit_begin = begining[i]['begin_debit']
            credit_begin = begining[i]['begin_credit']
            # d += ''.join(str(begin_deb))
            debit_awal.append(debit_begin)
            credit_awal.append(credit_begin)
        debit_b = 0
        credit_b = 0

        ids = self.pool.get('account.account').search(self.cr, self.uid, [('type', '<>', '')])
        for akun in self.pool.get('account.account').browse(self.cr, self.uid, ids, ctx):

            # get_begin = self.get_begin_bal(akun.id)
            # debit_awal = get_begin['begin_debit']
            # credit_awal = get_begin['begin_credit']
            if akun.balance > 0:
                bal_debit = akun.debit
                bal_credit = 0
            elif akun.balance < 0:
                bal_credit = akun.credit
                bal_debit = 0
            else:
                bal_debit = 0
                bal_credit = 0

            res = {
                'type': akun.type,
                'code': akun.code,
                'name': akun.name,
                'debit': akun.debit,
                'credit': akun.credit,
                'balance': akun.balance,
                'bal_debit' : bal_debit,
                'bal_credit' : bal_credit,
                'level' : akun.level,
                'start_date': form['date_from'],
                'end_date': form['date_to'],
                'begin_debit': debit_awal[debit_b],
                'begin_credit': credit_awal[credit_b],
                'end_debit': (debit_awal[debit_b] + akun.debit) - (credit_awal[credit_b] + akun.credit),
                # 'end_credit': credit_awal[credit_b] - akun.credit,
            }

            self.isi_laporan.append(res)
            debit_b += 1
            credit_b += 1
            # debit_e += 1
            # credit_e += 1

        return self.isi_laporan

report_sxw.report_sxw('report.trial_balance', 'account.account','addons/titis/report/trial_balance.rml',parser=trial_balance, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: