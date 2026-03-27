# Sydel Contact (Odoo 19)

Backend-only custom module extending `res.partner` with Sydel business data.

## Main features

- Extension of `res.partner` with Sydel fields:
  - first/last name for persons
  - stage and assigned users
  - internal notes
  - person/legal entity information
  - relations and shareholding information
  - capital and governance notes
- Dedicated models:
  - `sydel.contact.stage`
  - `sydel.contact.relation`
  - `sydel.contact.relation.type`
  - `sydel.contact.shareholding`
  - `sydel.contact.management`
  - `sydel.legal.form`
- Smart buttons on partner form for relations/shareholdings/governance
- Basic ACLs and groups
- Seed data for stages, relation types, and legal forms

## Notes

- No JS/SCSS/assets included.
- Designed to be installable on Odoo.sh as a simple backend module skeleton.
