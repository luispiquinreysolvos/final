# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Helpdesk AI Ticket Suggestion",
    "version": "17.0.1.0.0",
    "category": "Helpdesk",
    "summary": "AI-powered ticket generation and similar ticket suggestions",
    "description": """
        Extends OCA Helpdesk Management with AI-powered
        ticket generation and contextual ticket suggestions.
    """,
    "author": "Solvos",
    "website": "https://github.com/solvosci",
    "license": "LGPL-3",
    "depends": [
        "helpdesk_mgmt",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/ticket_suggestion_form_wizard.xml",
        "data/action_open_ai_suggestion_wizard.xml",
        "views/button_ticket_suggestion.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

