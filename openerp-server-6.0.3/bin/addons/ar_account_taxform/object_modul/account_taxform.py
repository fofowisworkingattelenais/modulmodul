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


from osv import fields, osv, orm
import decimal_precision as dp
import time


class account_taxform(osv.osv):
    _name = "account.taxform"
    _description = "Account Taxform"

    def default_state(self, cr, uid, context={}):
        return 'draft'

    _columns = 	{
        'name' : fields.char('Taxform ID', size=30, required=True),
        'company_id' : fields.many2one(obj='res.company', string='Company', required=True),
        'company_address' : fields.many2one(obj='res.partner.address', string='Company Address', required=True),
        'company_npwp' : fields.char('Company NPWP', size=30, required=True),
        'invoice_id' : fields.many2one(obj='account.invoice', string='Invoice ID', required=True, readonly=True),
        'partner_id' : fields.many2one(obj='res.partner', string='Partner', required=True),
        'partner_address_id' : fields.many2one(obj='res.partner.address', string='Partner Address', required=True),
        'partner_npwp' : fields.char('Partner NPWP', size=30, required=True),
        'signature_id' : fields.many2one(obj='res.users', string='Signature', readonly=True),
        'category_id' : fields.many2one(obj='account.taxform_category', string='Control'),
        'discount':fields.float(string='Discount', digits_compute=dp.get_precision('Account'), required=True),
        'advance_payment':fields.float(string='Amount Advance Payment', digits_compute=dp.get_precision('Account'), required=True),
        'untaxed':fields.float(string='Untaxed', digits_compute=dp.get_precision('Account'), required=True),
        'base':fields.float(string='Base', digits_compute=dp.get_precision('Account'), required=True),
        'amount_tax':fields.float(string='Amount Tax', digits_compute=dp.get_precision('Account'), required=True),
        'taxform_line_ids' : fields.one2many(obj='account.taxform_line', fields_id='taxform_id', string='Tax Line'),
        'taxform_date' : fields.date(string='Taxform Date', required=True),
        'state' : fields.selection([('draft','Draft'),('printed','Printed'),('cancel','Cancel')], 'Status', readonly=True),
        'kurs_pajak': fields.float(string='Kurs Pajak', digits_compute=dp.get_precision('Account'), required=True),
        'result_pajak': fields.float(string='Result Pajak', digits_compute=dp.get_precision('Account'), required=True),
        'result_pajak_ppn': fields.float(string='Result Pajak ppn', digits_compute=dp.get_precision('Account')),
        'berdasarkan_no': fields.char('Kurs Berdasarkan', size=50),
        'berdasarkan_date': fields.date(string='Berdasarkan Tanggal'),
        'description': fields.text('Description'),
    }

    _defaults =	{
       'state' : default_state,
    }

    def create_sequence(self, cr, uid, ids, context=None):
        obj_taxform = self.pool.get('account.taxform')
        obj_sequence = self.pool.get('ir.sequence')
        obj_taxform_sequence = self.pool.get('account.taxform_sequence')

        for taxform in obj_taxform.browse(cr, uid, ids):
            if taxform.invoice_id.company_id.company_tax_id:
                sequence_id = taxform.invoice_id.company_id.company_tax_id.sequence_taxform_id and taxform.invoice_id.company_id.company_tax_id.sequence_taxform_id.id or False
            else:
                sequence_id = taxform.invoice_id.company_id.sequence_taxform_id and taxform.invoice_id.company_id.sequence_taxform_id.id or False

            if not sequence_id:
                raise osv.except_osv('Warning!', 'No taxform sequence defined')


            sequence = obj_sequence.get_id(cr, uid, sequence_id, 'id', {'period_id':False})

            obj_taxform.write(cr, uid, [taxform.id], {'name':sequence, 'state':'printed'})

            val_sequence =	{
                'name' : sequence,
                'taxform_id' : taxform.id,
                'sequence_id' : sequence_id,
            }
            obj_taxform_sequence.create(cr, uid, val_sequence)

        return True

    def button_compute(self, cr, uid, ids, context={}):

        obj_taxform = self.pool.get('account.taxform')
        obj_currency = self.pool.get('res.currency')

        for taxform in obj_taxform.browse(cr, uid, ids):
            untaxed = 0.0
            for line in taxform.taxform_line_ids:
                untaxed += line.subtotal
            base = untaxed - taxform.discount - taxform.advance_payment

            result_pajak = taxform.kurs_pajak * taxform.base
            result_pajak_ppn = taxform.kurs_pajak * taxform.amount_tax
            res = {
                'untaxed': untaxed,
                'base': base,
                'amount_tax': obj_currency.round(cr, uid, taxform.invoice_id.currency_id, 0.1000 * base),
                'result_pajak': result_pajak,
                'result_pajak_ppn': result_pajak_ppn
            }
            obj_taxform.write(cr, uid, [taxform.id], res)

        return True


account_taxform()