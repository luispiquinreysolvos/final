from odoo import _, fields, models
from odoo.exceptions import UserError


class TicketSuggestionFormWizard(models.TransientModel):
    _name = 'helpdesk.ticket.suggestion'
    _description = 'Helpdesk AI Ticket Suggestion Wizard'

    prompt = fields.Text(string='Prompt')
    files_data = fields.Binary(
        string='Images', attachment=True, copy=False
    )

    def action_suggest(self):
        self.ensure_one()
        if not self.prompt:
            raise UserError(_('Describe el problema antes de pedir una sugerencia.'))
        suggestion = self.env['helpdesk.ai.ticket.suggestion.client'].call_ai_client(self.prompt, self.files_data)

        Tag = self.env['helpdesk.ticket.tag']
        tag_ids = []

        Category = self.env['helpdesk.ticket.category']
        category_ids = []

        Attachment = self.env['ir.attachment']
        attachment_ids = []

        if self.files_data:
            attachment = self.env['ir.attachment'].create({
                'name': 'AI Ticket Suggestion',
                'type': 'binary',
                'datas': self.files_data,
            })
            attachment_ids.append(attachment.id)

        category = Category.search([
            ('name', '=ilike', suggestion.get('category', ''))
        ], limit=1)

        if not category:
            category = Category.create({
                'name': suggestion['category'].strip(),
            })
        category_ids.append(category.id)

        for tag_name in suggestion.get('tags', []):
            tag = Tag.search([
                ('name', '=ilike', tag_name.strip())
            ], limit=1)

            if not tag:
                tag = Tag.create({
                    'name': tag_name.strip(),
                })
            tag_ids.append(tag.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_partner_id': self.env.user.partner_id.id,
                'default_partner_name': self.env.user.partner_id.name,
                'default_partner_email': self.env.user.partner_id.email,
                'default_name': suggestion['title'],
                'default_description': suggestion['description'],
                'default_category_id': category.id,
                'default_priority': suggestion['priority'],
                'default_tag_ids': [(6,0,tag_ids)],
                'default_attachment_ids': [(6,0,attachment_ids)],
            },
        }
