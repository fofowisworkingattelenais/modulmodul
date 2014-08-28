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


class stock_picking_in(osv.osv_memory):
   
   
    _inherit = 'stock.picking.in'

    _columns = {
                # 'karyawan_id' : fields.many2one('hr.employee', 'User Request',required=False),
                'jenis_dokumen_id' : fields.many2one('gdi.jenis_dokumen_pabean', 'Jenis Dokumen',required=False),
                'nomor_dokumen_pabean' : fields.char(string='Nomor Dokumen Pabean', size=50, required=False),
                'tanggal_dokumen_pabean' : fields.date(string='Tanggal Dokumen Pabean', required=False),
                'chk_import' : fields.boolean(string='Import'),
            }
stock_picking_in()



class stock_picking_out(osv.osv_memory):
   
   
    _inherit = 'stock.picking.out'

    _columns = {
                # 'karyawan_id' : fields.many2one('hr.employee', 'User Request',required=False),
                'jenis_dokumen_id' : fields.many2one('gdi.jenis_dokumen_pabean', 'Jenis Dokumen',required=False),
                'nomor_dokumen_pabean' : fields.char(string='Nomor Dokumen Pabean', size=50, required=False),
                'tanggal_dokumen_pabean' : fields.date(string='Tanggal Dokumen Pabean', required=False),
                'chk_import' : fields.boolean(string='Import'),
            }
stock_picking_out()

class stock_picking(osv.osv_memory):
   
   
    _inherit = 'stock.picking'

    _columns = {
                # 'karyawan_id' : fields.many2one('hr.employee', 'User Request',required=False),
                'jenis_dokumen_id' : fields.many2one('gdi.jenis_dokumen_pabean', 'Jenis Dokumen',required=False),
                'nomor_dokumen_pabean' : fields.char(string='Nomor Dokumen Pabean', size=50, required=False),
                'tanggal_dokumen_pabean' : fields.date(string='Tanggal Dokumen Pabean', required=False),
                'chk_import' : fields.boolean(string='Import'),
            }
stock_picking()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

