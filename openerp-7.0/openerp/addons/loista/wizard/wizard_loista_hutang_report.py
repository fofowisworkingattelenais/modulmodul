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

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from osv import fields, osv
from osv.orm import browse_record, browse_null
from tools.translate import _


class wizard_loista_hutang_report(osv.osv_memory):
	_name = 'loista.wizard_loista_hutang_report'
	_description = 'Wizard Loista Hutang Report'

	_columns = {
				'tanggal' : fields.date(required=True, string='Date'),
	}

	def cetak_report(self, cr, uid, ids, context=None):
		datas = {}
		if context is None:
			context = {}

		data = self.read(cr, uid, ids, [], context)[0]

		datas =	{
				'ids' : context.get('active_ids', []),
				'model' : 'account.account',
				'form' : data
				}

		return {
				'type' : 'ir.actions.report.xml',
				'report_name' : 'loista_hutang_report',
				'datas' : datas
				}


wizard_loista_hutang_report()