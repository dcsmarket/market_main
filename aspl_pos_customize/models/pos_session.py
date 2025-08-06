# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
from odoo import models, fields


class PosOrder(models.Model):
    _inherit = "pos.order"

    def action_update_pos_payment(self):
        return {
            'name': 'Update POS Payment',
            'type': 'ir.actions.act_window',
            'res_model': 'update.pos.payment.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_pos_payment_ids': [(0, 0, {
                    'pos_payment_id': line.id,
                    'payment_method_id': line.payment_method_id.id,
                    'amount': line.amount
                }) for line in self.payment_ids]}
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: