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
    'name': 'AR - Rekrutmen',
    'version': '1.1',
    'author': 'Andhitia Rama',
    'category': 'Andhitia Rama/HR',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    Rekrutmen
    """,
    'author': 'Andhitia Rama',
    'website': 'http://andhitiarama.wordpress.com',
    'images': [],
    'depends': ['ar_hr', 'ar_identitas', 'ar_pendidikan'],
    'init_xml': [],
    'update_xml': [ 'security/ir.model.access.csv',
                    'workflow/workflow_Lowongan.xml',
                    'workflow/workflow_Lamaran.xml',
                    'workflow/workflow_ProsesLamaran.xml',
                    'view/view_PerusahaanRekrutmen.xml',
                    'view/view_Seleksi.xml',
                    'view/view_ProsesSeleksi.xml',
                    'view/view_Pelamar.xml',
                    'view/view_LowonganAdmin.xml',
                    'view/view_LamaranAdmin.xml',
                    'window_action/waction_PerusahaanRekrutmen.xml',
                    'window_action/waction_Seleksi.xml',
                    'window_action/waction_ProsesSeleksi.xml',
                    'window_action/waction_Pelamar.xml',
                    'window_action/waction_PelamarPelamar.xml',
                    'window_action/waction_PelamarDiterima.xml',
                    'window_action/waction_LowonganAdmin.xml',
                    'window_action/waction_LowonganRequest.xml',
                    'window_action/waction_LowonganDisetujui.xml',
                    'window_action/waction_LowonganSeleksi.xml',
                    'window_action/waction_LowonganSelesai.xml',
                    'window_action/waction_LowonganBatal.xml',
                    'window_action/waction_LamaranAdmin.xml',
                    'window_action/waction_LamaranDraft.xml',
                    'window_action/waction_LamaranSeleksi.xml',
                    'window_action/waction_LamaranApproval.xml',
                    'window_action/waction_LamaranLimitGaji.xml',
                    'window_action/waction_LamaranNegoGaji.xml',
                    'window_action/waction_LamaranDiterima.xml',
                    'window_action/waction_LamaranTidakDiterima.xml',
                    'window_action/waction_LamaranBatal.xml',],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
