# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _

class account_open_closed_fiscalyear(osv.osv_memory):
    _name = "account.open.closed.fiscalyear"
    _description = "Choose Fiscal Year"
    _columns = {
       'fyear_id': fields.many2one('account.fiscalyear', \
                                 'Fiscal Year to Open', required=True, help='Select Fiscal Year which you want to remove entries for its End of year entries journal'),
    }

    def remove_entries(self, cr, uid, ids, context=None):
        fy_obj = self.pool.get('account.fiscalyear')
        move_obj = self.pool.get('account.move')

        data = self.read(cr, uid, ids, [], context=context)[0]
        data_fyear = fy_obj.browse(cr, uid, data['fyear_id'], context=context)
        if not data_fyear.end_journal_period_id:
            raise osv.except_osv(_('Error !'), _('No End of year journal defined for the fiscal year'))
        period_journal = data_fyear.end_journal_period_id
        ids_move = move_obj.search(cr, uid, [('journal_id','=',period_journal.journal_id.id),('period_id','=',period_journal.period_id.id)])
        if ids_move:
            cr.execute('delete from account_move where id IN %s', (tuple(ids_move),))
        return {'type': 'ir.actions.act_window_close'}

account_open_closed_fiscalyear()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: