import base64

import requests
from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools.mimetypes import guess_mimetype

class HelpdeskTicketSuggestionApiClient(models.AbstractModel):
    _name = 'helpdesk.ticket.suggestion.api.client'
    _description = 'Helpdesk Ticket Suggestion API Client'

    @api.model
    def _get_suggestion_api_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('helpdesk_ai_ticket_suggestion.suggestion_api_url')

    @api.model
    def request_suggestion(self, problem_description, attachments):
        suggestion_api_url = self._get_suggestion_api_url()
        if not suggestion_api_url:
            raise UserError(_("Suggestion API URL not configured. Please configure it in the settings."))
        files = []
        for attachment in attachments:
            raw = base64.b64decode(attachment.datas)
            files.append(('file', (attachment.name, raw, guess_mimetype(raw))))
        try:
            response = requests.post(suggestion_api_url, data={'problem_description': problem_description}, files=files or None, timeout=(10, 540))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise UserError(_("Error calling Suggestion API: %s") % str(e))
