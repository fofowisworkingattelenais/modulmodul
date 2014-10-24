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
    'name': 'AR - Base',
    'version': '1.1',
    'author': 'Andhitia Rama',
    'category': 'Andhitia Rama/Base',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    Modul warna
    """,
    'author': 'Andhitia Rama',
    'website': 'http://andhitiarama.wordpress.com',
    'images': [],
    'depends': ['base'],
    'init_xml': [],
    'update_xml': [ 'view/view_Negara.xml',
                    'view/view_Propinsi.xml',
                    'view/view_TitelMitraBisnis.xml',
                    'view/view_KategoriMitraBisnis.xml',
                    'window_action/waction_Negara.xml',
                    'window_action/waction_Propinsi.xml',
                    'window_action/waction_TitelMitraBisnis.xml',
                    'window_action/waction_KategoriMitraBisnis.xml',
                    'window_action/waction_TitelIndividu.xml',],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
