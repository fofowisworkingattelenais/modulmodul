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
import decimal_precision as dp
import netsvc


class purchase_order(osv.osv):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    def default_discount_type(self, cr, uid, context={}):
        return 'total'

    def default_purchase_approval_ids(self, cr, uid, ids, context={}):
        print "Default Purchase Approval Ids"
        res = []
        obj_company = self.pool.get('titis.company_purchase_approval')

        company = obj_company.browse(cr, uid, [uid])[0]
        for approval_sequence in company.company_id.purchase_approval_ids:
            value = {
                'name': approval_sequence.name,
                'sequence': approval_sequence.sequence,
                'user_id': approval_sequence.user_id.id,
            }
            res.append(value)
        return res


    def _amount_line_tax(self, cr, uid, line, context=None):
        val = 0.0

        if line.order_id.discount_type == 'total':
            discount = line.order_id.total_discount
        elif line.order_id.discount_type == 'line':
            discount = line.discount

        for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id,
                                                          line.price_unit * (1 - (discount or 0.0) / 100.0),
                                                          line.product_qty)['taxes']:
            val += c.get('amount', 0.0)
        return val


    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    '''
            Add by iCS
            Thursday, 19/09/2013
            menambah method baru
    '''

    def compute_order(self, cr, uid, ids, field_name, context=None):
        res = {}
        cur_obj = self.pool.get('res.currency')
        obj_tax = self.pool.get('account.tax')
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_before_discount': 0.0,
                'amount_untaxed': 0.0,
                'amount_discount': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = disc = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.product_qty * line.discount
                val += self._amount_line_tax(cr, uid, line, context=context)
                #disc += line.tmp

            sebelumDiskon = val1
            diskon = cur_obj.round(cr, uid, cur, order.total_discount)
            jumlahDiskon = sebelumDiskon * (diskon) / 100
            tidakKenaPajak = sebelumDiskon - jumlahDiskon
            pajak = val
            self.write(cr, uid, ids,
                       {'amount_discount': jumlahDiskon, 'amount_before_discount': sebelumDiskon, 'amount_tax': pajak,
                        'amount_untaxed': tidakKenaPajak, 'amount_total': pajak + tidakKenaPajak})

        return True

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        cur_obj = self.pool.get('res.currency')
        obj_tax = self.pool.get('account.tax')
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_before_discount': 0.0,
                'amount_untaxed': 0.0,
                'amount_discount': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = disc = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
                #disc += line.tmp

            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_before_discount'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, disc)
            res[order.id]['amount_discount'] = res[order.id]['amount_before_discount'] - res[order.id]['amount_untaxed']
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']

        return res

    def default_purchase_type(self, cr, uid, context={}):
        return 'material'

    _columns = {
        'name': fields.char('# PO', size=64, required=True, select=True,
                            help='unique number of the purchase order,computed automatically when the purchase order is created',
                            readonly=True),
        'discount_type': fields.char('Discount On', size=64, required=True, readonly=True, states={'draft': [('readonly', True)]}),
        # 'discount_type': fields.selection(selection=[('total', 'Total'), ('line', 'Line')], string='Discount On',
        #                                   required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'total_discount': fields.float(string='Total Discount %', digits=(16, 2), readonly=True,
                                       states={'draft': [('readonly', False)]}),
        'project_id': fields.many2one(string='Project', obj='project.project', readonly=True,
                                      states={'draft': [('readonly', False)]}),

        # Edited by iCS
        # Thursday, 19/09/2013
        # Mengganti tipe field dari function menjadi float

        'amount_discount': fields.float(string='Amount Discount', digits=(16, 2), store=True, readonly=True,
                                        states={'draft': [('readonly', True)]}),
        'amount_untaxed': fields.float(string='Untaxed Amount', digits=(16, 2), store=True, readonly=True,
                                       states={'draft': [('readonly', True)]}),
        'amount_before_discount': fields.float(string='Amount Before Discount', digits=(16, 2), store=True,
                                               readonly=True,
                                               states={'draft': [('readonly', True)]}),
        'amount_tax': fields.float(string='Tax Amount', digits=(16, 2), store=True, readonly=True,
                                   states={'draft': [('readonly', True)]}),
        'amount_total': fields.float(string='Total', digits=(16, 2), store=True, readonly=True,
                                     states={'draft': [('readonly', True)]}),

        'purchase_approval_ids': fields.one2many(stirng='Purchase Order Approval', obj='titis.purchase_approval',
                                                 fields_id='po_id', readonly=True,
                                                 states={'draft': [('readonly', False)]}),
        'approval_id': fields.many2one(string='Waiting Approval From', obj='res.users', readonly=True),
        'requisition_id': fields.many2one(obj='purchase.requisition', string='Purchase Requisition', readonly=False),
        'purchase_type': fields.selection(string='Purchase Type',
                                          selection=[('material', 'Material'), ('service', 'Service')], required=True,
                                          readonly=True, states={'draft': [('readonly', False)]}),


        'catatan': fields.text('Catatan'),
        'analytics_id':fields.many2one('account.analytic.plan.instance','Analytic Distribution',required=True ),
        'subject_desc': fields.char('Subject PO', size=128, required=True, select=True, readonly=False),

        # override semua field total
        #				'amount_untaxed': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Purchase Price'), string='Untaxed Amount',
        #				    store={
        #				        'purchase.order.line': (_get_order, None, 10),
        #				    }, multi="sums", help="The amount without tax"),
        #				'amount_before_discount': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Purchase Price'), string='Amount Before Discount',
        #				    store={
        #				        'purchase.order.line': (_get_order, None, 10),
        #				    }, multi="sums", help="Total without discount"),
        ##				'amount_discount': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Purchase Price'), string='Amount Discount',
        ##				    store={
        ##				        'purchase.order.line': (_get_order, None, 10),
        ##				    }, multi="sums", help="Total amount discount"),
        #				'amount_tax': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Purchase Price'), string='Taxes',
        #				    store={
        #				        'purchase.order.line': (_get_order, None, 10),
        #				    }, multi="sums", help="The tax amount"),
        #				'amount_total': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Purchase Price'), string='Total',
        #				    store={
        #				        'purchase.order.line': (_get_order, None, 10),
        #				    }, multi="sums",help="The total amount"),
    }

    _defaults = {
        'name': lambda *a: '/',
        # Edit by iCS
        # menghilangkan default purchase approval
        # 'purchase_approval_ids': default_purchase_approval_ids,
        'discount_type': default_discount_type,
        'purchase_type': default_purchase_type,
    }

    _sql_constraints = [('name_uniq', 'unique(id)', 'Order Reference must be unique !'), ]

    def create(self, cr, user, vals, context=None):
        vals['name'] = '/'

        new_id = super(purchase_order, self).create(cr, user, vals, context)
        return new_id

    def create_sequence(self, cr, uid, id):
        """
        Method untuk create sequence
        """

        obj_sequence = self.pool.get('ir.sequence')
        obj_project = self.pool.get('project.project')

        purchase = self.browse(cr, uid, [id])[0]
        tanggal = purchase.date_order or datetime.today().strftime('%Y-%m-%d')

        if not purchase.project_id:
            sequence_id = self.pool.get('ir.sequence').search(cr, uid, [('name', '=', 'Purchase Order')])[0]
            new_name = obj_sequence.get_id(cr, uid, sequence_id, 'id', {'tanggal': tanggal})
        else:
            if not purchase.project_id.purchase_sequence_id:
                raise osv_except_osv('Warning!', 'Project purchase sequence has not been set')
                return False
            sequence_id = purchase.project_id.purchase_sequence_id.id
            new_name = obj_sequence.get_id(cr, uid, sequence_id, 'id', {'tanggal': tanggal})

        if purchase.purchase_type == 'material':
            new_name = 'M ' + new_name
        else:
            new_name = 'S ' + new_name

        val = {
            'name': new_name
        }

        self.write(cr, uid, [id], val)

        return True

    def inv_line_create(self, cr, uid, a, ol):
       
        if ol.order_id.discount_type == 'total':
            discount = ol.order_id.total_discount
        elif ol.order_id.discount_type == 'line':
            discount = ol.discount

        return (0, False, {
            'name': ol.name,
            'account_id': a,
            'price_unit': ol.price_unit or 0.0,
            'quantity': ol.product_qty,
            'product_id': ol.product_id.id or False,
            'uos_id': ol.product_uom.id or False,
            
            'invoice_line_tax_id': [(6, 0, [x.id for x in ol.taxes_id])],
            'analytics_id': ol.analytics_id.id or False,
            'asset_category_id': ol.product_id.asset_category_id.id or False,
            
        })

    

    def has_stockable_product(self,cr, uid, ids, *args):
        for order in self.browse(cr, uid, ids):
            for order_line in order.order_line:
                if order_line.product_id and order_line.product_id.product_tmpl_id.type in ('product', 'consu'):
                    return True
        return False
    
    
    def wkf_approve_order(self, cr, uid, ids, context=None):
        super(purchase_order, self).wkf_approve_order(cr, uid, ids, context)

        return True

    def wkf_confirm_order(self, cr, uid, ids, context=None):
        super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context)

        for o in self.browse(cr, uid, ids):
            il = []
            todo = []
            for ol in o.order_line:
                todo.append(ol.id)
                if ol.product_id:
                    a = ol.product_id.product_tmpl_id.property_account_expense.id
                    if not a:
                        a = ol.product_id.categ_id.property_account_expense_categ.id
                    if not a:
                        raise osv.except_osv(('Error !'), ('There is no expense account defined for this product: "%s" (id:%d)') % (ol.product_id.name, ol.product_id.id,))
                else:
                    a = self.pool.get('ir.property').get(cr, uid, 'property_account_expense_categ', 'product.category').id
                fpos = o.fiscal_position or False
                a = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, a)
                il.append(self.inv_line_create(cr, uid, a, ol))

        for id in ids:
            if not self.create_sequence(cr, uid, id):
                return False

            if not self.start_approval(cr, uid, id):
                return False

        return True

    def all_approve(self, cr, uid, ids, context={}):


        for purchase in self.browse(cr, uid, ids):
            if not purchase.purchase_approval_ids:
                wkf_service.trg_validate(uid, 'purchase.order', purchase.id, 'purchase_approve', cr)
                return True

            for approval in purchase.purchase_approval_ids:
                if approval.state == 'waiting' or not approval.state:
                    self.start_approval(cr, uid, purchase.id)
                    return False

        return True

    def start_approval(self, cr, uid, id):
        """

        """
        obj_approval = self.pool.get('titis.purchase_approval')

        approval_ids = obj_approval.search(cr, uid, [('po_id', '=', id), ('state', '=', False)])

        if approval_ids:
            approval_id = approval_ids[0]
            approval = obj_approval.browse(cr, uid, [approval_id])[0]
            obj_approval.write(cr, uid, [approval_id], {'state': 'waiting'})
            self.write(cr, uid, [id], {'approval_id': approval.user_id.id})

        return True

    def button_workflow_approval(self, cr, uid, ids, context={}):
        wkf_service = netsvc.LocalService('workflow')
        obj_approval = self.pool.get('titis.purchase_approval')

        for purchase in self.browse(cr, uid, ids):
            wkf_service.trg_validate(uid, 'purchase.order', purchase.id, 'purchase_approve', cr)

        return True

    def onchange_project_id(self, cr, uid, ids, project_id):
		value = {}
		domain = {}
		warning = {}

		obj_purchase_approval = self.pool.get('titis.purchase_approval')
		obj_project = self.pool.get('project.project')
		obj_user = self.pool.get('res.users')

		value.update({'purchase_approval_ids' : []})

		# Hapus approval yg ada
		# kriteria = [('po_id','in', ids)]
		# purchase_approval_ids = obj_purchase_approval.search(cr, uid, kriteria)
		# if purchase_approval_ids:
		# 	obj_purchase_approval.unlink(cr, uid, purchase_approval_ids)

		# Jika po project, maka approval diambil dari project
		if project_id:
			project = obj_project.browse(cr, uid, [project_id])[0]
			if project.purchase_approval_ids:
				for approval in project.purchase_approval_ids:
					res =	{
									'name' : approval.name,
									'sequence' : approval.sequence,
									'user_id' : approval.user_id.id,
									}

					value['purchase_approval_ids'].append(res)
		else:
			user = obj_user.browse(cr, uid, [uid])[0]
			if user.company_id.purchase_approval_ids:
				for approval in user.company_id.purchase_approval_ids:
					res =	{
									'name' : approval.name,
									'sequence' : approval.sequence,
									'user_id' : approval.user_id.id,
									}
					value['purchase_approval_ids'].append(res)

		return {'value' : value, 'domain' : domain, 'warning' : warning}


    
    
    
    def write(self, cr, uid, ids, vals, context=None):
        if context is None : context = {}
        line_obj = self.pool.get('purchase.order.line')
        
        if vals.get('analytics_id'):
            lines = [line.id for po in self.browse(cr, uid, ids) for line in po.order_line]
            if lines:
                line_obj.write(cr, uid, lines, {'analytics_id': vals['analytics_id']})

        return super(purchase_order, self).write(cr, uid, ids, vals, context=context)


    def action_picking_create(self,cr, uid, ids, *args):
        picking_id = False
        for order in self.browse(cr, uid, ids):
            loc_id = order.partner_id.property_stock_supplier.id
            istate = 'none'
            if order.invoice_method=='picking':
                istate = '2binvoiced'
            pick_name = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking.in')
            picking_id = self.pool.get('stock.picking').create(cr, uid, {
                'name': pick_name,
                'origin': order.name+((order.origin and (':'+order.origin)) or ''),
                'type': 'in',
                'address_id': order.dest_address_id.id or order.partner_address_id.id,
                'invoice_state': istate,
                'purchase_id': order.id,
                'company_id': order.company_id.id,
                'move_lines' : [],
                'project_id' : order.project_id.id,
            })
            todo_moves = []
            for order_line in order.order_line:
                if not order_line.product_id:
                    continue
                if order_line.product_id.product_tmpl_id.type in ('product', 'consu'):
                    dest = order.location_id.id
                    move = self.pool.get('stock.move').create(cr, uid, {
                        'name': order.name + ': ' +(order_line.name or ''),
                        'product_id': order_line.product_id.id,
                        'product_qty': order_line.product_qty,
                        'product_uos_qty': order_line.product_qty,
                        'product_uom': order_line.product_uom.id,
                        'product_uos': order_line.product_uom.id,
                        'date': order_line.date_planned,
                        'commencement_date':order_line.date_planned,
                        # 'date_expected': order_line.date_planned,
                        'location_id': loc_id,
                        'location_dest_id': dest,
                        'picking_id': picking_id,
                        'move_dest_id': order_line.move_dest_id.id,
                        'state': 'draft',
                        'purchase_line_id': order_line.id,
                        'company_id': order.company_id.id,
                        'price_unit': order_line.price_unit,
                       
                    })
                    if order_line.move_dest_id:
                        self.pool.get('stock.move').write(cr, uid, [order_line.move_dest_id.id], {'location_id':order.location_id.id})
                    todo_moves.append(move)
            self.pool.get('stock.move').action_confirm(cr, uid, todo_moves)
            self.pool.get('stock.move').force_assign(cr, uid, todo_moves)
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)
        return picking_id

    


    



purchase_order()							
							





