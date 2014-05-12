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

class laporan_indirect_cashflow(report_sxw.rml_parse):
    _name = 'report.laporan.indirect.cashflow'

    def __init__(self, cr, uid, name, context):

        super(laporan_indirect_cashflow, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.total_debit = 0.0
        self.total_kredit = 0.0
        self.localcontext.update({
            'time': time,
            # 'date_from' : self.get_date_from,
            # 'date_to' : self.get_date_to,
            'date_length' : self.get_date_length,
            'isi_laporan' : self.lines,
        })
        self.context = context

    def get_date_length(self, form):
        date_start = form['date_from'][8:] + '-' + form['date_from'][5:7] + '-' + form['date_from'][:4]
        date_stop = form['date_to'][8:] + '-' + form['date_to'][5:7] + '-' + form['date_to'][:4]

        date_lenght = date_start + ' - ' + date_stop
        return date_lenght


#start of lines(isi laporan)
    def lines(self, form):

        # obj_account_move_line = self.pool.get('account.move.line')
        #
        # tanggal_mulai = form['date_from']
        # tanggal_akhir = form['date_to']
        #
        # move_line_ids = []

        # sql_string =    """
        #                 SELECT  A.id AS id
        #                 FROM    account_move_line AS A
        #                 JOIN    account_move AS B ON A.move_id=B.id
        #                 WHERE   B.date >= '%s' AND
        #                         B.date <= '%s' AND
        #                         A.state = 'valid'
        #                 ORDER BY    B.date
        #                 """ % (tanggal_mulai, tanggal_akhir)

        # self.cr.execute(sql_string)
        # for (move_id) in self.cr.fetchall():
        #     move_line_ids.append(move_id[0])
        # for account_move_line in obj_account_move_line.browse(self.cr, self.uid, move_line_ids):
        level = 0

        ctx = self.context.copy()
        ctx['date_from'] = form['date_from']
        ctx['date_to'] = form['date_to']
        model_account = self.pool.get('account.account')
        ids = model_account.search(self.cr, self.uid, [('type','<>','')])

        child_ids = model_account._get_children_and_consol(self.cr, self.uid, ids, ctx)

        if child_ids:
            ids = child_ids


        for account_move_line in self.pool.get('account.account').browse(self.cr, self.uid, ids, ctx):
            self.total_debit += account_move_line.debit
            self.total_kredit += account_move_line.credit
            # if account_move_line.balance > 0:
            #     bal_debit = account_move_line.debit
            #     bal_credit = 0
            # elif account_move_line.balance < 0:
            #     bal_credit = account_move_line.credit
            #     bal_debit = 0
            # else:
            #     bal_debit = 0
            #     bal_credit = 0

            res = {
                    'type': account_move_line.type,
                    'name': account_move_line.name,
                    'level' : account_move_line.level,
                    'debit': account_move_line.debit,
                    'kredit': account_move_line.credit,
                    'total_debit': self.total_debit,
                    'total_credit': self.total_kredit,
                    'balance': account_move_line.credit - account_move_line.debit,
                    'bal_type': '',

            }

            self.isi_laporan.append(res)

        return self.isi_laporan

#end of lines

report_sxw.report_sxw('report.laporan.indirect.cashflow', 'account.account','addons/titis/report/laporan_indirect_cashflow.rml',parser=laporan_indirect_cashflow, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
