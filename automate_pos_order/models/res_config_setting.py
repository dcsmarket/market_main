# from odoo import fields, models
#
#
# class PosConfig(models.Model):
#     _inherit = 'pos.config'
#
#     balance_control = fields.Boolean(string='For Cash', default=False)
#     for_atm = fields.Boolean(string='For ATM', default=False)
#     for_others = fields.Boolean(string='For Others', default=False)
#
#
# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     balance_control = fields.Boolean(
#         related='pos_config_id.balance_control',
#         readonly=False,
#         help="Hide Expected, Counted, Differences columns and Daily Sales button"
#     )
#
#     for_atm = fields.Boolean(
#         related='pos_config_id.for_atm',
#         readonly=False,
#         help="Hide Expected, Counted, Differences columns and Daily Sales button for ATM payments"
#     )
#
#     for_others = fields.Boolean(
#         related='pos_config_id.for_others',
#         readonly=False,
#         help="Hide Expected, Counted, Differences columns and Daily Sales button for other payment methods"
#     )