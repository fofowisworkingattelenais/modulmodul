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

class requisition_approval(osv.osv):
	_name = 'titis.requisition_approval'
	_description = 'Purchase Requisition Approval'
	_columns =	{
							'name' : fields.char(string='Approval', size=100, required=True),
							'prr_id' : fields.many2one(string='Purchase Requisition', obj='purchase.requisition'),
							'sequence' : fields.integer(string='Sequence', required=True),
							'user_id' : fields.many2one(string='Approved By', obj='res.users', required=True),
							'user_bypass_id' : fields.many2one(string='By Pass By', obj='res.users'),
							'approval_status' : fields.selection(selection=[('waiting','Waiting For Approval'),('approved','Approved'),('bypass','By Pass')], string='Approval Status', readonly=True),
							'approval_date' : fields.datetime(string='Approval Time', readonly=True),
							}						
requisition_approval()							
							






