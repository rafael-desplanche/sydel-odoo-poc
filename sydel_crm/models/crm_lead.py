from odoo import fields, models


class CrmLead(models.Model):
    _inherit = ['crm.lead']

    mission_letter_sent_date = fields.Date(
        string="Date d'envoi de la lettre de mission",
    )
    mission_letter_signed_date = fields.Date(
        string="Date de signature",
    )
    next_action_date = fields.Date(
        string="Date de prochaine relance",
    )
    next_action_note = fields.Char(
        string="Prochaine action",
    )
    mission_type = fields.Selection(
        selection=[
            ('consulting', "Conseil"),
            ('accounting', "Comptabilité"),
            ('legal', "Juridique"),
            ('tax', "Fiscal"),
            ('other', "Autre"),
        ],
        string="Type de mission",
    )
