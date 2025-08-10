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

from odoo import api, fields, models, tools, _


class UpdatePOSPayment(models.TransientModel):
    _name = 'update.pos.payment.wizard'
    _description = "Update POS Payment Wizard"

    wizard_id = fields.Many2one('update.pos.payment.wizard')
    pos_payment_ids = fields.One2many('update.pos.payment.wizard', 'wizard_id', string="POS Session(s)")
    payment_method_id = fields.Many2one('pos.payment.method', "Payment Method", readonly=1)
    pos_payment_id = fields.Many2one("pos.payment", "Pos Payment")
    amount = fields.Float("Amount")

    def on_confirm(self):
        for each in self.pos_payment_ids:
            if each.pos_payment_id:
                each.pos_payment_id.sudo().write({'amount': each.amount})
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: