from odoo import api, models

class TicketAI(models.Model):
    _inherit = "helpdesk.ticket"

    @api.model_create_multi
    def create(self, vals_list):
        tickets = super().create(vals_list)
        # The outbox is technical: the user already passed the create check on
        # helpdesk.ticket above, so enqueue without requiring outbox ACLs.
        self.env["helpdesk.ticket.ingest.outbox"].sudo().create(
            [{"ticket_id": ticket.id} for ticket in tickets]
        )
        return tickets
