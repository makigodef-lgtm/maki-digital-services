# AFICN — Site de formation en marketing digital

Site statique bilingue (français/anglais) de l'Académie Francophone Internationale des Compétences Numériques, basé à Kinshasa.

## État vérifié (6 novembre 2026)
- Pages `index.html` et `en.html` : refonte avec photographies de personnes réelles (illustrations de Pexels), programme de quatre modules et exemple pédagogique interactif.
- Aucun avatar, aucune voix de synthèse. **Aucune vidéo humaine enregistrée n'est incluse** : les images ne doivent pas être présentées comme celles de nos formateurs.
- Paiement non actif : le montant de 10 USD est indicatif. La vente de cours doit attendre la disponibilité des contenus et de la livraison après paiement.

## Paiements : préparation pour CinetPay Payment Links (RDC)
CinetPay indique prendre en charge Orange Money, M-Pesa, Airtel Money et Visa/Mastercard en RDC. Les services réels et frais doivent être confirmés dans le contrat marchand.

1. Ouvrir un compte marchand et faire vérifier l'identité professionnelle via https://cinetpay.com/products/payment-link.
2. Depuis le tableau de bord CinetPay, créer un Payment Link marchand valide pour la formation AFICN. Ne jamais mettre de clé API ou mot de passe dans ce dépôt.
3. Finaliser et vérifier la délivrance des leçons payantes avant la commercialisation. Un simple retour sur une page "paiement réussi" ne constitue pas une vérification du paiement.
4. Faire une transaction de test complète : prix, frais, confirmation effective dans le tableau de bord CinetPay et livraison du produit.
5. **Après ces contrôles seulement**, ouvrir `index.html` et `en.html` et remplacer dans chacun `const MERCHANT_PAYMENT_LINK='';` par l'URL publique réelle du lien de paiement. Le bouton n'apparaît que si une URL HTTPS d'un domaine CinetPay autorisé est fournie. Mettre les deux pages à jour ensemble.
6. Vérifier le prix, les taxes éventuelles et la procédure de remboursement avant mise en vente.

Il est déconseillé d'exposer une clé API secrète côté navigateur ou de demander à des acheteurs de transférer directement de l'argent vers un numéro personnel.

## Publication
Le dépôt GitHub contient le code source. Vérifier dans **Settings > Pages** que la publication GitHub Pages est activée sur `main` / racine. Une modification de fichier n'établit pas à elle seule que le site est public.

## Sources des photographies
- Katerina Holmes, Pexels, https://www.pexels.com/photo/black-woman-at-table-with-laptop-5905839/
- Andrea Piacquadio, Pexels, https://www.pexels.com/photo/group-of-diverse-colleagues-discussing-project-while-using-laptop-3862094/
- Anna Shvets, Pexels, https://www.pexels.com/photo/group-of-glad-multiracial-businesspeople-working-with-laptop-at-table-5324969/

Photos illustratives, sans affiliation commerciale ou recommandation des personnes photographiées.
