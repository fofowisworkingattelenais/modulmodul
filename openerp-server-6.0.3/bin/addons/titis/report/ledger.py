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

from datetime import time, date, datetime
from report import report_sxw

from tools.translate import _
import time

import pooler

class laporan_ledger(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(laporan_ledger, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.total_debit = 0.0
        self.total_kredit = 0.0
        self.total_saldo = 0.0
        self.saldo = 0.0
        self.localcontext.update({
            'time': time,
            'isi_laporan' : self.lines,
            'account_code' : self.get_account_code,
            'account_name' : self.get_account_name,
            'periode_length' : self.get_periode_length,
            'date_length' : self.get_date_length,
            'saldo_awal' : self.get_saldo_awal,
            'saldo_awal1': self.get_saldo_awal1,
        })
        self.context = context

    def get_account_code(self, form):
        account_code = ''
        obj_account_account = self.pool.get('account.account')
        kriteria = [ ('id','=', form['account_id']) ]
        account_ids = obj_account_account.search(self.cr, self.uid, kriteria)
        for account in obj_account_account.browse(self.cr, self.uid, account_ids):
            if account:
                account_code = account.code

        return account_code

    def get_account_name(self, form):
        account_name = ''
        obj_account_account = self.pool.get('account.account')
        kriteria = [ ('id','=', form['account_id']) ]
        account_ids = obj_account_account.search(self.cr, self.uid, kriteria)
        for account in obj_account_account.browse(self.cr, self.uid, account_ids):
            if account:
                account_name = account.name

        return account_name
    def get_periode_length(self, form):
        periode_length = ''
        obj_period = self.pool.get('account.period')
        kriteria = [ ('id','=', form['period_id']) ]
        period_ids = obj_period.search(self.cr, self.uid, kriteria)

        for period in obj_period.browse(self.cr, self.uid, period_ids):
            if period:
                periode_length = str(period.date_start) + '-' + str(period.date_stop)

        return periode_length

    def get_date_length(self, form):
        date_start = form['date_from'][8:] + '-' + form['date_from'][5:7] + '-' + form['date_from'][:4]
        date_stop = form['date_to'][8:] + '-' + form['date_to'][5:7] + '-' + form['date_to'][:4]

        date_lenght = date_start + ' - ' + date_stop
        return date_lenght

    def get_nama_analytic(self, analytic_account_id):
        nama_analytic = ''
        obj_account_analytic = self.pool.get('account.analytic.account')

        kriteria = [ ('id','=', analytic_account_id) ]

        analytic_line_ids = obj_account_analytic.search(self.cr, self.uid, kriteria)

        for analytic in obj_account_analytic.browse(self.cr, self.uid, analytic_line_ids):
            if analytic:
                nama_analytic = analytic.name

        return nama_analytic

    def get_saldo_awal(self, form):
        saldo_awal = 0
        obj_account_move_line = self.pool.get('account.move.line')

        tanggal_mulai = form['date_from']

        move_line_ids = []

        sql_string =    """
                        SELECT  A.id AS id
                        FROM    account_move_line AS A
                        JOIN    account_move AS B ON A.move_id=B.id
                        WHERE   B.date < '%s' AND
                                A.account_id = %s AND
                                A.state = 'valid'
                        ORDER BY    B.date
                        """ % (tanggal_mulai, form['account_id'])

        self.cr.execute(sql_string)
        for (move_id) in self.cr.fetchall():
            move_line_ids.append(move_id[0])

        if move_line_ids:
            for account_move_line in obj_account_move_line.browse(self.cr, self.uid, move_line_ids):
                saldo_awal += (account_move_line.debit - account_move_line.credit)
                self.saldo += (account_move_line.debit - account_move_line.credit)
        return saldo_awal


    def get_saldo_awal1(self, form):
        saldo_awal = 0
        obj_account_move_line = self.pool.get('account.move.line')

        tanggal_mulai = form['date_from']

        move_line_ids = []

        sql_string =    """
                        SELECT  A.id AS id
                        FROM    account_move_line AS A
                        JOIN    account_move AS B ON A.move_id=B.id
                        WHERE   B.date < '%s' AND
                                A.account_id = %s AND
                                A.state = 'valid'
                        ORDER BY    B.date
                        """ % (tanggal_mulai, form['account_id'])

        self.cr.execute(sql_string)
        for (move_id) in self.cr.fetchall():
            move_line_ids.append(move_id[0])

        if move_line_ids:
            for account_move_line in obj_account_move_line.browse(self.cr, self.uid, move_line_ids):
                saldo_awal += (account_move_line.debit - account_move_line.credit)
        return saldo_awal




    def lines(self, form):
        ss = []
        ss.append(self.get_saldo_awal1(form))

        obj_account_move_line = self.pool.get('account.move.line')

        tanggal_mulai = form['date_from']
        tanggal_akhir = form['date_to']

        move_line_ids = []

        sql_string =    """
                        SELECT  A.id AS id
                        FROM    account_move_line AS A
                        JOIN    account_move AS B ON A.move_id=B.id
                        WHERE   B.date >= '%s' AND
                                B.date <= '%s' AND
                                A.account_id = %s AND
                                A.state = 'valid'
                        ORDER BY    B.date
                        """ % (tanggal_mulai, tanggal_akhir, form['account_id'])

        self.cr.execute(sql_string)
        for (move_id) in self.cr.fetchall():
            move_line_ids.append(move_id[0])

        for account_move_line in obj_account_move_line.browse(self.cr, self.uid, move_line_ids):
            self.total_debit += account_move_line.debit
            self.total_kredit += account_move_line.credit
            self.saldo += (account_move_line.debit - account_move_line.credit)

            res = {
                'tanggal': account_move_line.move_id.date,
                'keterangan': account_move_line.name,
                'no_voucher': account_move_line.move_id.name,
                'debit': account_move_line.debit,
                'kredit': account_move_line.credit,
                'saldo': self.saldo,
                'total_debit': self.total_debit,
                'total_credit': self.total_kredit,
                'ref': account_move_line.ref,
                'foreign_kode': account_move_line.currency_id.name,
                'foreign_jumlah': account_move_line.amount_currency,
                'dept': self.get_nama_analytic(account_move_line.analytics_id.id),
                'saldo_akhir':   ss[0] + (self.total_debit - self.total_kredit)
            }

            self.isi_laporan.append(res)

        return self.isi_laporan

report_sxw.report_sxw('report.laporan_ledger', 'account.account', 'addons/titis/report/ledger.rml', parser=laporan_ledger, header='internal')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
