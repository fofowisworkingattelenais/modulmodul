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
import netsvc

class voucher_approval(osv.osv):
	_name = 'titis.voucher_approval'
	_description = 'Voucher Approval'
	_order = 'voucher_id, sequence'
	_columns =	{
							'name' : fields.char(string='Approval', size=100, required=True),
							'voucher_id' : fields.many2one(string='# Voucher', obj='account.voucher'),
							'sequence' : fields.integer(string='Sequence', required=True),
							'user_id' : fields.many2one(string='Approved By', obj='res.users', required=True),
							'user_bypass_id' : fields.many2one(string='By Pass By', obj='res.users', readonly=True),
							'approval_status' : fields.selection(selection=[('waiting','Waiting For Approval'),('approved','Approved'),('bypass','By Pass')], string='Approval Status', readonly=True),
							'state' : fields.selection(selection=[('waiting','Waiting For Approval'),('approved','Approved'),('bypass','By Pass')], string='Approval Status', readonly=True),
							'approval_date' : fields.datetime(string='Approval Time', readonly=True),
							}						
							
	def button_action_approved(self, cr, uid, ids, context={}):
		obj_voucher = self.pool.get('account.voucher')
		
		
		
		for approval in self.browse(cr, uid, ids):
			wkf_service = netsvc.LocalService('workflow')
			
			if not self.check_user(cr, uid, approval.id):
				return False
			
			self.write(cr, uid, [approval.id], {'state' : 'approved',  'approval_date' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')})
			wkf_service.trg_validate(uid, 'account.voucher', approval.voucher_id.id, 'button_ready', cr)	
			obj_voucher.write(cr, uid, [approval.voucher_id.id], {})	
		return True
		
	def button_action_bypass(self, cr, uid, ids, context={}):
		obj_voucher = self.pool.get('account.voucher')
		for approval in self.browse(cr, uid, ids):
			wkf_service = netsvc.LocalService('workflow')
			
			self.write(cr, uid, [approval.id], {'state' : 'bypass',  'user_bypass_id' : uid, 'approval_date' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')})
			wkf_service.trg_validate(uid, 'account.voucher', approval.voucher_id.id, 'button_ready', cr)	
			obj_voucher.write(cr, uid, [approval.voucher_id.id], {})	
		return True
		
	def check_user(self, cr, uid, id):
		approval = self.browse(cr, uid, [id])[0]
		
		if approval.user_id.id == uid:
			return True
		else:
			raise osv.except_osv('Warning!', 'You do not have authorization to approve this document')
			return False
			
voucher_approval()							
							






