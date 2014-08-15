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
from datetime import datetime
from tools.translate import _
import netsvc
import decimal_precision as dp

class account_voucher(osv.osv):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
    _order = 'number'

    def default_voucher_type_id(self, cr, uid, context=None):
        obj_account_voucher_type = self.pool.get('titis.voucher_type')
        voucher_type = []

        if context.get('voucher_type', False):
            kriteria = [('name', '=', context['voucher_type'])]

            voucher_type_ids = obj_account_voucher_type.search(cr, uid, kriteria)
            if voucher_type_ids : voucher_type = voucher_type_ids[0]

        return voucher_type

    def default_type(self, cr, uid, context=None):
        obj_account_voucher_type = self.pool.get('titis.voucher_type')

        voucher_type_id = self.default_voucher_type_id(cr, uid, context)

        if not voucher_type_id : return self._get_type(cr, uid, context)

        voucher_type = obj_account_voucher_type.browse(cr, uid, [voucher_type_id])[0]

        return voucher_type.default_header_type

    def default_journal_id(self, cr, uid, context={}):
        return False

    def default_approval_ids(self, cr, uid, context={}):
        res = []
        obj_user = self.pool.get('res.users')

        user = obj_user.browse(cr, uid, [uid])[0]

        for approval_sequence in user.company_id.voucher_approval_ids:
            if approval_sequence.voucher_type_id.name == context.get('voucher_type', False):
                value =	{
                                'name' : approval_sequence.name,
                                'sequence' : approval_sequence.sequence,
                                'user_id' : approval_sequence.user_id.id,
                                }
                res.append(value)

        return res


    _columns =	{
                        'voucher_type_id' : fields.many2one(obj='titis.voucher_type', string='Voucher Type', readonly=True, states={'draft':[('readonly',False)]}),
                        'payment_method' : fields.selection(string='Payment Method', selection=[('bank_transfer','Bank Transfer'),('cheque','Cheque'),('giro','Giro')], readonly=True, states={'draft':[('readonly',False)]}),
                        'cheque_number' : fields.char(string='Cheque Number', size=50, readonly=True, states={'draft':[('readonly',False)]}),
                        'cheque_date' : fields.date(string='Cheque Date', readonly=True, states={'draft':[('readonly',False)]}),
                        'cheque_partner_bank_id' : fields.many2one(obj='res.partner.bank', string='Destination Bank Account', readonly=True, states={'draft':[('readonly',False)]}),
                        'cheque_bank_id' : fields.related('cheque_partner_bank_id', 'bank', type='many2one', relation='res.bank', string='Bank', store=True, readonly=True),
                        'cheque_recepient' : fields.char(string='Cheque Recepient', size=100, readonly=True, states={'draft':[('readonly',False)]}),
                        'cheque_is_giro' : fields.boolean('Is Giro?'),
                        'state' : fields.selection(selection=[('draft','Draft'),('confirm','Confirm'), ('waiting','Waiting For Approval'),('ready','Ready To Process'),('proforma','Pro-forma'),('posted','Posted'),('cancel','Cancelled')], string='State', readonly=True),

                         'project_id': fields.many2one(string='Project', obj='project.project', required=True),

                         'user_id': fields.many2one('res.users', 'Finance User', readonly=True, states={'draft':[('readonly',False)]}),
                        'partner_id': fields.many2one(obj='res.partner', string='Partner'),


                        # APPROVAL
                        'approval_ids' : fields.one2many(string='Voucher Approval', obj='titis.voucher_approval', fields_id='voucher_id', readonly=True, states={'draft':[('readonly',False)]}),
                        'approval_id' : fields.many2one(string='Waiting Approval From', obj='res.users', readonly=True),

                        'analytics_id' : fields.many2one(obj='account.analytic.plan.instance', string='Analytic Distribution'),

                        # PENYESUAIAN STATE
                        'writeoff_acc_id' : fields.many2one('account.account', 'Write-Off account', readonly=False, states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]}),
                        'date' : fields.date('Date', readonly=False, select=True, states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]}, help="Effective date for accounting entries"),
                        'currency_id' : fields.many2one('res.currency', 'Currency', readonly=False, states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]}),
                        'journal_id':fields.many2one('account.journal', 'Journal', required=True, readonly=False, states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]}),

                        'line_ids':fields.one2many('account.voucher.line','voucher_id','Voucher Lines', readonly=False),

                        'move_line_id':fields.one2many('account.voucher.line','voucher_id','move_line_id'),

                        'line_cr_ids':fields.one2many('account.voucher.line','voucher_id','Credits', domain=[('type','=','cr')], context={'default_type':'cr'}, readonly=False, states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]}),
                        'line_dr_ids':fields.one2many('account.voucher.line','voucher_id','Debits', domain=[('type','=','dr')], context={'default_type':'dr'}, readonly=False, states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]}),
                        'period_id': fields.many2one('account.period', 'Period', required=True, readonly=False, states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]}),
                        'account_id':fields.many2one('account.account', 'Account', required=True, readonly=False, states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]}),
                        'amount': fields.float('Total', digits_compute=dp.get_precision('Account'), required=True, readonly=False, states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]}),


                        }

    _defaults =	{
                        'voucher_type_id' : default_voucher_type_id,
                        'type' : default_type,
                        'journal_id' : default_journal_id,
                        'approval_ids' : default_approval_ids,
                                    'user_id': lambda s, cr, u, c: u,
                        }

    def copy(self, cr, uid, id, default={}, context=None):

        approval = self.default_approval_ids(cr, uid,context)
        val = []

        for item in approval:
            val.append((0,False,item))

        default.update({'approval_ids' : val, 'approval_id' : False})
        return  super(account_voucher, self).copy(cr, uid, id, default, context)


    def workflow_action_confirm(self, cr, uid, ids, context={}):
        """
        Method yang dijalankan ketika confirm

        * Merubah state
        """
        for id in ids:

            self.write(cr, uid, [id], {'state':'confirm'})
        return True

    def workflow_action_waiting(self, cr, uid, ids, context={}):
        """
        Method yang dijalankan ketika waiting

        * Merubah state
        """
        for id in ids:
            if not self.start_approval(cr, uid, id):
                return False

            self.write(cr, uid, [id], {'state':'waiting'})
        return True

    def workflow_action_ready(self, cr, uid, ids, context={}):
        """
        Method yang dijalankan ketika ready

        * Merubah state
        """
        for id in ids:

            self.write(cr, uid, [id], {'state':'ready', 'approval_id' : False})
        return True

    def workflow_action_proforma(self, cr, uid, ids, context={}):
        """
        Method yang dijalankan ketika confirm

        * Merubah state
        * Memberikan nomor pada voucher
        """
        for id in ids:
            if not self.create_voucher_name(cr, uid, id):
                return False

            self.write(cr, uid, [id], {'state':'proforma'})
        return True

    def workflow_action_posted(self, cr, uid, ids, context={}):
        """
        Method yang dijalankan ketika confirm

        * Merubah state
        * Memberikan nomor pada voucher jika belum ada nomor
        * Membuat penjurnalan
        """
        for id in ids:

            if not self.create_voucher_name(cr, uid, id):
                return False

            if not self.create_account_move(cr, uid, id):
                return False

            self.write(cr, uid, [id], {'state':'posted'})
        return True

    def workflow_action_cancel(self, cr, uid, ids, context={}):
        """
        Method yang dijalankan ketika cancel

        * Merubah state
        """
        for id in ids:
            if not self.cancel_account_voucher(cr, uid, id):
                return False

            self.write(cr, uid, [id], {'state':'cancel', 'approval_id' : False})
        return True

    def create_voucher_name(self, cr, uid, id):
        """
        Method untuk memberikan nomor pada voucher. Sequence diambil dari journal
        """
        obj_sequence = self.pool.get('ir.sequence')

        voucher = self.browse(cr, uid, [id])[0]

        # Jika number sudah ada maka tidak perlu dibuat baru
        if voucher.number:
            return True

        if voucher.journal_id.sequence_id.id:
            name = obj_sequence.get_id(cr, uid, voucher.journal_id.sequence_id.id, 'id', {'tanggal' : voucher.date})

        if not name:
            raise osv.except_osv(_('Error !'), _('Please define a sequence on the journal and make sure it is activated !'))

        res	=	{
                    'number' : name,
                    }

        self.write(cr, uid, [id], res)
        return True

    def set_to_draft(self, cr, uid, id, context={}):
        """
        Method yang dijalankan untuk merubah cancel -> draft
        """
        wkf_service = netsvc.LocalService('workflow')
        obj_approval = self.pool.get('titis.voucher_approval')

        voucher = self.browse(cr, uid, [id], context)[0]

        wkf_service.trg_delete(uid, 'account.voucher', id, cr)
        wkf_service.trg_create(uid, 'account.voucher', id, cr)

        self.write(cr, uid, [id], {'state':'draft'})

        if voucher.approval_ids:
            for approval in voucher.approval_ids:
                val =	{
                            'state' : False,
                            'approval_date' : False,
                            'user_bypass_id' : False,
                            }
                obj_approval.write(cr, uid, approval.id, val)

        return True

    def button_set_to_draft(self, cr, uid, ids, context={}):
        """
        Method yang dijalankan ketika user menekan tombol set to draft
        """

        for id in ids:
            if not self.set_to_draft(cr, uid, id, context):
                return False

        return True

    def button_cancel(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.cancel_account_voucher(cr, uid, id):
                return False

            if not self.cancel_workflow_instance(cr, uid, id):
                return False

            self.write(cr, uid, [id], {'state' : 'cancel'})
        return True

    def cancel_workflow_instance(self, cr, uid, id):
        wkf_service = netsvc.LocalService('workflow')

        wkf_service.trg_delete(uid, 'account.voucher', id, cr)
        wkf_service.trg_create(uid, 'account.voucher', id, cr)
        wkf_service.trg_validate(uid, 'account.voucher', id, 'button_cancel', cr)

        return True

    def cancel_account_voucher(self, cr, uid, id, context=None):

        obj_reconcile = self.pool.get('account.move.reconcile')
        obj_move = self.pool.get('account.move')
        obj_move_line = self.pool.get('account.move.line')

        voucher = self.browse(cr, uid, [id], context)[0]

        # Batalkan rekonsiliasi setiap voucher line
        for line in voucher.move_ids:
            if line.reconcile_id:
                move_lines = [move_line.id for move_line in line.reconcile_id.line_id]
                move_lines.remove(line.id)
                obj_reconcile(cr, uid, line.reconcile_id.id)
                if len(move_lines) >= 2:
                    obj_move_line.reconcile_partial(cr, uid, move_lines, 'auto',context=context)

        # Hapus account.move
        if voucher.move_id:
            obj_move.button_cancel(cr, uid, [voucher.move_id.id])
            obj_move.unlink(cr, uid, [voucher.move_id.id])

        res = 	{
                    'move_id' : False,
                    }

        self.write(cr, uid, [id], res)

        return True

    def all_approve(self, cr, uid, ids, context={}):


        for voucher in self.browse(cr, uid, ids):
            if not voucher.approval_ids:
                raise osv.except_osv('a', 'b')
                return True


            for approval in voucher.approval_ids:

                if approval.state == 'waiting' or not approval.state:
                    self.start_approval(cr, uid, voucher.id)
                    return False

        return True

    def start_approval(self, cr, uid, id):
        obj_approval = self.pool.get('titis.voucher_approval')

        approval_ids = obj_approval.search(cr, uid, [('voucher_id','=', id),('state', '=', False)])


        if approval_ids:
            approval_id = approval_ids[0]
            approval = obj_approval.browse(cr, uid, [approval_id])[0]
            obj_approval.write(cr, uid, [approval_id], {'state' : 'waiting'})
            self.write(cr, uid, [id], {'approval_id' : approval.user_id.id})

        return True



    def create_account_move(self, cr, uid, id):
        """
        Method untuk membuat penjurnalan
        """

        context = {}

        obj_move = self.pool.get('account.move')
        obj_move_line = self.pool.get('account.move.line')
        obj_currency = self.pool.get('res.currency')
        obj_tax = self.pool.get('account.tax')
        obj_sequence = self.pool.get('ir.sequence')
        obj_voucher_line = self.pool.get('account.voucher.line')

        voucher = self.browse(cr, uid, [id], context)[0]
        line_total = 0.0 # variabel untuk menampung saldo account.move.line
        all_move_pair = []

        # Jika move_id sudah ada maka continue
        if voucher.move_id:
            return True

        context_multi_currency = context.copy()
        context_multi_currency.update({'date': voucher.date})

        # membuat  account.move
        for line in voucher.line_ids:
            move = 	{
                            'name' : voucher.number,
                            'journal_id' : voucher.journal_id.id,
                            'narration ': voucher.narration,
                            'date' : voucher.date,
                            'ref' : 'ref', #TODO
                            'period_id' : voucher.period_id and voucher.period_id.id or False,
                            'partner_id': line.partner_id.id
                            }
            move_id = obj_move.create(cr, uid, move)

            # mengupdate field move_id voucher
            self.write(cr, uid, [id], {'move_id' : move_id})

            # membuat baris pertama account.move.line
            company_currency = voucher.journal_id.company_id.currency_id.id
            current_currency = voucher.currency_id.id
            debit = 0.0
            credit = 0.0

            # konversi amount ke dalam company currency

            if voucher.type in ('purchase', 'payment'):
                credit = obj_currency.compute(cr, uid, current_currency, company_currency, voucher.amount, context=context_multi_currency)
            elif voucher.type in ('sale', 'receipt'):
                debit = obj_currency.compute(cr, uid, current_currency, company_currency, voucher.amount, context=context_multi_currency)

            if debit < 0:
                credit = -debit
                debit = 0.0
            if credit < 0:
                debit = -credit
                credit = 0.0
            sign = debit - credit < 0 and -1 or 1


            move_line = 	{
                                        'name' : voucher.name or '/',
                                        'debit' : debit,
                                        'credit' : credit,
                                        'account_id' : voucher.account_id.id,
                                        'move_id' : move_id,
                                        'journal_id' : voucher.journal_id.id,
                                        'period_id' : voucher.period_id.id,
                                        #TODO
                                        # 'partner_id' : line.partner_id.id,
                                        'currency_id' : company_currency <> current_currency and  current_currency or False,
                                        'amount_currency' : company_currency <> current_currency and sign * voucher.amount or 0.0,
                                        'date' : voucher.date,
                                        'date_maturity' : voucher.date_due
                                        }
            obj_move_line.create(cr, uid, move_line)


            # line_total untuk baris pertama
            line_total = debit - credit

            rec_list_ids = []

            #TODO: Ini seperti nya ga usah
            #line_total = debit - credit
            #if inv.type == 'sale':
                #line_total = line_total - currency_pool.compute(cr, uid, inv.currency_id.id, company_currency, inv.tax_amount, context=context_multi_currency)
            #elif inv.type == 'purchase':
                #line_total = line_total + currency_pool.compute(cr, uid, inv.currency_id.id, company_currency, inv.tax_amount, context=context_multi_currency)


            # Create one account.move.line for each voucher.line
            for line in voucher.line_ids:
                line_result, line_amount, move_pair = obj_voucher_line.create_account_move_line(cr, uid, line.id)

                if not line_result:
                    return False

                if len(move_pair) > 0:
                    all_move_pair.append(move_pair)

                line_total += line_amount

            # Buat move.line untuk selisih kurs
            currency = voucher.currency_id or voucher.journal_id.currency or voucher.journal_id.company_id.currency_id


            if not obj_currency.is_zero(cr, uid, currency, line_total):
                if not voucher.writeoff_acc_id:
                    raise osv.except_osv('Warning!', 'Please fill currency difference account')
                    return False

                diff = line_total
                move_line = 	{
                                            'name' : 'Currency difference for %s' % (voucher.number),
                                            'debit' : diff < 0 and -diff or 0.0,
                                            'credit' : diff > 0 and diff or 0.0,
                                            'account_id' : voucher.writeoff_acc_id.id, #TODO
                                            'move_id' : move_id,
                                            'journal_id' : voucher.journal_id.id,
                                            'period_id' : voucher.period_id.id,
                                            'date' : voucher.date,
                                            'partner_id' : line.partner_id.id,

                                            }


                obj_move_line.create(cr, uid, move_line)


            # reconcile voucher line
            for move_pair_item in all_move_pair:
                obj_move_line.reconcile_partial(cr, uid, move_pair_item)

            # Post account.move
            obj_move.post(cr, uid, [move_id], context={})

            return True



    def first_move_line_get(self, cr, uid, voucher_id, move_id, company_currency, current_currency, context=None):
        '''
        Override untuk menyesuaikan field yang berkaitan dengan cek/giro
        '''
        voucher = self.browse(cr, uid, [voucher_id])[0]

        res =	{
                    'payment_method' : voucher.payment_method,
                    'cheque_number' : voucher.cheque_number,
                    'cheque_date' : voucher.cheque_date,
                    'cheque_partner_bank_id' : voucher.cheque_partner_bank_id.id,
                    'cheque_recepient' : voucher.cheque_recepient
                    }

        move_line = super(account_voucher, self).first_move_line_get(cr, uid, voucher_id, move_id, company_currency, current_currency)

        move_line.update(res)

        return move_line

    def check_total_voucher(self, cr, uid, id):
        """
        Method untuk melakukan pengecekan agar total voucher == sum amount semua voucher line
        """

        voucher = self.browse(cr, uid, [id])[0]

        total = 0.0
        if voucher.line_ids:
            for line in voucher.line_ids:
                total += line.amount

        if voucher.amount == total:
            return True
        else:
            return False

    def proforma_voucher(self, cr, uid, ids, context=None):
        """
        Override
        """

        for id in ids:
            if not self.check_total_voucher(cr, uid, id):
                raise osv.except_osv('Warning!', 'Total voucher is not equal with line total')
                return False
            pass

        return super(account_voucher, self).proforma_voucher(cr, uid, ids, context)

    def onchange_journal_id(self, cr, uid, ids, journal_id):
        value = {}
        domain = {}
        warning = {}

        obj_journal = self.pool.get('account.journal')

        if journal_id:
            journal = obj_journal.browse(cr, uid, [journal_id])[0]
            value['account_id'] = journal.default_debit_account_id.id
            value['currency_id'] = journal.currency and journal.currency.id or False


        return {'value' : value, 'domain' : domain, 'warning' : warning}

    def onchange_date(self, cr, uid, ids, date, context=None):
        """
        @param date: latest value from user input for field date
        @param args: other arguments
        @param context: context arguments, like lang, time zone
        @return: Returns a dict which contains new values, and context
        """
        value = {}
        domain = {}
        warning = {}

        obj_period = self.pool.get('account.period')

        if context is None: context = {}

        period_ids = obj_period.find(cr, uid, date, context=context)

        if period_ids:
            value.update({'period_id' : period_ids[0]})
        return {'value' : value, 'domain' : domain, 'warning' : warning}

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        res = super(account_voucher, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        x = []
        mod_obj = self.pool.get('ir.model.data')
        obj_account_voucher_type = self.pool.get('titis.voucher_type')
        if context is None: context = {}

        voucher_type = context.get('voucher_type')

        if voucher_type and view_type == 'form':

            kriteria = [('name','=',voucher_type)]
            voucher_type_ids = obj_account_voucher_type.search(cr, uid, kriteria)[0]

            voucher = obj_account_voucher_type.browse(cr, uid, voucher_type_ids, context=context)

            result = mod_obj.get_object_reference(cr, uid, voucher.modul_origin, voucher.model_view_form)
            result = result and result[1] or False
            view_id = result

            if voucher.allowed_journal_ids:
                for journal in voucher.allowed_journal_ids:
                        x.append(journal.id)
            domain_journal = list(set(x))

            for field in res['fields']:
                if field == 'journal_id':
                    res['fields'][field]['domain'] = [('id','in',domain_journal)]
        #raise osv.except_osv('a', str(res))
        return res



account_voucher()

