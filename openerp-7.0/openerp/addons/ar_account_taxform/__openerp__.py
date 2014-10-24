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
    "name" : "AR - Account Taxform",
    "version" : "1.0",
    "author" : "Andhitia Rama",
    "description" : """
	Modifikasi modul Account Taxform
	""",
    'website': 'http://andhitiarama.wordpress.com',
    "license" : "GPL-3",
    "category" : "Generic Modules/Accounting",
    "depends" : ["account","ar_base_perusahaan"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [ 'security/ir.model.access.csv',
    				 'data/data_Sequence.xml',
					 'wizard/wizard_create_taxform.xml',
    				 'wizard/wizard_select_taxform_sequence.xml',
    				 'wizard/wizard_create_taxform_sequence.xml',
    				 'wizard/wizard_cancel_taxform_sequence.xml',
    				 'ar_account_taxform_report.xml',
				 	 'view/view_Company.xml',
					 'view/view_AccountTaxformLine.xml',
					 'view/view_AccountTaxform.xml',
					 'view/view_AccountTaxformCategory.xml',
					 'view/view_AccountTaxformSequence.xml',
					 'ar_account_invoice_view.xml',
					 'window_action/waction_AccountTaxform.xml',
					 'window_action/waction_AccountTaxformCategory.xml',
					 'menu/menu_Account.xml',
					],
    "active":False,
    "installable":True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
