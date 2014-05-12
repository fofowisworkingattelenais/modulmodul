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
    'name': 'AR - Kontrak',
    'version': '1.1',
    'author': 'Andhitia Rama',
    'category': 'Andhitia Rama/HR',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    Kontrak
    """,
    'author': 'Andhitia Rama',
    'website': 'http://andhitiarama.wordpress.com',
    'images': [],
    'depends': ['ar_hr','hr_contract'],
    'init_xml': [],
    'update_xml': [ 'security/ir.model.access.csv',
                    'data/data_HapusData.xml',
                    'data/data_TipeKontrak.xml',
                    'workflow/workflow_Kontrak.xml',
                    'wizard/view_WizardKaryawanBaru.xml',
                    'wizard/view_WizardMutasi.xml',
                    'wizard/view_WizardPerubahanGaji.xml',
                    'wizard/view_WizardPensiun.xml',
                    'wizard/view_WizardPromosiDemosi.xml',
                    'wizard/view_WizardPHK.xml',
                    'wizard/wizard_validasi_history.xml',
                    'view/view_TipeKontrak.xml',
                    'view/view_Kontrak.xml',
                    'view/view_Karyawan.xml',
                    'view/view_PerusahaanKontrak.xml',
                    'view/view_TipeHistory.xml',
                    'view/view_PeriodeGaji.xml',
                    'window_action/waction_TipeKontrak.xml',
                    'window_action/waction_Kontrak.xml',
                    'window_action/waction_KontrakDraft.xml',
                    'window_action/waction_KontrakDisetujui.xml',
                    'window_action/waction_KontrakValid.xml',
                    'window_action/waction_KontrakSelesai.xml',
                    'window_action/waction_KontrakBatal.xml',
                    'window_action/waction_TipeHistory.xml',
                    'window_action/waction_PeriodeGaji.xml',],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
