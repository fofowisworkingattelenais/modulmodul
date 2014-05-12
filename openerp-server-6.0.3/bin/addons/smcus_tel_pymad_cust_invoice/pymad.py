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
        'invoice_id': fields.many2one('account.invoice', 'Customer Invoice', readonly=True, help="Link to the automatically generated Customer Invoice."),       
    }

    def action_cancel_invoice(self, cr, uid, ids, *args):
        if not len(ids):
            return False
        for o in self.browse(cr, uid, ids):
            if o.invoice_id:
                if not o.invoice_id.state == 'draft':
                    raise osv.except_osv(_('Invalid action !'), _('Customer Invoce ' + o.invoice_id.name + ' is still in Progress. Please make it draft before cancel this PyMAD'))
                else:
                    self.pool.get('account.invoice').unlink (cr, uid, [o.invoice_id.id], context=None)
            self.write(cr, uid, ids, {'state': 'validated'})
        return True

    def inv_line_create(self, cr, uid, a, ol):
        return (0, False, {
            'name': ol.name,
            'account_id': a,
            'price_unit': ol.price_unit or 0.0,
            'quantity': ol.product_qty,
            'product_id': ol.product_id.id or False,
            'uos_id': ol.product_uom.id or False,
            'invoice_line_tax_id': [(6, 0, [x.id for x in ol.tax_id])],
            #'account_analytic_id': ol.account_analytic_id.id or False,
        })

    def action_invoice_create(self, cr, uid, ids, *args):
        if not len(ids):
            return False
        #create customer invoice
        journal_obj = self.pool.get('account.journal')

        for o in self.browse(cr, uid, ids):
            il = []
                
            for ol in o.pymad_line:
                if ol.product_id:
                    #direct to pymad account
                    a = ol.product_id.product_tmpl_id.property_stock_account_output.id
                    if not a:
                        a = ol.product_id.categ_id.property_stock_account_output_categ.id
                    if not a:
                        raise osv.except_osv(_('Error !'),
                                _('There is no Stock Output Account (PyMAD) defined ' \
                                        'for this product: "%s" (id:%d)') % \
                                        (ol.product_id.name, ol.product_id.id,))

                else:
                    prop = self.pool.get('ir.property').get(cr, uid,
                            'property_stock_account_output_categ', 'product.category',
                            context=context)
                    a = prop and prop.id or False

                fpos = o.order_id.fiscal_position or False
                a = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, a)
                il.append(self.inv_line_create(cr, uid, a, ol))

            a = o.partner_id.property_account_receivable.id
            journal_ids = journal_obj.search(cr, uid, [('type', '=','sale'),('company_id', '=', o.order_id.company_id.id)], limit=1)
            if not journal_ids:
                raise osv.except_osv(_('Error !'),
                    _('There is no Sales journal defined for this company: "%s" (id:%d)') % (o.order_id.company_id.name, o.order_id.company_id.id))
            inv = {
                'name': o.name,
                'smcus_pymad_id': o.id,
                'reference': (o.order_id.name or '')+':'+ o.name,
                'account_id': a,
                'type': 'out_invoice',
                'partner_id': o.partner_id.id,
                'currency_id': o.order_id.pricelist_id.currency_id.id,
                'address_invoice_id': o.order_id.partner_invoice_id.id,
                'address_contact_id': o.order_id.partner_order_id.id,
                'journal_id': len(journal_ids) and journal_ids[0] or False,
                'origin': (o.order_id.name or '')+':'+ o.name,
                'invoice_line': il,
                'fiscal_position': o.order_id.fiscal_position.id or o.partner_id.property_account_position.id,
                'payment_term': o.partner_id.property_payment_term and o.partner_id.property_payment_term.id or False,
                'company_id': o.order_id.company_id.id,
            }
            inv_id = self.pool.get('account.invoice').create(cr, uid, inv, {'type':'out_invoice'})
            self.pool.get('account.invoice').button_compute(cr, uid, [inv_id], {'type':'out_invoice'}, set_total=True)
            self.pool.get('sale.order').write(cr, uid, [o.order_id.id], {'invoice_ids': [(4, inv_id)]})
            res = inv_id
       
            self.write(cr, uid, o.id, {'state': 'invoiced', 'invoice_id': inv_id})
        return True

smcus_pymad()

