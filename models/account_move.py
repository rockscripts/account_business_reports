# -*- coding: utf-8 -*-
from odoo import models, fields, api

class account_move(models.Model):
    _inherit = 'account.move'
    
    reason = fields.Selection([['returns', 'Devolucion'],['discounts', 'Descuentos']], string="Discrepancia", default="discounts")
    x_termino = fields.Selection([('debit','Débito'),('credit','Crédito')], string="Tipo de pago", default="debit")