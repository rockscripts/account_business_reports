# -*- coding: utf-8 -*-
from odoo import models, fields, api

class account_move_reversal(models.TransientModel):
    _inherit = 'account.move.reversal'
    
    reason = fields.Selection([['returns', 'Devolucion'],['discounts', 'Descuentos']], string="Discrepancia", default="discounts")

    def _prepare_default_reversal(self, move):
        vector = super(account_move_reversal, self)._prepare_default_reversal(move)
        vector['reason'] = self.reason
        return vector