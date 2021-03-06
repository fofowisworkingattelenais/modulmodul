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
import netsvc

class bank_receipt(osv.osv):
	_name = 'titis.bank_receipt'
	_inherit = 'account.voucher'
	_table = 'account_voucher'
	_description = 'Bank Receipt'
	
	def check_access_rights(self, cr, uid, operation, raise_exception=True):
		"""
		override in order to redirect the check of access rights on the account.voucher object
		"""
		return self.pool.get('account.voucher').check_access_rights(cr, uid, operation, raise_exception=raise_exception)
		
	def check_access_rule(self, cr, uid, ids, operation, context=None):
		"""
		override in order to redirect the check of access rules on the account.voucher object
		"""
		return self.pool.get('account.voucher').check_access_rule(cr, uid, ids, operation, context=context)
		
	def create(self, cr, uid, value, context=None):
		"""
		override method orm create
		"""
		new_id = super(bank_receipt, self).create(cr, uid, value, context)
		
		wkf_service = netsvc.LocalService('workflow')
		wkf_service.trg_create(uid, 'account.voucher', new_id, cr)
		
		return new_id
		
	def unlink(self, cr, uid, ids, context=None):
		"""
		override method orm
		"""
		wkf_service = netsvc.LocalService('workflow')
		for id in ids:
			wkf_service.trg_delete(uid, 'account.voucher', id, cr)
			
		return super(bank_receipt, self).unlink(cr, uid, ids, context)
		
	def button_proforma_voucher(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'proforma_voucher', cr)
			
		return True
		
	def button_cancel_voucher(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'cancel_voucher', cr)
			
		return True	
		
	def button_proforma_voucher(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'proforma_voucher', cr)
			
		return True
		
	def button_cancel_voucher(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'cancel_voucher', cr)
			
		return True	
		
	def button_workflow_action_confirm(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
		
			#TODO: Harusnya ini ada di account.voucher
			if not self.check_total_voucher(cr, uid, id):
				raise osv.except_osv('Warning!', 'Total voucher is not equal with line total')
				return False		
				
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_confirm', cr)
			

		return True		
		
	def button_workflow_action_waiting(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_waiting', cr)
			
		return True			
		
	def button_workflow_action_proforma(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_proforma', cr)
			
		return True		
		
	def button_workflow_action_posted(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_posted', cr)
			
		return True		
		
	def button_workflow_action_cancel(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_cancel', cr)
			
		return True		
		
	def button_workflow_action_ready(self, cr, uid, ids, context={}):
		wkf_service = netsvc.LocalService('workflow')
		
		for id in ids:
			wkf_service.trg_validate(uid, 'account.voucher', id, 'button_ready', cr)
			
		return True					
		
        def onchange_project_id(self, cr, uid, ids, project_id):
		value = {}
		domain = {}
		warning = {}

		obj_purchase_approval = self.pool.get('titis.voucher_approval')
		obj_project = self.pool.get('project.project')
		obj_user = self.pool.get('res.users')

		value.update({'approval_ids' : []})

		# Hapus approval yg ada
		# kriteria = [('po_id','in', ids)]
		# purchase_approval_ids = obj_purchase_approval.search(cr, uid, kriteria)
		# if purchase_approval_ids:
		# 	obj_purchase_approval.unlink(cr, uid, purchase_approval_ids)

		# Jika po project, maka approval diambil dari project
		if project_id:
			project = obj_project.browse(cr, uid, [project_id])[0]
			if project.bank_receipt_approval_ids:
				for approval in project.bank_receipt_approval_ids:
					res =	{
									'name' : approval.name,
									'sequence' : approval.sequence,
									'user_id' : approval.user_id.id,
									}

					value['approval_ids'].append(res)
		else:
			user = obj_user.browse(cr, uid, [uid])[0]
			if user.company_id.voucher_approval_ids:
				for approval in user.company_id.voucher_approval_ids:
					res =	{
									'name' : approval.name,
									'sequence' : approval.sequence,
									'user_id' : approval.user_id.id,
									}
					value['approval_ids'].append(res)

		return {'value' : value, 'domain' : domain, 'warning' : warning}
					

bank_receipt()




