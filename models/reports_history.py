# -*- coding: utf-8 -*-
from odoo import models, fields, api

class reports_history(models.Model):
    _name = 'reports.history'
    _description = 'Historial de Reportes'
    
    name = fields.Char(string="Nombre")
    seller = fields.Many2one('res.users', string="Vendedor", ondelete='cascade', index=True)
    partner = fields.Many2one('res.partner', string="Cliente", ondelete='cascade', index=True)
    date_start = fields.Datetime(string="Fecha inicial", select=True, default=lambda self: fields.datetime.now())
    date_ends = fields.Datetime(string="Fecha final", select=True, default=lambda self: fields.datetime.now())
    product_category = fields.Many2one('product.category', string="Categoria de productos", ondelete='cascade', index=True)
    product_brand = fields.Many2one('ej.marcas', string="Marca", ondelete='cascade', index=True)
    invoice_site = fields.Char(string="Sito de facturación")
    payment_type = fields.Selection([('debit','Débito'),('credit','Crédito')], string="Tipo de pago", default="debit")
    operation_executed = fields.Many2one('ej.operacion', string="Operación lanzada", ondelete='cascade', index=True)
    category_executed = fields.Many2one('ej.categoria', string="Categoria lanzada", ondelete='cascade', index=True)
    #pos_config = fields.Many2one('pos.config', string="POS", ondelete='cascade', index=True)
    report_type = fields.Selection([
                                        ('informe_ganancia_liquida', 'Informe ganancia liquida'),
                                        ('informe_ganancia_bruta', 'Informe ganancia bruta'),
                                        ('informe_gastos', 'Informe gastos'),
                                        ('informe_movimientos_caja', 'Informe movimientos caja'),
                                        ('informe_credit_notes_returns', 'Informe Nota Crédito - Devoluciones'),
                                        ('informe_credit_notes_discounts', 'Informe Nota Crédito - Descuentos'),
                                        ('informe_tax_purchase', 'Informe Impuestos en Compras'),
                                        ('informe_tax_sale', 'Informe Impuestos en Ventas'),
                                    ],
                                    default='informe_ganancia_liquida',
                                    required=True,
                                    string='Tipo reporte')
    
    # informe_credit_notes_discounts
    total_discount = fields.Float(string="Descuentos")
    # informe_credit_notes_returns
    total_returns = fields.Float(string="Devoluciones")

    pdf_report_name = fields.Char(string="Archivo")
    pdf_report = fields.Binary(string="PDF")

    date_generated = fields.Datetime(string="Fecha", select=True, default=lambda self: fields.datetime.now())

    def search_in_field(model, keyword, in_field):
        matched_results = self.env[model].sudo().search([
                                                            (in_field,'=',keyword),
                                                        ])
        return matched_results 