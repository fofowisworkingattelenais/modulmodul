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


class purchase_requisition(osv.osv):
    _name = 'purchase.requisition'
    _inherit = 'purchase.requisition'

    def default_requisition_approval_ids(self, cr, uid, context={}):
        res = []
        obj_user = self.pool.get('res.users')

        user = obj_user.browse(cr, uid, [uid])[0]

        for approval_sequence in user.company_id.requisition_approval_ids:
            value = {
            'name': approval_sequence.name,
            'sequence': approval_sequence.sequence,
            'user_id': approval_sequence.user_id.id,
            }
            res.append(value)

        return res

    def default_name(self, cr, uid, context={}):
        return '/'

    def default_purchase_type(self, cr, uid, context={}):
        return 'material'

    _columns = {
    'name': fields.char('# PRR', size=32, required=True, readonly=True),
    'pcs_by': fields.char('Purchase By', size=32),
    'project_id': fields.many2one(string='Project', obj='project.project', required=True, readonly=True,
                                  states={'draft': [('readonly', False)]}),
    'date_start': fields.datetime('Requisition Date', readonly=True, states={'draft': [('readonly', False)]}),
    'user_id': fields.many2one(obj='res.users', string='Responsible', readonly=True),
    'approval_id': fields.many2one(string='Waiting Approval From', obj='res.users', readonly=True),
    'warehouse_id': fields.many2one(obj='stock.warehouse', string='Warehouse', required=True, readonly=True,
                                    states={'draft': [('readonly', False)]}),
    'requisition_approval_ids': fields.one2many(stirng='Purchase Requisition Approval',
                                                obj='titis.requisition_approval', fields_id='prr_id', readonly=True,
                                                states={'draft': [('readonly', False)]}),
    'purchase_type': fields.selection(string='Purchase Type',
                                      selection=[('material', 'Material'), ('service', 'Service')], required=True,
                                      readonly=True, states={'draft': [('readonly', False)]}),
    'pr_type': fields.selection(string='Purchase Requisition Type',
                                selection=[('Normal', 'Normal'), ('Urgent', 'Urgent'), ('Top Urgent', 'Top Urgent')],
                                required=True, readonly=True, states={'draft': [('readonly', False)]}),
    'state': fields.selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('waiting', 'Waiting For Approval'),
                               ('in_progress', 'In Progress'), ('cancel', 'Cancelled'), ('done', 'Done')], 'State',
                              required=True),
    'order_id' : fields.many2one(obj='purchase.order', string='Status', readonly=False),
    'po_date_order': fields.date('Order Date', readonly=True, states={'draft': [('readonly', False)]}),

    }

    _defaults = {
    'requisition_approval_ids': default_requisition_approval_ids,
    'name': default_name,
    'purchase_type': default_purchase_type,
    }

    def workflow_action_confirm(self, cr, uid, ids, context={}):
        for id in ids:
            self.run_approval(cr, uid, id)
            self.write(cr, uid, [id], {'state': 'confirm'})

        return True

    def workflow_action_waiting(self, cr, uid, ids, context={}):
        obj_approval = self.pool.get('titis.requisition_approval')

        for requisition in self.browse(cr, uid, ids):
            if requisition.approval_id.id != uid:
                raise osv.except_osv('Warning!', 'You are not authorize to approve this document')
                return False

            self.write(cr, uid, [requisition.id], {'state': 'waiting'})

            if self.check_approval(cr, uid, [requisition.id]):
                self.tender_in_progress(cr, uid, [requisition.id])

            else:
                if requisition.requisition_approval_ids:
                    for approval in requisition.requisition_approval_ids:
                        if approval.approval_status == 'waiting':
                            obj_approval.write(cr, uid, [approval.id], {'approval_status': 'approved',
                                                                        'approval_date': datetime.today().strftime(
                                                                            '%Y-%m-%d %H:%M:%S')})

                            self.run_approval(cr, uid, requisition.id)

                        if self.check_approval(cr, uid, [requisition.id]):
                            self.tender_in_progress(cr, uid, [requisition.id])

                            break
        return True

    def workflow_action_bypass(self, cr, uid, ids, context={}):
        """
        Method untuk bypass approval
        """
        obj_approval = self.pool.get('titis.requisition_approval')

        for requisition in self.browse(cr, uid, ids):
            self.write(cr, uid, [requisition.id], {'state': 'waiting'})
            if self.check_approval(cr, uid, [requisition.id]):
                self.tender_in_progress(cr, uid, [requisition.id])
            else:
                if requisition.requisition_approval_ids:
                    for approval in requisition.requisition_approval_ids:
                        if approval.approval_status == 'waiting':
                            obj_approval.write(cr, uid, [approval.id],
                                               {'approval_status': 'bypass', 'user_bypass_id': uid,
                                                'approval_date': datetime.today().strftime('%Y-%m-%d %H:%M:%S')})

                            self.run_approval(cr, uid, requisition.id)

                        if self.check_approval(cr, uid, [requisition.id]):
                            self.tender_in_progress(cr, uid, [requisition.id])
                            break

        return True

    def check_approval(self, cr, uid, ids, context={}):
        """
        Memeriksa approval. Jika tidak ada approval sequence return True. Jika ada approval sequence yang belum 'Approved' maka return False
        """
        for requisition in self.browse(cr, uid, ids):
            if requisition.requisition_approval_ids:
                for approval in requisition.requisition_approval_ids:
                    if approval.approval_status != 'approved' and approval.approval_status != 'bypass':
                        return False
                return True
            else:
                return True

    def run_approval(self, cr, uid, id):
        requisition = self.browse(cr, uid, [id])[0]
        obj_approval = self.pool.get('titis.requisition_approval')

        if requisition.requisition_approval_ids:
            for approval in requisition.requisition_approval_ids:
                if not approval.approval_status:
                    obj_approval.write(cr, uid, [approval.id], {'approval_status': 'waiting'})
                    self.write(cr, uid, [id], {'approval_id': approval.user_id.id})
                    break

        return True

    def create(self, cr, uid, vals, context=None):
        obj_sequence = self.pool.get('ir.sequence')
        obj_project = self.pool.get('project.project')

        if ('name' not in vals) or (vals.get('name') == '/'):
            if not vals.get('project_id', False):
                sequence_id = self.pool.get('ir.sequence').search(cr, uid, [('name', '=', 'Purchase Requisition Order')])[0]
                new_name = obj_sequence.get_id(cr, uid, sequence_id)

            else:
                project = obj_project.browse(cr, uid, [vals['project_id']])[0]
                if not project.requisition_sequence_id:
                    raise osv_except_osv('Warning!', 'Project purchase requisition sequence has not been set')
                else:
                    sequence_id = project.requisition_sequence_id.id
                    new_name = obj_sequence.get_id(cr, uid, sequence_id, 'id', {'tanggal': vals['date_start'][0:10]})
            vals['name'] = new_name

        new_id = super(purchase_requisition, self).create(cr, uid, vals, context)
        return new_id

    def get_project_id(self, cr, uid, vals, context=None):
        print "MASUK GET PROJECT ID"
        print "-->", vals.get('project_id')
        idProject = 0
        return idProject

    def write(self, cr, uid, ids, vals, context=None):
        if context is None : context = {}
        line_obj = self.pool.get('purchase.requisition.line')

        if vals.get('pcs_by'):
            lines = [line.id for pr in self.browse(cr, uid, ids) for line in pr.line_ids]
            if lines:
                line_obj.write(cr, uid, lines, {'pcs_by': vals['pcs_by']})

        if vals.get('order_id'):
            lines = [line.id for pr in self.browse(cr, uid, ids) for line in pr.line_ids]
            if lines:
                line_obj.write(cr, uid, lines, {'order_id': vals['order_id']})

        if vals.get('po_date_order'):
            lines = [line.id for pr in self.browse(cr, uid, ids) for line in pr.line_ids]
            if lines:
                line_obj.write(cr, uid, lines, {'po_date_order': vals['po_date_order']})

        if vals.get('date_start'):
            lines = [line.id for pr in self.browse(cr, uid, ids) for line in pr.line_ids]
            if lines:
                line_obj.write(cr, uid, lines, {'date_start': vals['date_start']})

        return super(purchase_requisition, self).write(cr, uid, ids, vals, context=context)


    def onchange_project_id(self, cr, uid, ids, project_id):
        value = {}
        domain = {}
        warning = {}

        obj_requisition_approval = self.pool.get('titis.requisition_approval')
        obj_project = self.pool.get('project.project')
        obj_user = self.pool.get('res.users')

        value.update({'requisition_approval_ids': []})

        # Hapus approval yg ada
        # kriteria = [('prr_id', 'in', ids)]
        # requisition_approval_ids = obj_requisition_approval.search(cr, uid, kriteria)
        # if requisition_approval_ids:
        #     obj_requisition_approval.unlink(cr, uid, requisition_approval_ids)

        # Jika prr project, maka approval diambil dari project
        if project_id:
            project = obj_project.browse(cr, uid, [project_id])[0]
            if project.requisition_approval_ids:
                for approval in project.requisition_approval_ids:
                    res = {
                    'name': approval.name,
                    'sequence': approval.sequence,
                    'user_id': approval.user_id.id,
                    }

                    value['requisition_approval_ids'].append(res)
        else:
            user = obj_user.browse(cr, uid, [uid])[0]
            if user.company_id.requisition_approval_ids:
                for approval in user.company_id.requisition_approval_ids:
                    res = {
                    'name': approval.name,
                    'sequence': approval.sequence,
                    'user_id': approval.user_id.id,
                    }
                    value['requisition_approval_ids'].append(res)

        return {'value': value, 'domain': domain, 'warning': warning}


purchase_requisition()							
							






