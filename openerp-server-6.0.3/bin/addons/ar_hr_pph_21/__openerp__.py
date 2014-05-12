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
    'name': 'AR - PPH 21',
    'version': '1.1',
    'author': 'Andhitia Rama',
    'category': 'Andhitia Rama/HR',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    PPH21
    """,
    'author': 'Andhitia Rama',
    'website': 'http://andhitiarama.wordpress.com',
    'images': [],
    'depends': ['ar_hr_kontrak', 'ar_hr_keluarga_karyawan', 'ar_hr_payroll', 'ar_pajak'],
    'init_xml': [],
    'update_xml': [ 'security/ir.model.access.csv',
                    'data/data_SalaryRuleCategory.xml',
                    'data/data_SalaryRulePPH21.xml',
                    'data/data_KategoriPTKP.xml',
                    'wizard/view_WizardKaryawanBaru.xml',
                    'wizard/view_WizardCetak1721Induk.xml',
                    'view/view_PerusahaanPayroll.xml',
                    'view/view_KetentuanGaji.xml',
                    'view/view_StrukturGaji.xml',
                    'view/view_Karyawan.xml',
                    'view/view_KategoriPTKP.xml',
                    'view/view_Payslip.xml',
                    'view/view_StatusKaryawanPajak.xml',
                    'view/view_TahunPajak.xml',
                    'view/view_Kontrak.xml',
                    'view/view_Form1721Induk.xml',
                    'view/view_Form1721A1.xml',
                    'view/view_Form1721A.xml',
                    'view/view_Form1721II.xml',
                    'window_action/waction_KetentuanGaji.xml',
                    'window_action/waction_KategoriPTKP.xml',
                    'window_action/waction_StatusKaryawanPajak.xml',
                    'window_action/waction_Form1721Induk.xml',
                    'window_action/waction_Form1721A1.xml',
                    'window_action/waction_Form1721A.xml',
                    'window_action/waction_Form1721II.xml'],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
