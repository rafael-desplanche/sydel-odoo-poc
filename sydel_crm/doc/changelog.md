# Changelog — Sydel CRM

## 19.0.1.0.0 (2026-XX-XX)

### Ajouté
- Extension `res.partner` : champs personne physique (prénom, sexe, date naissance,
  situation maritale, régime matrimonial, propriétaire, revenus, RPPS, n° ordre,
  filiation)
- Extension `res.partner` : champs personne morale (forme juridique, objet social,
  SIREN, SIRET, NAF/APE, RCS, capital social, nombre de parts)
- Modèle `sydel.capital.share` : répartition du capital social avec % et montant calculé
- Modèle `sydel.company.director` : dirigeants avec fonction et dates de mandat
- Modèle `sydel.relation.type` : types de relations configurables (libellés aller/retour)
- Modèle `sydel.contact.relation` : liens professionnels avec création automatique du miroir
- Modèle `sydel.contact.document` : gestion documentaire catégorisée par contact
- Extension `crm.lead` : type de mission, dates lettre de mission, date de relance
- Pipeline CRM : 6 stages (appel découverte → lettre de mission signée/non signée)
- Tags contacts : Prospect, Client, Partenaire, Ancien client, Prescripteur
- Attribution multi-utilisateurs avec filtre "Mes contacts"
- Source d'acquisition du contact
- Sécurité : groupe Utilisateur Sydel, droits CRUD complets
- Tests unitaires : validations, computes, logique miroir des relations
