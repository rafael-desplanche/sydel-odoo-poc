import re
from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner']

    # -------------------------------------------------------------------------
    # Champ devise (requis par les champs Monetary)
    # -------------------------------------------------------------------------
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Devise",
        default=lambda self: self.env.company.currency_id,
    )

    # -------------------------------------------------------------------------
    # Champs — Personne physique (is_company = False)
    # -------------------------------------------------------------------------
    firstname = fields.Char(
        string="Prénom",
    )
    gender = fields.Selection(
        selection=[
            ('male', "Homme"),
            ('female', "Femme"),
        ],
        string="Sexe",
    )
    birthdate = fields.Date(
        string="Date de naissance",
    )
    age = fields.Integer(
        string="Âge",
        compute='_compute_age',
        store=True,
    )
    birth_city = fields.Char(
        string="Ville de naissance",
    )
    birth_department = fields.Char(
        string="Département de naissance",
    )
    nationality_id = fields.Many2one(
        comodel_name='res.country',
        string="Nationalité",
    )
    marital_status = fields.Selection(
        selection=[
            ('single', "Célibataire"),
            ('married', "Marié(e)"),
            ('pacs', "Pacsé(e)"),
            ('divorced', "Divorcé(e)"),
            ('widowed', "Veuf/ve"),
        ],
        string="Situation maritale",
    )
    matrimonial_regime = fields.Selection(
        selection=[
            ('legal_community', "Communauté légale"),
            ('reduced_community', "Communauté réduite aux acquêts"),
            ('separation', "Séparation de biens"),
        ],
        string="Régime matrimonial",
    )
    is_owner = fields.Boolean(
        string="Propriétaire",
        default=False,
    )
    revenue = fields.Monetary(
        string="Revenus",
        currency_field='currency_id',
    )
    rpps_number = fields.Char(
        string="Numéro RPPS",
        size=11,
    )
    ordre_number = fields.Char(
        string="N° inscription à l'ordre",
        size=9,
    )
    father_name = fields.Char(
        string="Nom et prénom du père",
    )
    mother_name = fields.Char(
        string="Nom et prénom de la mère",
    )

    # -------------------------------------------------------------------------
    # Champs — Personne morale (is_company = True)
    # -------------------------------------------------------------------------
    legal_form = fields.Selection(
        selection=[
            ('sarl', "SARL"),
            ('sas', "SAS"),
            ('sa', "SA"),
            ('eurl', "EURL"),
            ('sasu', "SASU"),
            ('sci', "SCI"),
            ('snc', "SNC"),
            ('scm', "SCM"),
            ('selarl', "SELARL"),
            ('selas', "SELAS"),
            ('other', "Autre"),
        ],
        string="Forme juridique",
    )
    legal_form_other = fields.Char(
        string="Forme juridique (autre)",
    )
    corporate_purpose = fields.Text(
        string="Objet social",
    )
    rcs_city = fields.Char(
        string="Immatriculée au RCS de",
    )
    siren = fields.Char(
        string="SIREN",
        size=9,
    )
    siret = fields.Char(
        string="SIRET",
        size=14,
    )
    naf_code = fields.Char(
        string="Code NAF / APE",
        size=5,
    )
    share_capital = fields.Monetary(
        string="Capital social",
        currency_field='currency_id',
    )
    total_shares = fields.Integer(
        string="Nombre de parts / actions",
    )
    share_value = fields.Monetary(
        string="Valeur unitaire de la part",
        compute='_compute_share_value',
        store=True,
        currency_field='currency_id',
    )
    capital_share_ids = fields.One2many(
        comodel_name='sydel.capital.share',
        inverse_name='company_partner_id',
        string="Répartition du capital",
    )
    director_ids = fields.One2many(
        comodel_name='sydel.company.director',
        inverse_name='company_partner_id',
        string="Dirigeants",
    )

    # -------------------------------------------------------------------------
    # Champs — Communs (physique et morale)
    # -------------------------------------------------------------------------
    assigned_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='sydel_partner_user_rel',
        column1='partner_id',
        column2='user_id',
        string="Attribué à",
    )
    contact_note = fields.Html(
        string="Notes",
    )
    last_interaction_date = fields.Datetime(
        string="Dernière interaction",
        compute='_compute_last_interaction',
        store=True,
    )
    acquisition_source = fields.Selection(
        selection=[
            ('word_of_mouth', "Bouche-à-oreille"),
            ('website', "Site web"),
            ('referral', "Recommandation"),
            ('social_media', "Réseaux sociaux"),
            ('event', "Événement"),
            ('advertising', "Publicité"),
            ('other', "Autre"),
        ],
        string="Source d'acquisition",
    )
    opportunity_ids = fields.One2many(
        comodel_name='crm.lead',
        inverse_name='partner_id',
        string="Opportunités",
        domain="[('type', '=', 'opportunity')]",
    )
    relation_ids = fields.One2many(
        comodel_name='sydel.contact.relation',
        inverse_name='partner_id',
        string="Relations",
    )
    relation_reverse_ids = fields.One2many(
        comodel_name='sydel.contact.relation',
        inverse_name='related_partner_id',
        string="Relations (inverse)",
    )
    document_ids = fields.One2many(
        comodel_name='sydel.contact.document',
        inverse_name='partner_id',
        string="Documents",
    )

    # -------------------------------------------------------------------------
    # Compute
    # -------------------------------------------------------------------------
    @api.depends('birthdate')
    def _compute_age(self):
        today = date.today()
        for partner in self:
            if partner.birthdate:
                bd = partner.birthdate
                partner.age = today.year - bd.year - (
                    (today.month, today.day) < (bd.month, bd.day)
                )
            else:
                partner.age = 0

    @api.depends('share_capital', 'total_shares')
    def _compute_share_value(self):
        for partner in self:
            if partner.total_shares:
                partner.share_value = partner.share_capital / partner.total_shares
            else:
                partner.share_value = 0.0

    @api.depends('message_ids')
    def _compute_last_interaction(self):
        for partner in self:
            last_message = self.env['mail.message'].search(
                [('res_id', '=', partner.id),
                 ('model', '=', 'res.partner')],
                order='date desc',
                limit=1,
            )
            partner.last_interaction_date = last_message.date if last_message else False

    # -------------------------------------------------------------------------
    # Onchange
    # -------------------------------------------------------------------------
    @api.onchange('siren')
    def _onchange_siren(self):
        if self.siren and self.siret:
            if not self.siret.startswith(self.siren):
                self.siret = self.siren

    # -------------------------------------------------------------------------
    # Contraintes
    # -------------------------------------------------------------------------
    @api.constrains('rpps_number')
    def _check_rpps_number(self):
        for partner in self:
            if partner.rpps_number and not re.match(r'^\d{11}$', partner.rpps_number):
                raise ValidationError(
                    _("Le numéro RPPS doit contenir exactement 11 chiffres.")
                )

    @api.constrains('ordre_number')
    def _check_ordre_number(self):
        for partner in self:
            if partner.ordre_number and not re.match(r'^\d{9}$', partner.ordre_number):
                raise ValidationError(
                    _("Le numéro d'inscription à l'ordre doit contenir exactement 9 chiffres.")
                )

    @api.constrains('siren')
    def _check_siren(self):
        for partner in self:
            if partner.siren and not re.match(r'^\d{9}$', partner.siren):
                raise ValidationError(
                    _("Le numéro SIREN doit contenir exactement 9 chiffres.")
                )

    @api.constrains('siret')
    def _check_siret(self):
        for partner in self:
            if partner.siret and not re.match(r'^\d{14}$', partner.siret):
                raise ValidationError(
                    _("Le numéro SIRET doit contenir exactement 14 chiffres.")
                )

    @api.constrains('siren', 'siret')
    def _check_siren_siret_coherence(self):
        for partner in self:
            if partner.siren and partner.siret:
                if not partner.siret.startswith(partner.siren):
                    raise ValidationError(
                        _("Les 9 premiers chiffres du SIRET doivent correspondre au SIREN.")
                    )

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------
    def action_send_email(self):
        """Ouvre le compositeur d'email avec le destinataire pré-rempli."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_composition_mode': 'comment',
                'default_model': 'res.partner',
                'default_res_ids': self.ids,
                'default_partner_ids': [self.id],
            },
        }

    @api.constrains('naf_code')
    def _check_naf_code(self):
        for partner in self:
            if partner.naf_code and not re.match(r'^\d{4}[A-Z]$', partner.naf_code):
                raise ValidationError(
                    _("Le code NAF/APE doit être au format 4 chiffres + 1 lettre majuscule (ex: 6920Z).")
                )
