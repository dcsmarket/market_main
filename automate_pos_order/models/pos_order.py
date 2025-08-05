from odoo import models, api, _
from datetime import datetime
import logging
from pytz import timezone

_logger = logging.getLogger(__name__)
from psycopg2 import sql
from odoo.exceptions import UserError

from psycopg2 import OperationalError


class PosOrderInherit(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _run_auto_invoice(self):
        print('Run Auto Invoice')

        date_order = datetime(2024, 7, 10).strftime('%Y-%m-%d')
        batch_size = 50
        max_orders = 350

        query = """
            UPDATE pos_order
            SET partner_id = COALESCE(partner_id, 19670)
            WHERE id IN (
                SELECT id 
                FROM pos_order 
                WHERE state IN ('paid', 'done')
                AND date_order > %s
                AND EXISTS (SELECT 1 FROM pos_order_line WHERE order_id = pos_order.id)
                ORDER BY date_order
                LIMIT %s
            )
            RETURNING id
        """

        total_processed = 0
        while total_processed < max_orders:
            self.env.cr.execute(query, (date_order, min(batch_size, max_orders - total_processed)))
            order_ids = [row[0] for row in self.env.cr.fetchall()]
            if not order_ids:
                break

            self.browse(order_ids).with_context(generate_pdf=False).action_pos_order_invoice()
            self.env.cr.commit()
            total_processed += len(order_ids)

        print(f'Processed {total_processed} orders')


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _run_edi_error_invoice(self):
        _logger.info('Processing EDI invoices.')
        query = """
            SELECT id FROM account_move
            WHERE edi_state = 'to_send' AND state = 'posted'
            ORDER BY date, id
            LIMIT 100
        """
        self.env.cr.execute(query)

        for (move_id,) in self.env.cr.fetchall():
            move = self.browse(move_id)
            if move.edi_blocking_level not in ('error', 'warning'):
                continue

            method = 'action_retry_edi_documents_error' if move.edi_blocking_level == 'error' else 'button_process_edi_web_services'

            try:
                getattr(move, method)()
                self.env.cr.commit()
            except Exception as e:
                _logger.error(f"Failed to process move {move_id}: {str(e)}")
                self.env.cr.rollback()

        _logger.info('Finished processing EDI invoices.')
