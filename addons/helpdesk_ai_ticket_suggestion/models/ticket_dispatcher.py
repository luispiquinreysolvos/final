from odoo import models, fields

class TicketDispatcher(models.Model):
    _name = "helpdesk.ticket.ingest.outbox"
    _description = "Transactional Outbox for AI Ticket Ingestion"

    ticket_id = fields.Many2one("helpdesk.ticket", string="Ticket", required=True)
    state = fields.Selection(
        selection=[("draft", "Draft"), ("done", "Done"), ("error", "Error")],
        string="State",
        default="draft",
        required=True,
    )
    error_message = fields.Text(string="Error Message")

