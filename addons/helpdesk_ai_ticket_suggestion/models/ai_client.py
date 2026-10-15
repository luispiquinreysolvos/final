import base64

import requests
from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools.mimetypes import guess_mimetype

class HelpdeskAiTicketSuggestionAiClient(models.AbstractModel):
    _name = 'helpdesk.ai.ticket.suggestion.client'
    _description = 'Helpdesk AI Ticket Suggestion AI Client'

    @api.model
    def _get_ai_client_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('helpdesk_ai_ticket_suggestion.ai_client_url')

    @api.model
    def call_ai_client(self, problem_description, files_data):
        ai_client_url = self._get_ai_client_url()
        if not ai_client_url:
            raise UserError(_("AI Client URL not configured. Please configure it in the settings."))
        files = None
        if files_data:
            raw = base64.b64decode(files_data)
            files = {'file': ('image', raw, guess_mimetype(raw))}
        try:
            response = requests.post(ai_client_url, data={'problem_description': problem_description}, files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise UserError(_("Error calling AI Client: %s") % str(e))
