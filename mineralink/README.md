# MineraLink RDC — vitrine et espace client pilote

- `index.html` : vitrine bilingue et accès aux services.
- `espace-client.html` : espace Supabase (authentification, enregistrement d'entreprises, demandes de devis, invitations, propositions).
- `demande-rfq.html` : préparation d'une demande sans compte, avec transfert volontaire par e-mail. Ce formulaire **n'enregistre pas** les données dans Supabase.
- `commencer.html` : instructions pour les acheteurs et fournisseurs.
- Aucune solution d'encaissement, aucun agrément commercial et aucun fournisseur certifié ne sont confirmés.

## Hébergement et données

Le site est publié par GitHub Actions / GitHub Pages. L'adresse à vérifier depuis un navigateur externe est :
https://makigodef-lgtm.github.io/maki-digital-services/mineralink/

La base PostgreSQL Supabase `mineralink-rdc` contient cinq tables : `organizations`, `memberships`, `rfqs`, `invitations`, `quotes`. La sécurité RLS est activée. L'inscription dépend des confirmations e-mail et des URL autorisées dans les paramètres Auth du projet.

Le 14 novembre 2026, un scénario SQL simulant deux comptes (acheteur et fournisseur), une demande, une invitation et un devis a réussi. La transaction a été annulée pour ne laisser aucune donnée fictive. **Cet essai ne remplace pas un test navigateur avec deux adresses email confirmées.**

## Parcours complet

1. L'acheteur crée et confirme son compte, puis enregistre son entreprise.
2. Le fournisseur crée et confirme son compte, puis transmet l'identifiant de son entreprise à l'acheteur.
3. L'acheteur soumet une demande et invite le fournisseur.
4. Le fournisseur consulte la demande et enregistre un devis.
5. L'acheteur consulte les devis dans son espace.
6. Les parties négocient séparément ; aucun paiement marchand réel n'est activé.

Le projet se limite à la mise en relation et au sourcing industriel. Ne jamais annoncer un agrément qui n'a pas été obtenu. GitHub Pages est statique ; Supabase héberge les données, pas les transactions financières.
