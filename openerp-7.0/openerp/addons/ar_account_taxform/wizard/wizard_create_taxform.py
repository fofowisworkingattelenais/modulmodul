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


from osv import fields, osv
from datetime import date
import netsvc
from tools.translate import _


class wizard_create_taxform(osv.osv_memory):
    _name = 'account.wizard_create_taxform'
    _description = 'Wizard Create Taxform'

    def create_taxform(self, cr, uid, ids, context={}):
        var_discount = 0.00
        obj_user = self.pool.get('res.users')
        obj_taxform = self.pool.get('account.taxform')
        obj_taxform_line = self.pool.get('account.taxform_line')
        obj_inv_line = self.pool.get('account.invoice_line')
        obj_inv = self.pool.get('account.invoice')
        obj_tax = self.pool.get('account.tax')
        obj_currency = self.pool.get('res.currency')
        kp_obj = self.pool.get('smcus.kurs.pajak')

        user = obj_user.browse(cr, uid, [uid], context=context)[0]


        for invoice in obj_inv.browse(cr, uid, context['active_ids'], context=context):
            company_currency = invoice.company_id.currency_id.id

            advance_payment = 0.0
            discount = 0.0

            kriteria = [('invoice_id','=',invoice.id),('state','in',('draft','printed'))]
            taxform_ids = obj_taxform.search(cr, uid, kriteria)
            diff_currency_p = invoice.currency_id.id <> company_currency

            if diff_currency_p:
                datek = date.today().strftime('%Y-%m-%d')
                kp_rate = kp_obj.search(cr, uid, [('name','=',invoice.currency_id.id),('tcurrency_id','=',company_currency)], context={'date': datek})
                smcus_kurs_pajak = False

                if kp_rate:
                    rate_id = kp_rate[0]
                    smcus_kurs_pajak = kp_obj.browse(cr, uid, [rate_id], context={'date': datek})[0].rate
                    berdasarkan_no = kp_obj.browse(cr, uid, [rate_id], context={'date': datek})[0].berdasarkan_no
                    berdasarkan_date = kp_obj.browse(cr, uid, [rate_id], context={'date': datek})[0].berdasarkan_date
                    if smcus_kurs_pajak==0:
                        raise osv.except_osv(_('Error'), _('No Kurs Pajak found \n' \
                                'for the currency: %s \n' \
                                'at the date: %s') % (invoice.currency_id.name, datek))
                else:
                    raise osv.except_osv(_('Error!'), _('Kurs Pajak has not defined yet'))
            else:
                smcus_kurs_pajak = 0.00
                berdasarkan_no = None
                berdasarkan_date = None

            if not taxform_ids and invoice.state in ('open','paid'):
                doc_signed_id = invoice.company_id.user_sign_id

                val_taxform ={
                    'name' : '/',
                    'company_id' : invoice.company_id.company_tax_id      and invoice.company_id.company_tax_id.id or invoice.company_id.id,
                    'company_address' : invoice.company_id.company_tax_id and invoice.company_id.company_tax_id.partner_id.id or invoice.company_id.partner_id.id,
                    'company_npwp' : invoice.company_id.company_tax_id and invoice.company_id.company_tax_id.partner_id.vat or invoice.company_id.partner_id.vat,
                    'taxform_date' : date.today().strftime('%Y-%m-%d'),
                    'invoice_id' : invoice.id,
                    'partner_id' : invoice.partner_id.id,
                    'partner_address_id' : invoice.partner_id.id,
                    'partner_npwp' : invoice.partner_id.npwp,
                    'discount' : discount,
                    'advance_payment' : advance_payment,
                    'signature_id' : doc_signed_id and doc_signed_id.id or False,
                    'base' : invoice.amount_untaxed,
                    'untaxed' : invoice.amount_untaxed,
                    'amount_tax' : invoice.amount_tax,
                    'kurs_pajak': smcus_kurs_pajak,
                    'berdasarkan_no': berdasarkan_no,
                    'berdasarkan_date': berdasarkan_date,
                    'result_pajak': smcus_kurs_pajak * invoice.amount_tax
                }


                if val_taxform.get('company_npwp', False) == False:
                    val_taxform['company_npwp'] = '/'

                if val_taxform.get('partner_npwp', False) == False:
                    val_taxform['partner_npwp'] = '/'

                taxform_id = obj_taxform.create(cr, uid, val_taxform)

                for invoice_line in invoice.invoice_line:
                    if invoice_line.price_subtotal > 0:
                        price = invoice_line.price_unit * (1-(invoice_line.discount or 0.0)/100.0)
                        taxes = obj_tax.compute_all(cr, uid, invoice_line.invoice_line_tax_id, price, invoice_line.quantity, product=invoice_line.product_id,  partner=invoice_line.invoice_id.partner_id)
                        subtotal = obj_currency.round(cr, uid, invoice.currency_id, (100.00/(100.00 - invoice_line.discount)) * taxes['total'] )
                        val_inv_line = {
                            'name' : invoice_line.name,
                            'product_id' : invoice_line.product_id and invoice_line.product_id.id or False,
                            'subtotal' : subtotal,
                            'taxform_id' : taxform_id,
                        }
                        obj_taxform_line.create(cr, uid, val_inv_line)
                        discount =+ (invoice_line.discount/100.00) * subtotal
                    else:
                        advance_payment =+ (-1.0 * invoice_line.price_subtotal)

                res_update	=	{
                                'discount' : discount,
                                'advance_payment' : advance_payment
                                }

                if invoice.tax_line:
                    res_update['amount_tax'] = invoice.tax_line[0].amount

                obj_taxform.write(cr, uid, [taxform_id], res_update)
            else:
                raise osv.except_osv('Warning', 'Invoice already has a taxform or not in open/paid state')

        return {'type': 'ir.actions.act_window_close'}


wizard_create_taxform()


