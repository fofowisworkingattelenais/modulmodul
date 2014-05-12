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

class project_purchase_approval(osv.osv):
	_name = 'titis.project_purchase_approval'
	_description = 'Project Purchase Approval'
	_columns =	{
							'name' : fields.char(string='Approval', size=100, required=True),
							'project_id' : fields.many2one(string='Project', obj='project.project'),
							'sequence' : fields.integer(string='Sequence', required=True),
							'user_id' : fields.many2one(string='Approved By', obj='res.users', required=True),
							}						
project_purchase_approval()							
							






