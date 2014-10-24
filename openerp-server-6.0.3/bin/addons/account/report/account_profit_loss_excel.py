import time
import pooler
from report import report_sxw
from common_report_header import common_report_header
from tools.translate import _
import xlwt
from report_xls import report_xls
from account.report.account_profit_loss import report_pl_account_horizontal


# XLWT Styles
center_bold = xlwt.easyxf('font:bold True; alignment:horizontal center, vertical center, wrap True; borders:left medium, right medium, top medium, bottom medium;')
center_bold_big = xlwt.easyxf('font:bold True, height 300; alignment:horizontal center, vertical center, wrap True ; borders:left medium, right medium, top medium, bottom medium;')
right_align = xlwt.easyxf('alignment:horizontal right, vertical center, wrap True ; borders:left medium, right medium, top medium, bottom medium;')
right_align2 = xlwt.easyxf('alignment:horizontal right, vertical center, wrap True ;')
left_align = xlwt.easyxf('alignment:horizontal left, vertical center, wrap on ; borders:left medium, right medium, top medium, bottom medium;')
left_bold = xlwt.easyxf('font:bold True; alignment:horizontal left, vertical center, wrap on ; borders:left medium, right medium, top medium, bottom medium;')
left_bold2 = xlwt.easyxf('font:bold True; alignment:horizontal left, vertical center, wrap on ;')
right_bold2 = xlwt.easyxf('font:bold True; alignment:horizontal right, vertical center, wrap on ;')
center_align = xlwt.easyxf('alignment:horizontal center, vertical center, wrap True ; borders:left medium, right medium, top medium, bottom medium;')


class ReportStatus(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(ReportStatus, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,  
	    'xls_export' : 1,         
        })

 
