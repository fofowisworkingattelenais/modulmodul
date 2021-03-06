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

{
    'name': 'AR - Base Perusahaan',
    'version': '1.1',
    'author': 'Andhitia Rama',
    'category': 'Andhitia Rama/Base',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    Modul untuk melengkapi isian mengenai legalitas partners
    
    6.0.3, 6.0.4, dan 6.1 compability
    """,
    'author': 'Andhitia Rama',
    'website': 'http://andhitiarama.wordpress.com',
    'images': [],
    'depends': ['ar_base'],
    'init_xml': [],
    'update_xml': [
                    'security/ir.model.access.csv',
                     'view/view_JenisUsahaPerusahaan.xml',
                    'view/view_KepemilikanPerusahaan.xml',
                    'view/view_StatusPerusahaan.xml',
                    'view/view_LegalitasPerusahaan.xml',
                    'window_action/waction_JenisUsahaPerusahaan.xml',
                    'window_action/waction_KepemilikanPerusahaan.xml',
                    'window_action/waction_StatusPerusahaan.xml',],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
