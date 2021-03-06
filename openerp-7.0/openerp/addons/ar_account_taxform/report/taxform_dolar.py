import time
import locale

from report import report_sxw

class taxform_dolar(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(taxform_dolar, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'locale' : locale,
        })


report_sxw.report_sxw('report.account.taxform.dolar', 'account.taxform', 'addons/via_account_taxform/report/taxform_dolar.rml', parser=taxform_dolar, header=False)
