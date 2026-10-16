from odoo import _, api, models
from odoo.exceptions import UserError
import requests
class HelpdeskTicketIngestApiClient(models.AbstractModel):
    _name = 'helpdesk.ticket.ingest.api.client'
    _description = 'Helpdesk Ticket Ingest API Client'

    @api.model
    def _get_ingest_api_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('helpdesk_ai_ticket_suggestion.ingest_api_url')

    @api.model
    def _prepare_ingest_payload(self, ticket):
        """Build the JSON body expected by IngestTicketHttpRequest from a helpdesk.ticket."""
        return {
            'id': ticket.id,
            'database': self.env.cr.dbname,
            'company_id': ticket.company_id.id,
            'number': ticket.number or None,
            'name': ticket.name,
            'description': ticket.description or '',
            'category': ticket.category_id.name or None,
            'partner_email': ticket.partner_email or None,
            'tags': ticket.tag_ids.mapped('name'),
            'priority': ticket.priority,
            'team_id': ticket.team_id.id or None,
            'stage': ticket.stage_id.name or None,
            'closed': ticket.closed,
            'active': ticket.active,
            'write_date': ticket.write_date.isoformat(),
        }

    @api.model
    def ingest_ticket(self, ticket):
        """Send one helpdesk.ticket to the ingest endpoint; raises on failure."""
        url = self._get_ingest_api_url()
        if not url:
            raise UserError(_("Ingest API URL not configured. Please configure it in the settings."))
        payload = self._prepare_ingest_payload(ticket)
        try:
            response = requests.post(url, json=payload, timeout=(10, 60))
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise UserError(_("Failed to ingest ticket: %s") % str(e))
