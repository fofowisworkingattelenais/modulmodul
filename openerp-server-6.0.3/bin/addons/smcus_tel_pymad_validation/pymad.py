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

class smcus_pymad(osv.osv):
    _inherit = "smcus.pymad"

    _columns = {
        'move_id': fields.many2one('account.move', 'Journal Entry', readonly=True, help="Link to the automatically generated Journal Items."),       
    }
    
    def action_validate(self, cr, uid, ids, *args):
        if not len(ids):
            return False
            
        #get journal_id
        user = self.pool.get('res.users').browse(cr, uid, uid, context=None)
        company_id = user.company_id.id
        journal_obj = self.pool.get('account.journal')
        res = journal_obj.search(cr, uid, [('type', '=', 'sale'),
                                            ('company_id', '=', company_id)],
                                                limit=1)
        journal_id = res and res[0] or False
        if not journal_id:
            raise osv.except_osv(_('Error !'), _('No default Sales Journal'))
        journal = journal_obj.browse (cr, uid, journal_id, context=None)
        if not journal.sequence_id:
            raise osv.except_osv(_('Error !'), _('Please define sequence on invoice journal'))
            
        mv_obj = self.pool.get('account.move')
        mvl_obj = self.pool.get('account.move.line')

        for py in self.browse(cr, uid, ids):

            move = {
                'ref': py.name,
                'journal_id': journal_id,
                'date': py.date_pymad,
                'type': 'journal_sale_vou',
                'narration':py.notes
            }
            move_id = mv_obj.create(cr, uid, move, context=None)

            for line in py.pymad_line:
                #find account_id
                if line.product_id:
                    a = line.product_id.product_tmpl_id.property_account_income.id
                    if not a:
                        a = line.product_id.categ_id.property_account_income_categ.id
                    if not a:
                        raise osv.except_osv(_('Error !'),
                                _('There is no income account defined ' \
                                        'for this product: "%s" (id:%d)') % \
                                        (line.product_id.name, line.product_id.id,))
                    b = line.product_id.product_tmpl_id.property_stock_account_output.id
                    if not b:
                        b = line.product_id.categ_id.property_stock_account_output_categ.id
                    if not b:
                        raise osv.except_osv(_('Error !'),
                                _('There is no Stock Output Account (PyMAD) defined ' \
                                        'for this product: "%s" (id:%d)') % \
                                        (line.product_id.name, line.product_id.id,))
                else:
                    prop = self.pool.get('ir.property').get(cr, uid,
                            'property_account_income_categ', 'product.category',
                            context=context)
                    a = prop and prop.id or False
                    prop = self.pool.get('ir.property').get(cr, uid,
                            'property_stock_account_output_categ', 'product.category',
                            context=context)
                    b = prop and prop.id or False
                    
                sale_account_id = a
                pymad_account_id = b

                #debit side (pymad)
                vals = { 
                    'date_maturity': False,
                    'partner_id': py.partner_id.id,
                    'name': line.name,
                    'date': py.date_pymad,
                    'debit': line.price_subtotal,
                    'credit': 0,
                    'account_id': pymad_account_id,
                    'ref': py.name,
                    'move_id': move_id
                }
                mvl_id = mvl_obj.create(cr, uid, vals, context=None)
                
                #credit side (penjualan)
                vals = { 
                    'date_maturity': False,
                    'partner_id': py.partner_id.id,
                    'name': line.name,
                    'date': py.date_pymad,
                    'debit': 0,
                    'credit': line.price_subtotal,
                    'account_id': sale_account_id,
                    'ref': py.name,
                    'move_id': move_id
                }
                mvl_id = mvl_obj.create(cr, uid, vals, context=None)
                      
        mv_obj.post(cr, uid, [move_id], context=None)
        self.write(cr, uid, ids, {'state': 'validated', 'move_id': move_id})
        return True

    def action_cancel(self, cr, uid, ids, *args):
        if not len(ids):
            return False
        mv_obj = self.pool.get('account.move')
        for rec in self.browse(cr, uid, ids, context=None):
            if rec.move_id:
                res = mv_obj.button_cancel(cr, uid, [rec.move_id.id], context=None)
                if res:
                    mv_obj.unlink(cr, uid, [rec.move_id.id], context=None)

        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        """Allows to delete sales order lines in draft,cancel states"""
        for rec in self.browse(cr, uid, ids, context=context):
            if rec.state not in ['draft']:
                raise osv.except_osv(_('Invalid action !'), _('Only delete Draft PyMAD'))
        return super(smcus_pymad, self).unlink(cr, uid, ids, context=context)

smcus_pymad()

