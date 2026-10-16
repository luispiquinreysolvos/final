import requests

from odoo import api, models
from odoo.exceptions import UserError
class TicketIngestionCron(models.AbstractModel):
    _name = "helpdesk.ticket.ingest.cron"
    _description = "Ticket Ingestion Cron"

    @api.model
    def _cron_ingest_tickets(self):
        outbox_entries = self.env["helpdesk.ticket.ingest.outbox"].search([("state", "=", "draft")])
        client_ai = self.env["helpdesk.ticket.ingest.api.client"]
        for entry in outbox_entries:
            try:
                client_ai.ingest_ticket(entry.ticket_id)
            except (requests.exceptions.RequestException, UserError) as e:
                entry.write({"state": "error", "error_message": str(e)})
            else:
                entry.write({"state": "done", "error_message": False})
