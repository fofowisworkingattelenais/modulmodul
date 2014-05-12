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

class account_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    _columns = {
        'project_id': fields.many2one(string='Project', obj='project.project', readonly=True,
                                      states={'draft': [('readonly', False)]}),
        'ta_description': fields.text('Description'),
        'ta_qty': fields.char('Quantity', size=256, required=False),
        'nomor': fields.char('Nomor', size=80, required=False),
        'remarks': fields.char('Remarks', size=256, required=False),
        'uang_sebanyak': fields.text('Uang sebanyak'),
        'untuk_pembayaran': fields.text('Untuk pembayaran')
    }

account_invoice()

