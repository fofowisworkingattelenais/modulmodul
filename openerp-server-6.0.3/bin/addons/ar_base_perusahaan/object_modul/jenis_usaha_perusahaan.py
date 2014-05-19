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


class jenis_usaha_perusahaan(osv.osv):
    _name = "base.jenis_usaha_perusahaan"
    _description = "Jenis Usaha Perusahaan"

    _columns = {
                'name' : fields.char(string='Jenis Usaha Perusahaan', size=100, required=True),
                'kode' : fields.char(string='Kode', size=30),
                'keterangan' : fields.text(string='Keterangan'),
                'active' : fields.boolean(string='Aktif'),
            }
                     
jenis_usaha_perusahaan()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
