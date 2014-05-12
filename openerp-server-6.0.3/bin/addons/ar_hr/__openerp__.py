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
    'name': 'AR - Human Resources',
    'version': '1.1',
    'author': 'Andhitia Rama',
    'category': 'Andhitia Rama/HR',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    Modifikasi modul HR
    """,
    'author': 'Andhitia Rama',
    'website': 'http://andhitiarama.wordpress.com',
    'images': [],
    'depends': ['hr', 'ar_identitas'],
    'init_xml': [],
    'update_xml': [ 'security/ir.model.access.csv',
                    'view/view_Departemen.xml',
                    'view/view_Jabatan.xml',
                    'view/view_KategoriKaryawan.xml',
                    'view/view_Karyawan.xml',
                    'view/view_PerusahaanHR.xml',
                    'window_action/waction_Departemen.xml',
                    'window_action/waction_Jabatan.xml',
                    'window_action/waction_KategoriKaryawan.xml',
                    'window_action/waction_Karyawan.xml',
                    'window_action/waction_KaryawanDraft.xml',
                    'window_action/waction_KaryawanProbation.xml',
                    'window_action/waction_KaryawanKontrak.xml',
                    'window_action/waction_KaryawanTetap.xml',
                    'window_action/waction_KaryawanPHK.xml',
                    'window_action/waction_KaryawanPensiunDini.xml',
                    'window_action/waction_KaryawanPensiun.xml',
                    'window_action/waction_PerusahaanHR.xml'],
    'demo_xml': [],
    'test': [],
    'license' : 'Other proprietary',
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