class report_pl_account_excel(report_xls, report_pl_account_horizontal):

    def generate_xls_report(self, cr, uid, ids, parser, data, obj, wb, context=None):
	self.prepare_data(cr, uid, ids, data, context=context)		

	if data['form']['display_type']:
		# Pengaturan cell report
		ws = wb.add_sheet("Profit And Loss")
		ws.col(1).width = 10000
		ws.col(5).width = 10000
		ws.row(2).height = 1000
	
		# Header report
		ws.write_merge(0,0,0,7,"Profit And Loss",center_bold_big)
		ws.write_merge(1,1,0,1,"Chart of Account",center_bold)
		ws.write(1,2,"Fiscal Year",center_bold)
		if data['form']['filter'] == 'filter_date':
			ws.write_merge(1,1,3,4,"Filter By Date",center_bold)
			ws.write(2,3,"Start Date "+self._get_start_date(data),center_align)
			ws.write(2,4,"End Date "+self._get_end_date(data),center_align)
		elif data['form']['filter'] == 'filter_period':	  
			ws.write_merge(1,1,3,4,"Filter By Periods",center_bold)
			ws.write(2,3,"Start Period "+self.get_start_period(data),center_align)
			ws.write(2,4,"End Period "+self.get_end_period(data),center_align)
		else:
			ws.write_merge(1,1,3,4,"Filter By",center_bold)
			ws.write_merge(2,2,3,4,"No Filter",center_align)
		ws.write(1,5,"Display Account",center_bold)
		ws.write_merge(1,1,6,7,"Target Moves",center_bold)

		ws.write_merge(2,2,0,1,self._get_account(data),center_align)
		ws.write(2,2,self._get_fiscalyear(data),center_align)
		ws.write(2,5,self.get_display_account_name(data['form']['display_account']),center_align)
		ws.write_merge(2,2,6,7,self._get_target_move(data),center_align)	

		self.account_pl_horizontal_write(ws)
	else:
		# Pengaturan cell report
		ws = wb.add_sheet("Profit And Loss")
		ws.col(0).width = 7500
		ws.col(4).width = 7500
		ws.col(5).width = 7500
		ws.row(2).height = 1000
	
		# Header report
		ws.write_merge(0,0,0,5,"Profit And Loss",center_bold_big)
		ws.write(1,0,"Chart of Account",center_bold)
		ws.write(1,1,"Fiscal Year",center_bold)
		if data['form']['filter'] == 'filter_date':
			ws.write_merge(1,1,2,3,"Filter By Date",center_bold)
			ws.write(2,2,"Start Date "+self._get_start_date(data),center_align)
			ws.write(2,3,"End Date "+self._get_end_date(data),center_align)
		elif data['form']['filter'] == 'filter_period':	  
			ws.write_merge(1,1,2,3,"Filter By Periods",center_bold)
			ws.write(2,2,"Start Period "+self.get_start_period(data),center_align)
			ws.write(2,3,"End Period "+self.get_end_period(data),center_align)
		else:
			ws.write_merge(1,1,2,3,"Filter By",center_bold)
			ws.write_merge(2,2,2,3,"No Filter",center_align)
		ws.write(1,4,"Display Account",center_bold)
		ws.write(1,5,"Target Moves",center_bold)

		ws.write(2,0,self._get_account(data),center_align)
		ws.write(2,1,self._get_fiscalyear(data),center_align)
		ws.write(2,4,self.get_display_account_name(data['form']['display_account']),center_align)
		ws.write(2,5,self._get_target_move(data),center_align)

		self.account_pl_write(ws)

	pass

    def prepare_data(self, cr, uid, ids, data, context=None):
	self.cr = cr
	self.uid = uid
	self.ids = ids
	self.cursor = cr
	self.pool = pooler.get_pool(self.cr.dbname)
	self.context = context
	self.result_sum_dr = 0.0
        self.result_sum_cr = 0.0
        self.res_pl = {}
        self.result = {}
        self.result_temp = []
	self.isi_laporan = self.get_data(data)

    def get_display_account_name(self, display_account):
	if display_account == "bal_all":
		return "All"
	elif display_account == "bal_movement":
		return "With movements"
	else:
		return "With balance is not equal to 0"

    def account_pl_horizontal_write(self, ws):
	ws.write(4,0,"Code",left_bold)
	ws.write(4,1,"Particular",left_bold)
	ws.write_merge(4,4,2,3,"Balance",left_bold)
	ws.write(4,4,"Code",left_bold)
	ws.write(4,5,"Particular",left_bold)
	ws.write_merge(4,4,6,7,"Balance",left_bold)

	i = 5
	for result in self.result_temp:
		ws.write(i,0,result['code'])
		ws.write(i,1,result['name'])
		ws.write_merge(i,i,2,3,"Rp "+format(result['balance'],',.2f'),right_align2)
		ws.write(i,4,result['code1'])
		ws.write(i,5,result['name1'])
		if result['code1']:
			ws.write_merge(i,i,6,7,"Rp "+format(abs(result['balance1']),',.2f'),right_align2)
		else:
			ws.write_merge(i,i,6,7,"")
		i += 1

	ws.write(i,4,"Net Loss",left_bold2)
	ws.write_merge(i,i,6,7,"Rp "+format(abs(self.final_result()['balance']),',.2f'),right_bold2)
	i += 1
	ws.write(i,0,"Total:",left_bold2)
	ws.write_merge(i,i,2,3,"Rp "+format(self.sum_dr(),',.2f'),right_bold2)
	ws.write(i,4,"Total:",left_bold2)
	ws.write_merge(i,i,6,7,"Rp "+format(self.sum_cr(),',.2f'),right_bold2)

    def account_pl_write(self, ws):
	ws.write(4,0,"Code",left_bold)
	ws.write_merge(4,4,1,4,"Expenses",left_bold)
	ws.write(4,5,"Balance",left_bold)

	i = 5
	for result in self.result.get('expense', []):
		ws.write(i,0,result['code'])
		ws.write_merge(i,i,1,4,result['name'])
		ws.write(i,5,"Rp "+format(result['balance'],',.2f'),right_align2)
		i += 1

	ws.write(i,0,"Total",left_bold2)
	ws.write(i,5,"Rp "+format(abs(self.sum_dr()),',.2f'),right_bold2)

	i += 2
	ws.write(i,0,"Code",left_bold)
	ws.write_merge(i,i,1,4,"Incomes",left_bold)
	ws.write(i,5,"Balance",left_bold)

	i += 1
	for result in self.result.get('income', []):
		ws.write(i,0,result['code'])
		ws.write_merge(i,i,1,4,result['name'])
		ws.write(i,5,"Rp "+format(result['balance'],',.2f'),right_align2)
		i += 1


	ws.write(i,1,"Net Loss",left_bold2)
	ws.write(i,5,"Rp "+format(abs(self.final_result()['balance']),',.2f'),right_bold2)
	i += 1
	ws.write(i,0,"Total:",left_bold2)
	ws.write(i,5,"Rp "+format(self.sum_cr(),',.2f'),right_bold2)
	


report_pl_account_excel('report.pl.account.excel', 'account.account', 'addons/account/report/account_profit_loss_excel.mako', parser=ReportStatus, header=False)
