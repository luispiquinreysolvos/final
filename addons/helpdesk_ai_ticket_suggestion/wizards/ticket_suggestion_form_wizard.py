from odoo import fields, models


class TicketSuggestionFormWizard(models.TransientModel):
    _name = 'helpdesk.ticket.suggestion'
    _description = 'Helpdesk AI Ticket Suggestion Wizard'

    prompt = fields.Text(string='Prompt')
