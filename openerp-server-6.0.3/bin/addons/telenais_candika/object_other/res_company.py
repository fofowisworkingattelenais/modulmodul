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


from osv import fields, osv

class res_company(osv.osv):
    _name = 'res.company'
    _inherit = 'res.company'

    _columns = {
                'default_account_cash_register_id' : fields.property(obj_prop='account.account', type='many2one', relation='account.account',string='Default Account Cash Register', method=True, view_load=True, required=False),
                'default_account_diskon_id' : fields.property(obj_prop='account.account', type='many2one', relation='account.account',string='Default Account Diskon', method=True, view_load=True, required=False),
                'default_account_penjualan_id' : fields.property(obj_prop='account.account', type='many2one', relation='account.account',string='Default Account Penjualan', method=True, view_load=True, required=False),
                'default_account_konsiensi_penjualan_id' : fields.property(obj_prop='account.account', type='many2one', relation='account.account',string='Default Account Konsiensi Penjualan', method=True, view_load=True, required=False),
                'default_account_retur_id' : fields.property(obj_prop='account.account', type='many2one', relation='account.account',string='Default Account Retur', method=True, view_load=True, required=False),
                }
            
res_company()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

