# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#
#    Copyright (C) 2014-2015 PT.Telenais Aset Tangguh
#    Author Faris Bassam
##
##############################################################################
{
    "name": "Show Purchase Requisition Lines menu entry",
    "version": "1.01",
    "depends": [ "purchase_requisition" ],
    "author": "Faris Bassam",
    "category": "Sales & Purchases",
    "description": """Show Purchase Requisition Lines menu entry
    """,
    "init_xml": [],
    'update_xml': ["view/purchase_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}