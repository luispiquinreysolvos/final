from odoo import _, fields, models, api
from odoo.exceptions import UserError, ValidationError


class TicketSuggestionFormWizard(models.TransientModel):
    _name = 'helpdesk.ticket.suggestion'
    _description = 'Helpdesk AI Ticket Suggestion Wizard'

    prompt = fields.Text(string='Prompt')
    image_ids = fields.Many2many('ir.attachment', string='Images')

    @api.constrains("image_ids")
    def _check_image_ids(self):
        for record in self:
            if not all(
                    attachment.mimetype
                    and attachment.mimetype.startswith("image/")
                    for attachment in record.image_ids
            ):
                raise ValidationError(
                    _("Solo se permiten archivos de imagen.")
                )

    def action_suggest(self):
        self.ensure_one()
        if not self.prompt:
            raise UserError(_('Describe el problema antes de pedir una sugerencia.'))
        suggestion = self.env['helpdesk.ticket.suggestion.api.client'].request_suggestion(self.prompt, self.image_ids)

        Tag = self.env['helpdesk.ticket.tag']
        tag_ids = []

        Category = self.env['helpdesk.ticket.category']
        category_ids = []

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
                'default_attachment_ids': [(6,0,self.image_ids.ids)],
            },
        }
