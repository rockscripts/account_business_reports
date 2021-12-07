# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class business_reports(models.Model):
    _name = 'business.reports'
    _description = 'Reportes empresariales'
    
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

    def generate_financial_report(self):
        if(self.report_type == str('informe_credit_notes_discounts')):
            return self.env.ref('account_business_reports.informe_tax_sale_pdf').report_action(self)

    def get_tax(self, _id):
        tax = self.env['account.tax'].sudo().browse(int(_id))
        return tax

    def get_tax_total(self, taxes, _id):
        _logger.warning('get_tax_total')
        _logger.warning(_id)
        _logger.warning(taxes)
        return taxes[str(_id)]

    def get_taxes_keys(self):
        total_taxes = {}
        taxes = self.env['account.tax'].search([
                                                    ['active','=',True],
                                                    ['type_tax_use','=','sale'],
                                                ])
        if(taxes):
            for tax in taxes:
                total_taxes[str(tax.id)] = float()
        return total_taxes

    def get_sale_taxes(self):
        # filter fields: date_start, date_ends
        total_taxes = self.get_taxes_keys()
        _logger.warning("total_taxes get_sale_taxes")
        _logger.warning(total_taxes)
        journals = self.env['account.journal'].sudo().search([
                                                                ['refund_sequence','=', False],
                                                                ['type','=', 'sale']
                                                            ])
        _logger.warning("journals get_credit_note_total_discounts")
        _logger.warning(journals)
        if(journals):
            for journal in journals:                
                moves = self.env['account.move'].sudo().search([
                                                                    ['journal_id','=', int(journal.id)],
                                                                    ['state','=', str('posted')],
                                                                ])
                _logger.warning("moves get_credit_note_total_discounts")
                _logger.warning(moves)
                if(moves):
                    for move in moves:
                        if(move.invoice_line_ids):
                            _logger.warning("move.invoice_line_ids get_sale_taxes")
                            _logger.warning(move.invoice_line_ids)
                            for line in move.invoice_line_ids:
                                    if(line.tax_ids): 
                                        for tax in line.tax_ids:
                                            if(str(tax.price_include) == True):
                                                if(str(tax.amount_type) == "percent"):
                                                    line_tax_rate = float(tax.amount) / 100
                                                    line_tax_amount = float(line.price_total)-((float(line.price_total)/(1+float(line_tax_rate))*float(line_tax_rate)))
                                                    total_taxes[str(tax.id)] = float(line_tax_amount)
                                                else:
                                                    raise Warning("Solo reporta impuestos basados en porcentaje.")
                                            else:
                                                raise Warning("Solo reporta impuestos incluidos en el precio.")
        self.create_report_history({
                                        #'total_sale_taxes':total_taxes, # ¿crear modelo?
                                        'pdf_report_name':self.get_report_name(),
                                    })
        _logger.warning("total_taxes get_sale_taxes")
        _logger.warning(total_taxes)
        return total_taxes

    def get_purchase_taxes(self):
        # filter fields: date_start, date_ends
        total_taxes = self.get_taxes_keys()
        _logger.warning("total_taxes get_purchase_taxes")
        _logger.warning(total_taxes)
        journals = self.env['account.journal'].sudo().search([
                                                                ['refund_sequence','=', False],
                                                                ['type','=', 'purchase']
                                                            ])
        _logger.warning("journals get_purchase_taxes")
        _logger.warning(journals)
        if(journals):
            for journal in journals:                
                moves = self.env['account.move'].sudo().search([
                                                                    ['journal_id','=', int(journal.id)],
                                                                    ['state','=', str('posted')],
                                                                ])
                _logger.warning("moves get_purchase_taxes")
                _logger.warning(moves)
                if(moves):
                    for move in moves:
                        if(move.invoice_line_ids):
                            _logger.warning("move.invoice_line_ids get_purchase_taxes")
                            _logger.warning(move.invoice_line_ids)
                            for line in move.invoice_line_ids:
                                    if(line.tax_ids): 
                                        for tax in line.tax_ids:
                                            if(str(tax.price_include) == True):
                                                if(str(tax.amount_type) == "percent"):
                                                    line_tax_rate = float(tax.amount) / 100
                                                    line_tax_amount = float(line.price_total)-((float(line.price_total)/(1+float(line_tax_rate))*float(line_tax_rate)))
                                                    total_taxes[str(tax.id)] = float(line_tax_amount)
                                                else:
                                                    raise Warning("Solo reporta impuestos basados en porcentaje.")
                                            else:
                                                raise Warning("Solo reporta impuestos incluidos en el precio.")
        self.create_report_history({
                                        #'total_sale_taxes':total_taxes, # ¿crear modelo?
                                        'pdf_report_name':self.get_report_name(),
                                    })
        _logger.warning("total_taxes get_purchase_taxes")
        _logger.warning(total_taxes)
        return total_taxes

    def get_credit_note_total_discounts(self):
        # filter fields: date_start, date_ends
        total_discount = float(0)
        journals = self.env['account.journal'].sudo().search([['refund_sequence','=', True]])
        #_logger.warning("journals get_credit_note_total_discounts")
        #_logger.warning(journals)
        if(journals):
            for journal in journals:
                
                moves = self.env['account.move'].sudo().search([
                                                                    ['journal_id','=', int(journal.id)], 
                                                                    ['reason','=', str('discounts')],
                                                                    ['state','=', str('posted')],
                                                                ])
                #_logger.warning("moves get_credit_note_total_discounts")
                #_logger.warning(moves)
                if(moves):
                    for move in moves:
                        if(move.invoice_line_ids):
                            #_logger.warning("move.invoice_line_ids get_credit_note_total_discounts")
                            #_logger.warning(move.invoice_line_ids)
                            for line in move.invoice_line_ids:
                                    if(float(line.discount) > 0): 
                                        _logger.warning("**********************")
                                        _logger.warning("journal.name: "+str(journal.name))
                                        _logger.warning("move.name: "+str(move.name))
                                        _logger.warning("move.id: "+str(move.id))
                                        _logger.warning("line.product_id.id: "+str(line.product_id.id))
                                        _logger.warning("line.name: "+str(line.name))
                                        total_discount_line = (float(line.discount) / 100) * (float(line.price_total))
                                        total_discount += float(total_discount_line)
                                        _logger.warning("total.discount: "+str(total_discount))
                                        _logger.warning("**********************")
        self.create_report_history({
                                        'total_discount':total_discount,
                                        'pdf_report_name':self.get_report_name(),
                                    })
        return total_discount
    
    def get_credit_note_total_returns(self):
        # filter fields: date_start, date_ends
        total_returns = float(0)
        journals = self.env['account.journal'].sudo().search([['refund_sequence','=', True]])
        _logger.warning("journals get_credit_note_total_returnss")
        _logger.warning(journals)
        if(journals):
            for journal in journals:
                
                moves = self.env['account.move'].sudo().search([
                                                                    ['journal_id','=', int(journal.id)], 
                                                                    ['reason','=', str('returns')],
                                                                    ['state','=', str('posted')],
                                                                ])
                _logger.warning("moves get_credit_note_total_returnss")
                _logger.warning(moves)
                if(moves):
                    for move in moves:
                        if(move.invoice_line_ids):
                            #_logger.warning("move.invoice_line_ids get_credit_note_total_returnss")
                            #_logger.warning(move.invoice_line_ids)
                            for line in move.invoice_line_ids:
                                    if(float(line.price_total) > 0):
                                        _logger.warning("**********************")
                                        _logger.warning("journal.name: "+str(journal.name))
                                        _logger.warning("move.name: "+str(move.name))
                                        _logger.warning("move.id: "+str(move.id))
                                        _logger.warning("line.product_id.id: "+str(line.product_id.id))
                                        _logger.warning("line.name: "+str(line.name))
                                        total_returns += float(line.price_total)
                                        _logger.warning("total.amount.returns: "+str(total_returns))
                                        _logger.warning("**********************")
        self.create_report_history({'total_returns':total_returns})
        return total_returns    
    
    def create_report_history(self, extra_values=None):
        record =   {
                        'name':self.name,
                        'seller':self.seller,
                        'partner':self.partner,
                        'date_start':self.date_start,
                        'date_ends':self.date_ends,
                        'product_category':self.product_category,
                        'product_brand':self.product_brand,
                        'payment_type':self.payment_type,
                        'operation_executed':self.operation_executed,
                        'category_executed':self.category_executed,
                        #'pos_config':self.pos_config,
                        'report_type':self.report_type,
                    }

        if(extra_values):
            if('total_discount' in extra_values):
                record['total_discount'] = extra_values['total_discount']
            if('total_returns' in extra_values):
                record['total_returns'] = extra_values['total_returns']
        self.env['reports.history'].sudo().create(record)
    
    def get_report_name(self):
        return str(self.name) + str('-') + str(fields.datetime.now())