##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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
from datetime import datetime
from dateutil.relativedelta import relativedelta

from osv import osv, fields
import netsvc
import pooler
from tools.translate import _
import decimal_precision as dp
from osv.orm import browse_record, browse_null
import logging
_log = logging.getLogger('kurs pajak')

class smcus_kurs_pajak(osv.osv):
    _name = "smcus.kurs.pajak"
    _description = "Telenais Kurs Pajak Form"
    _order = "name desc"

    def _current_rate(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        res = {}
        if 'date' in context:
            date = context['date']
        else:
            date = time.strftime('%Y-%m-%d')
        _log.info ('get rate')
        _log.info (context)
        _log.info (date)
        date = date or time.strftime('%Y-%m-%d')
        res = {}
        for id in ids:
            res[id] = {
                'rate': 0.0,
                'berdasarkan': False,
                'berdasarkan_no': False,
                'berdasarkan_date': False,
            }
            cr.execute("SELECT faktur_pajak_rate_id, rate, berdasarkan, berdasarkan_no, berdasarkan_date FROM smcus_kurs_pajak_line WHERE faktur_pajak_rate_id = %s AND name <= %s ORDER BY name desc LIMIT 1" ,(id, date))
            if cr.rowcount:
                id, rate, berdasarkan, berdasarkan_no, berdasarkan_date = cr.fetchall()[0]
                res[id]['rate'] = rate
                res[id]['berdasarkan'] = berdasarkan
                res[id]['berdasarkan_no'] = berdasarkan_no
                res[id]['berdasarkan_date'] = berdasarkan_date

        return res


    def _get_default_to(self, cr, uid, context=None):
        currency = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id
        if currency:
            return currency.id
        else:
            return False

    _columns = {
        'name': fields.many2one('res.currency', 'From Currency', required=True),
        'tcurrency_id': fields.many2one('res.currency', 'To Currency', required=True),
        'rate': fields.function(_current_rate, method=True, string='Current Rate', digits=(12,3),
            help='The rate of the currency to the currency of rate 1.', multi='currate'),
        'rate_ids': fields.one2many('smcus.kurs.pajak.line', 'faktur_pajak_rate_id', 'Rates'),
        'berdasarkan': fields.function(_current_rate, method=True, type="char", string='Kurs Berdasarkan', multi='currate'),
        'berdasarkan_no': fields.function(_current_rate, method=True, type="char", string='No.', multi='currate'),
        'berdasarkan_date': fields.function(_current_rate, method=True, type="date", string='Tanggal', multi='currate'),
    }
    _defaults = {
        'tcurrency_id': _get_default_to,
    }

    _sql_constraints = [('from_to_uniq', 'unique(name, tcurrency_id)', 'Only one pair from and to currency allowed')] 

smcus_kurs_pajak()

class smcus_kurs_pajak_line(osv.osv):
    _name = 'smcus.kurs.pajak.line'
    
    _columns = {
        'name': fields.date('Date', required=True, select=True),
        'rate': fields.float('Rate', digits=(12,3), help='The rate of the currency to the currency of rate 1',required=True),
        'faktur_pajak_rate_id': fields.many2one('smcus.kurs.pajak', 'Kurs Pajak'),
        'berdasarkan': fields.char('Kurs Berdasakan', size=50,required=False),
        'berdasarkan_no': fields.char('No.', size=50,required=False),
        'berdasarkan_date': fields.date('Tanggal', required=False),
    }
    _defaults = {
        'name': lambda *a: time.strftime('%Y-%m-%d'),
    }
    _sql_constraints = [('date_rate_uniq', 'unique(name, faktur_pajak_rate_id)', 'Only one date for each rate')] 
    _order = "name desc"
    

smcus_kurs_pajak_line()
