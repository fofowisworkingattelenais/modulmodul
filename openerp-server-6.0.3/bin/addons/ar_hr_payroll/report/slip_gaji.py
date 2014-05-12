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

import time
import locale
from report import report_sxw

class slip_gaji(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(slip_gaji, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'locale':locale,
        })

report_sxw.report_sxw('report.hr.slip_gaji', 'hr.payslip', 'addons/ar_hr_payroll/report/slip_gaji.rml', parser=slip_gaji, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

