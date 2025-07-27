# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PhysicalInventoryAdjustment(models.Model):
    _name = 'physical.inventory.adjustment'
    _description = 'Physical Inventory Adjustment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: 'New'
    )

    location_id = fields.Many2one(
        'stock.location',
        string='Location',
        required=True,
        tracking=True,
        domain=[('usage', '=', 'internal')]
    )

    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        required=True,
        tracking=True
    )

    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
        ('reject', 'Reject'),
    ], string='Status', default='draft', tracking=True)

    location_barcode = fields.Char(related='location_id.barcode', string='Location Barcode')
    created_by = fields.Many2one('res.users', string='Created By')
    approved_by = fields.Many2one('res.users', string='Approved By')

    line_ids = fields.One2many(
        'physical.inventory.adjustment.line',
        'adjustment_id',
        string='Adjustment Lines'
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('physical.inventory.adjustment') or 'New'
        vals['created_by'] = self.env.user.id
        return super(PhysicalInventoryAdjustment, self).create(vals)

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', 'New') == 'New':
    #         vals['name'] = self.env['ir.sequence'].next_by_code('physical.inventory.adjustment') or 'New'
    #     vals['created_by'] = self.env.user.id
    #     record = super(PhysicalInventoryAdjustment, self).create(vals)
    #     if record.line_ids:
    #         for line in record.line_ids:
    #             line._compute_temp_barcode()
    #     return record
    #
    # def write(self, vals):
    #     result = super(PhysicalInventoryAdjustment, self).write(vals)
    #     if 'line_ids' in vals:
    #         for line in self.line_ids:
    #             line._compute_temp_barcode()
    #     return result

    # @api.constrains('location_id', 'status')
    # def _check_unique_active_location(self):
    #     for record in self:
    #         if record.status not in ['done', 'cancel']:
    #             duplicate = self.search([
    #                 ('location_id', '=', record.location_id.id),
    #                 ('status', 'not in', ['done', 'cancel']),
    #                 ('id', '!=', record.id)
    #             ], limit=1)
    #             if duplicate:
    #                 raise ValidationError(_(
    #                     "A record for this Location is already active in the '%s' state. "
    #                     "Please complete or cancel the existing record before creating a new one."
    #                 ) % duplicate.status)
    #
    # _sql_constraints = [
    #     ('unique_active_location',
    #      'UNIQUE(location_id, status)',
    #      'Only one active record per location is allowed.')
    # ]

    def unlink(self):
        for record in self:
            if record.status != 'draft':
                raise ValidationError("You can only delete records in the Draft state.")
        return super(PhysicalInventoryAdjustment, self).unlink()

    def action_approve(self):
        self.status = 'approved'

    def action_cancel(self):
        for rec in self:
            rec.status = 'cancel'

    def action_reject(self):
        for rec in self:
            rec.status = 'reject'

    def action_done(self):
        self.ensure_one()
        StockQuant = self.env['stock.quant']

        product_quantities = {}

        for line in self.line_ids:
            product_id = line.product_id.id
            if product_id not in product_quantities:
                product_quantities[product_id] = 0
            product_quantities[product_id] += line.qty

        for product_id, total_qty in product_quantities.items():
            quant = StockQuant.search([
                ('location_id', '=', self.location_id.id),
                ('product_id', '=', product_id)
            ], limit=1)

            if quant:
                quant.write({
                    'inventory_quantity': total_qty,
                    'inventory_date': fields.Date.today(),
                    'user_id': self.env.user.id,
                    'inventory_quantity_set': True  # Add this line to make Apply button visible
                })
            else:
                new_quant = StockQuant.create({
                    'product_id': product_id,
                    'location_id': self.location_id.id,
                    'inventory_quantity': total_qty,
                    'inventory_date': fields.Date.today(),
                    'user_id': self.env.user.id,
                    'inventory_quantity_set': True  # Add this line to make Apply button visible
                })

        self.status = 'done'
        self.approved_by = self.env.user.id

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Adjustment Added Successfully'),
                'sticky': False,
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def copy(self, default=None):
        default = default or {}
        # Set the state to 'draft' for the new copy
        default['status'] = 'draft'

        # Call the original copy method to duplicate the main record
        new_record = super(PhysicalInventoryAdjustment, self).copy(default)

        # Duplicate the related lines
        for line in self.line_ids:
            line.copy({'adjustment_id': new_record.id})

        return new_record


class PhysicalInventoryAdjustmentLine(models.Model):
    _name = 'physical.inventory.adjustment.line'
    _description = 'Physical Inventory Adjustment Line'

    adjustment_id = fields.Many2one(
        'physical.inventory.adjustment',
        string='Inventory Adjustment',
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )

    description = fields.Char(
        string='Description',
        related='product_id.name',
        store=True
    )

    qty = fields.Float(
        string='QTY',
        required=True
    )

    qty_on_hand = fields.Float(
        string='QTY On Hand',
        compute='_compute_qty_on_hand',
        store=True
    )

    uom_id = fields.Many2one(
        'uom.uom',
        related='product_id.uom_id',
        string='UOM',
    )

    repetitive_count = fields.Integer(
        string='Repetitive',
        compute='_compute_repetitive_count',
        store=True
    )

    reference = fields.Char(string='Reference', related='product_id.default_code')
    # barcode = fields.Char(string='Barcode', related='product_id.barcode')
    barcode = fields.Char(string='Barcode')

    temp_barcode = fields.Char(string='Temp Barcode', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.barcode = self.product_id.barcode
        else:
            self.barcode = False

    @api.onchange('barcode')
    def _onchange_barcode(self):
        if self.barcode:
            product = self.env['product.product'].sudo().search([('barcode', '=', self.barcode.strip())], limit=1)
            if product:
                self.product_id = product
            else:
                return {'warning': {
                    'title': _("Warning"),
                    'message': _("The entered barcode does not match any product.")
                }}
        else:
            self.product_id = False

    @api.constrains('qty')
    def _check_qty(self):
        for record in self:
            if record.qty <= 0:
                raise ValidationError(_("Add Quantity and Quantity must be greater than zero."))

    @api.depends('product_id', 'adjustment_id.line_ids.product_id')
    def _compute_repetitive_count(self):
        for line in self:
            if line.adjustment_id:
                line.repetitive_count = sum(
                    1 for rec in line.adjustment_id.line_ids if rec.product_id == line.product_id
                )

    @api.depends('product_id', 'adjustment_id.location_id')
    def _compute_qty_on_hand(self):
        for record in self:
            adjustment = self.env['stock.quant'].sudo().search(
                [('location_id', '=', record.adjustment_id.location_id.id), ('product_id', '=', record.product_id.id)],
                limit=1)
            record.qty_on_hand = adjustment.quantity if adjustment else 0

    def unlink(self):
        for record in self:
            if record.adjustment_id and record.adjustment_id.status != 'draft':
                raise ValidationError(_("You can only delete records in the Draft state."))
        return super(PhysicalInventoryAdjustmentLine, self).unlink()

