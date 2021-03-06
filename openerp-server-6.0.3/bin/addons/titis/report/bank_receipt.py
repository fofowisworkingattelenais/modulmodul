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
from tools.translate import _
from tools import amount_to_text_en

class bank_receipt(report_sxw.rml_parse):


    def __init__(self, cr, uid, name, context):
        super(bank_receipt, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_title': self.get_title,
            'get_lines':self.get_lines,
            'get_on_account':self.get_on_account,
            'convert':self.convert
        })

    def convert(self, amount):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', 'Dolar')
        return amt_en

    def get_lines(self, voucher):
        result = []
        if voucher.type in 'receipt':
            type = voucher.line_ids and voucher.line_ids[0].type or False
            for move in voucher.move_ids:
                res = {}
                amount = move.credit
                if type == 'dr':
                    amount = move.debit
                if amount > 0.0:
                    res['pname'] = move.partner_id.name
                    res['ref'] = str(move.name)
                    res['aname'] = move.account_id.code
                    res['amount'] = amount
                    result.append(res)
        else:
            type = voucher.line_ids and voucher.line_ids[0].type or False
            for move in voucher.move_ids:
                res = {}
                amount = move.credit
                if type == 'dr':
                    amount = move.debit
                if amount > 0.0:
                    res['pname'] = move.partner_id.name
                    res['ref'] =  move.name
                    res['aname'] = move.account_id.code
                    res['amount'] = amount
                    result.append(res)
        return result

    def get_title(self, type):
        title = ''
        if type:
            title = type[0].swapcase() + type[1:] + " Voucher"
        return title

    def get_on_account(self, voucher):
        name = ""
        if voucher.type == 'receipt':
            name = "Receipt from "+str(voucher.partner_id.name)
        return name

report_sxw.report_sxw('report.bank_receipt','titis.bank_receipt','addons/titis/report/bank_receipt.rml',parser=bank_receipt, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


