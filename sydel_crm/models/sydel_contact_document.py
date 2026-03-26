from odoo import fields, models


class SydelContactDocument(models.Model):
    _name = 'sydel.contact.document'
    _description = "Document lié à un contact"
    _order = 'upload_date desc, id desc'

    active = fields.Boolean(
        default=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Contact",
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(
        string="Nom du document",
        required=True,
    )
    file = fields.Binary(
        string="Fichier",
        attachment=True,
    )
    filename = fields.Char(
        string="Nom du fichier",
    )
    document_type = fields.Selection(
        selection=[
            ('id', "Pièce d'identité"),
            ('contract', "Contrat"),
            ('invoice', "Facture"),
            ('letter', "Lettre de mission"),
            ('legal', "Acte juridique"),
            ('tax', "Document fiscal"),
            ('other', "Autre"),
        ],
        string="Catégorie",
    )
    upload_date = fields.Date(
        string="Date d'ajout",
        default=fields.Date.today,
    )
    uploaded_by_id = fields.Many2one(
        comodel_name='res.users',
        string="Ajouté par",
        default=lambda self: self.env.uid,
    )
    notes = fields.Text(
        string="Notes",
    )
