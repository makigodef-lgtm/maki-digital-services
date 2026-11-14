# MINERALINK RDC — Tableau de lancement, 14 novembre 2026

**Mode actuel : pilote technique et prospection sans encaissement en ligne.** Le site est publié et l'installation PWA ne demande aucun compte développeur payant. L'utilisateur ne doit pas être invité à effectuer des paiements via un prestataire tant que les autorisations ne sont pas accordées.

## A. Accompli et testé

- GitHub Pages : déploiement automatisé et vérification HTTPS du site, de l'espace client et des éléments PWA.
- Supabase : authentification intégrée au code ; tables organisations, adhésions, demandes RFQ, invitations, devis.
- Sécurité : RLS active sur les tables, refus des lectures non autorisées lors des tests SQL simulés. **Attention : le test avec deux vrais comptes et confirmation e-mail reste à réaliser.**
- Répertoire de fournisseurs : publication volontaire, édition et retrait, visibles seulement aux utilisateurs connectés. Aucun fournisseur n'est étiqueté « vérifié » par défaut.
- Politique de confidentialité et conditions d'utilisation adaptées aux comptes et au répertoire.
- Contrôle automatique du code et de la disponibilité publique.

## B. Obligations administratives externes non accomplies

| Dépendance | Preuve nécessaire pour fermer le dossier | État |
|---|---|---|
| RCCM de l'établissement | Extrait RCCM délivré et contrôlé | Non constaté |
| Identification nationale / NIF | Documents réels au nom du titulaire / de l'établissement | Non constatés |
| ARSP | Qualification juridique des prestations ; enregistrement et attestation lorsque la sous-traitance visée l'exige | À instruire |
| Données personnelles | Revue des règles du Code du numérique, registre et formalités auprès de l'autorité compétente | À instruire |
| CinetPay | Approbation marchande, identifiants techniques autorisés, vérification de la transaction, retrait autorisé | En attente |
| Compte bancaire / Mobile Money lié à l'activité | Validation KYC par l'opérateur financier | En attente |
| Test réel des comptes | Deux inscriptions confirmées, dépôt RFQ, invitation, devis reçu, session clôturée | Non réalisé |
| Fournisseurs réels et clients réels | Accords et demandes légitimes ; aucune fausse donnée de test | Aucun présent dans Supabase au 14/11 |
| Vente/invoice | Devis accepté et possibilité de facturation conforme ; paiement vérifié | Non autorisé / non réalisé |

## C. Démarches en cours et liens vérifiés

1. **Formalisation** : dossier préliminaire déjà déclaré via le [ministère de l'Économie](https://economie.gouv.cd/formalisation_detail), gratuit à cette étape. Le dépôt ne suffit pas à démontrer la délivrance du RCCM. Suivi via le [GUCE](https://eguce.net/). Point à clarifier : les frais d'immatriculation sont annoncés à **30 USD** sur le site de l'[ANAPI](https://www.investindrc.cd/fr/Creation-d-entreprise-103), contre **40 USD** sur le portail [e-GUCE](https://eguce.net/) pour personne physique. Demander un écrit et **ne payer aucun lien non vérifié**.
2. **ARSP** : procédure d'[enregistrement annoncée comme gratuite](https://arsp.cd/enregistrement-et-demande-dagrement?scfm-mobile=1) ; justificatifs requis. Le [communiqué ARSP du 13/11/2026](https://arsp.cd/actualites/official-communique-no-018dgarsptb2026-new-requirements-to-obtain-or-maintain-the-registration-certificate) prévoit des pièces supplémentaires à compter du 01/12/2026 pour les activités de sous-traitance concernées. Pas d'attestation annoncée sans examen.
3. **CinetPay** : d'après les courriels commerciaux reçus les 12-13/11, l'ouverture sandbox est gratuite et le compte a été créé ; paiement Mobile Money en production subordonné aux documents et à l'approbation du risque. Les commissions annoncées sont 2,5 % d'encaissement et 2 % de reversement, sans présumer de toutes les charges applicables.
4. **FlexPaie** : frais initiaux de 100 USD communiqués par son commercial ; non retenu pour ce lancement à coût zéro.
5. **Chambre des Mines / FEC** : entretien prévu lundi **16/11/2026 à 09:00 heure de Kinshasa** (10:00 Lubumbashi). Le lien de visioconférence a été demandé ; ne pas le fabriquer.

## D. Positionnement commercial recommandé après formalisation

**Offre initiale** : recherche et qualification de fournisseurs industriels sur demande, priorités équipements de protection, maintenance, pièces, logistique, Lualaba et Haut-Katanga. Décrire les livrables et la méthode de vérification avant signature. Les estimations de prix sur le site ne sont pas des factures.

**Deux clientèles** : l'acheteur peut rémunérer une mission de qualification ; le fournisseur peut souscrire séparément une veille commerciale ou un service de présentation, sous contrat transparent. Divulguer les liens économiques pour éviter qu'une rémunération fournisseur soit confondue avec un classement neutre. Pas de commission cachée, ni de collecte des fonds dus à des vendeurs tiers.

**Stratégie sans frais de lancement** : démonstration lors de la rencontre FEC, collecte d'observations, publication du lien pilote, invitation manuelle de partenaires volontaires. Pas de promesse de revenus ni de simulation de clients.

## E. Validation de mise en production définitive

Ne cocher « commercialement opérationnel » que si :
- RCCM / NIF / IDNAT et obligations applicables vérifiés ;
- validation marchande / KYC réelle et transaction de petite valeur réussie, rapprochée au compte de destination ;
- essai multi-comptes avec e-mails réels et confirmation de connexion ;
- confidentialité, autorisations des publications et suppression des fiches vérifiées ;
- premier devis accepté, prestation exécutée et reçu / facture conforme.

Dernier contrôle technique : les tests de SQL avec annulation de transaction n'ont laissé aucune entreprise ou utilisateur fictif dans la base. Le déploiement GitHub Pages est une condition nécessaire mais non suffisante de la capacité à facturer.
