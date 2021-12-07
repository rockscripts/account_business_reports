# -*- coding: utf-8 -*-
{
    'name': "account_business_reports",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ROCKSCRIPTS",
    'website': "http://www.instagram.com/rockscripts",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
                    'base', 
                    'account', 
                    'sale', 
                    'payment', 
                    'website',
                    'point_of_sale',
                    'categoria',
                    'marcas',
                    'operacion',
                ],
    'data': [
                # 'security/ir.model.access.csv',
                'data/dashboard.xml',
                'views/assets.xml',
                'views/report_dashboard.xml',
                'views/reports_history.xml',
                'views/account_move.xml',
                'views/account_move_reversal.xml',
                #reports
                 #discount
                'views/reports/informe_credit_notes_discount/base.xml',
                'views/reports/informe_credit_notes_discount/informe_credit_notes_discount.xml',
                 #returns
                'views/reports/informe_credit_notes_returns/base.xml',
                'views/reports/informe_credit_notes_returns/informe_credit_notes_returns.xml',
                 #tax sale
                'views/reports/informe_tax_sale/base.xml',
                'views/reports/informe_tax_sale/informe_tax_sale.xml',
                 #tax purchase
                'views/reports/informe_tax_purchase/base.xml',
                'views/reports/informe_tax_purchase/informe_tax_purchase.xml',
                 #expenses
                'views/reports/informe_gastos/base.xml',
                'views/reports/informe_gastos/informe_tax_sale.xml',
                 #net profit
                'views/reports/informe_ganancia_liquida/base.xml',
                'views/reports/informe_ganancia_liquida/informe_ganancia_liquida.xml',
                 #gross profit
                'views/reports/informe_ganancia_bruta/base.xml',
                'views/reports/informe_ganancia_bruta/informe_ganancia_bruta.xml',
                #cash moves
                'views/reports/informe_movimientos_caja/base.xml',
                'views/reports/informe_movimientos_caja/informe_tax_sale.xml',

                'views/menu.xml',
            ],
    'qweb': [
                #'static/src/xml/popups/ganancia_bruta.xml',
                #'static/src/xml/popups/ganancia_liquida.xml',
                #'static/src/xml/popups/gastos.xml',
                #'static/src/xml/popups/impuestos.xml',
                #'static/src/xml/popups/movimientos_caja.xml',
            ],
}