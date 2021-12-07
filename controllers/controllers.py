# -*- coding: utf-8 -*-
# from odoo import http


# class AccountBusinessReports(http.Controller):
#     @http.route('/account_business_reports/account_business_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_business_reports/account_business_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_business_reports.listing', {
#             'root': '/account_business_reports/account_business_reports',
#             'objects': http.request.env['account_business_reports.account_business_reports'].search([]),
#         })

#     @http.route('/account_business_reports/account_business_reports/objects/<model("account_business_reports.account_business_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_business_reports.object', {
#             'object': obj
#         })
