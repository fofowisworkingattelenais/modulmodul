import time
import netsvc
from osv import fields,osv

class purchase_order_line(osv.osv):

    _inherit = 'purchase.order.line'
    _columns = {
        'requisition_id': fields.char('Source Documents', size=62, help="Reference of the document that generated this purchase order request."),
    }

purchase_order_line()