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
    'name': 'AR - Attendance',
    'version': '1.1',
    'author': 'Andhitia Rama',
    'category': 'Andhitia Rama/HR',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    -
    """,
    'author': 'Andhitia Rama',
    'website': 'http://andhitiarama.wordpress.com',
    'images': [],
    'depends': ['ar_product', 'ar_hr_kontrak','hr_attendance'],
    'init_xml': [],
    'update_xml': [ 'security/ir.model.access.csv',
                    'data/data_JenisAbsensi.xml',
                    'data/data_KodeAbsen.xml',
                    'wizard/view_WizardBuatTimesheet.xml',
                    'wizard/view_WizardSesuaikanLiburNasional.xml',
                    'wizard/wizard_konfirmasi_absensi.xml',
                    'view/view_PerusahaanAbsensi.xml',
                    'view/view_Kontrak.xml',
                    'view/view_AttendaceReason.xml',
                    'view/view_Attendance.xml',
                    'view/view_JenisAbsen.xml',
                    'view/view_KodeAbsen.xml',
                    'view/view_KetentuanAbsensi.xml',
                    'view/view_ShiftKerja.xml',
                    'view/view_PolaKerja.xml',
                    'view/view_PerhitunganTimesheet.xml',
                    'view/view_TimesheetKaryawan.xml',
                    'view/view_Absensi.xml',
                    'view/view_LiburNasional.xml',
                    'view/view_PeriodeGaji.xml',
                    'view/view_CutiKerja.xml',
                    'view/view_KetentuanCuti.xml',
                    'view/view_Lembur.xml',
                    'window_action/waction_PerusahaanAbsensi.xml',
                    'window_action/waction_AttendanceReason.xml',
                    'window_action/waction_Attendance.xml',
                    'window_action/waction_JenisAbsen.xml',
                    'window_action/waction_KodeAbsen.xml',
                    'window_action/waction_KetentuanAbsensi.xml',
                    'window_action/waction_ShiftKerja.xml',
                    'window_action/waction_PolaKerja.xml',
                    'window_action/waction_TimesheetKaryawan.xml',
                    'window_action/waction_Absensi.xml',
                    'window_action/waction_LiburNasional.xml',
                    'window_action/waction_CutiKerja.xml',
                    'window_action/waction_KetentuanCuti.xml',
                    'window_action/waction_Lembur.xml',],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
