# MineraLink : fondation backend sécurisée (non déployée)

Ce dossier contient une **migration PostgreSQL/Supabase** pour les organisations, appartenances, demandes RFQ, invitations et devis. Il ne s'agit **pas** d'un service opérationnel. GitHub Pages reste un hébergement statique.

## Déploiement contrôlé
1. Créer un projet Supabase privé et choisir la région adaptée aux obligations de protection des données.
2. Examiner la migration et l'appliquer dans l'éditeur SQL du projet. Ne jamais publier la clé `service_role` ou les mots de passe dans GitHub ou le navigateur.
3. Configurer l'authentification, la vérification des adresses email, les restrictions d'inscription, les limites de débit, les sauvegardes, la journalisation et la politique de conservation.
4. Créer des fonctions serveur sécurisées pour l'inscription d'une organisation avec son propriétaire, l'invitation d'un fournisseur, la validation des dossiers et la transition des statuts. Les permissions d'écriture correspondantes sont **volontairement fermées**.
5. Écrire des tests d'isolation entre deux entreprises : un fournisseur non invité ne doit pas lire une RFQ, un acheteur ne doit pas modifier le devis d'autrui, un membre ne doit pas s'attribuer le statut « vérifié ».
6. Préparer les notices légales et les consentements, puis connecter l'interface uniquement après validation des tests et du fonctionnement réel sur mobile.

## Modèle de confiance
- Chaque utilisateur est authentifié par `auth.users`.
- Chaque organisation possède des membres.
- Les RFQ appartiennent aux organisations acheteuses.
- Les fournisseurs ne voient que les RFQ auxquelles ils sont invités.
- Les devis appartiennent aux organisations fournisseurs invitées.
- Les statuts de vérification ne sont pas modifiables directement par les utilisateurs.

**Important :** aucune base de données, authentification, notification ni paiement n'est actuellement activé par ce commit. L'activation nécessite un projet d'hébergement et une configuration sécurisée.
