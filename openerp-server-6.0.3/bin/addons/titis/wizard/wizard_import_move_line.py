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

from lxml import etree

import netsvc
import time

from osv import osv,fields
from tools.translate import _
import decimal_precision as dp

class wizard_import_move_line(osv.osv_memory):
    _name = 'titis.wizard_import_move_line'
    _description = 'Wizard Import Move Line'
    
    _columns = {
                            'move_line_ids' : fields.many2many(string='Move Lines', obj='account.move.line', rel='account_import_move_line_rel', id1='import_id', id2='move_id', required=True),
                            }
                            
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        res = super(wizard_import_move_line, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar,submenu=False)
        view = []
        
        record_id = context and context.get('move_type', False) or False

        if view_type == 'form':
        
            for field in res['fields']:
                if field == 'move_line_ids':
                    if record_id == 'cr':
                        res['fields'][field]['domain'] = [('reconcile_id','=',False),('account_id.reconcile','=',True),('debit','>',0),('state','=','valid')]
                    elif record_id == 'dr':
                        res['fields'][field]['domain'] = [('reconcile_id','=',False),('account_id.reconcile','=',True),('credit','>',0),('state','=','valid')]
                    else:
                        res['fields'][field]['domain'] = []
        return res
        
    def import_move_lines(self, cr, uid, ids, data, context=None):
        obj_wizard = self.pool.get('titis.wizard_import_move_line')
        obj_account_voucher = self.pool.get('account.voucher')
        obj_account_voucher_line = self.pool.get('account.voucher.line')

        record_id = data['active_id']

        move_type = data['move_type']
        
        wizard = obj_wizard.browse(cr, uid, ids)[0]

        voucher_id = obj_account_voucher.browse(cr, uid, [record_id])[0]

        for move_line in wizard.move_line_ids:
            kriteria = [('move_line_id','=',move_line.id),('voucher_id','=',voucher_id.id)]

            voucher_line_ids = obj_account_voucher_line.search(cr, uid, kriteria)

            if not voucher_line_ids:
                amount = obj_account_voucher_line.compute_amount(cr, uid, move_line.id, voucher_id.journal_id.id, voucher_id.currency_id.id)['amount']
                val = {
                        'voucher_id' : record_id,
                        'account_id' : move_line.account_id.id,
                        'move_line_id' : move_line.id,
                        'name' : move_line.name,
                        'type' : move_type,
                        'amount' : amount,
                        
                        }
                obj_account_voucher_line.create(cr, uid, val, context=context)
        return {'type': 'ir.actions.act_window_close'}
        
wizard_import_move_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

