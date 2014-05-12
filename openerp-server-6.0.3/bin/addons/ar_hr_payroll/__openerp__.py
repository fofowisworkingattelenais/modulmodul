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
    'name': 'AR - Payroll',
    'version': '1.1',
    'author': 'Andhitia Rama',
    'category': 'Andhitia Rama/HR',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    Modifikasi modul Payroll
    """,
    'author': 'Andhitia Rama',
    'website': 'http://andhitiarama.wordpress.com',
    'images': [],
    'depends': ['hr_payroll', 'ar_base_waktu'],
    'init_xml': [],
    'update_xml': [ 'security/ir.model.access.csv',
                    'data/data_HapusSalaryRule.xml',
                    'data/data_HapusSalaryRuleCategory.xml',
                    'data/data_ContributionRegister.xml',
                    'data/data_SalaryRuleCategory.xml',
                    'data/data_SalaryRule.xml',
                    'data/data_JenisRate.xml',
                    'ar_hr_payroll_report.xml',
                    'wizard/view_WizardImportDataPayroll.xml',
                    'wizard/view_WizardKaryawanBaru.xml',
                    'wizard/view_WizardPerubahanGaji.xml',
                    'wizard/view_WizardPromosiDemosi.xml',
                    'wizard/view_WizardMulaiJadwalPenggajian.xml',
                    'wizard/view_WizardCetakF1b.xml',
                    'wizard/view_WizardCetakF2a.xml',
                    'wizard/view_WizardCetakRiwayatPembayaranGaji.xml',
                    'view/view_PerusahaanPayroll.xml',
                    'view/view_Karyawan.xml',
                    'view/view_Payslip.xml',
                    'view/view_PayslipBatch.xml',
                    'view/view_Kontrak.xml',
                    'view/view_KategoriKetentuanGaji.xml',
                    'view/view_KetentuanGaji.xml',
                    'view/view_StrukturGaji.xml',
                    'view/view_ImportDataPayroll.xml',
                    'view/view_JadwalPenggajian.xml',
                    'view/view_EksekusiPenggajian.xml',
                    'view/view_GajiNonReguler.xml',
                    'view/view_JenisRate.xml',
                    'view/view_RateKaryawan.xml',
                    'view/view_ImportPayslipInput.xml',
                    'view/view_Kontribusi.xml',
                    'window_action/waction_PerusahaanPayroll.xml',
                    'window_action/waction_Payslip.xml',
                    'window_action/waction_PayslipBatch.xml',
                    'window_action/waction_KategoriKetentuanGaji.xml',
                    'window_action/waction_KetentuanGaji.xml',
                    'window_action/waction_StrukturGaji.xml',
                    'window_action/waction_ImportDataPayroll.xml',
                    'window_action/waction_JadwalPenggajian.xml',
                    'window_action/waction_EksekusiPenggajian.xml',
                    'window_action/waction_GajiNonreguler.xml',
                    'window_action/waction_JenisRate.xml',
                    'window_action/waction_RateKaryawan.xml',
                    'window_action/waction_Kontribusi.xml',
                    'window_action/waction_ImportPayslipInput.xml'],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
