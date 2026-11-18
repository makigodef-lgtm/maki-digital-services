# Facturation mensuelle MineraLink

Composant serveur préparé, non déployé. Les formulaires publics de demande d’essai continuent de fonctionner sans mandat. Aucun numéro de carte, RIB, secret bancaire ou identifiant réel dans le dépôt.

Le futur checkout hébergé par la banque doit présenter le forfait, la date et l’heure exactes du premier débit après 14 jours, le montant mensuel, le bénéficiaire et le moyen de résilier. Conserver la preuve de l’accord et sa version dans le stockage privé. Rattacher le mandat à l’entreprise authentifiée. Appeler enroll uniquement après vérification serveur de cette confirmation. Un essai déjà consenti comme gratuit ne donne aucun droit de débit.

Le moteur gère les dates UTC, les mois courts, le refus, les échéances en attente, la résiliation et les reprises avec la même clé bancaire. Le raccordement exige une interface bancaire officielle capable de réutiliser le mandat et de rechercher une opération par référence sans la débiter deux fois. Désactiver l’ordonnanceur du marchand si la banque ordonnance elle-même les mêmes mensualités.

Pour la recette locale : depuis ce dossier, lancer python -B -m unittest -v. La banque de test n’est importée que par les tests.

Pour déployer après activation bancaire : installer l’adaptateur validé mineralink_rawbank sur un serveur à stockage persistant et accès restreint. Configurer le compte de règlement dans l’espace marchand. Relier les routes authentifiées de souscription et de résiliation. Définir MINERALINK_BILLING_DB vers une base privée hors répertoire web et exécuter worker.py périodiquement. Configurer des délais réseau bornés, la surveillance des refus et des opérations en attente, sauvegardes, contrôle d’accès et rapprochement des relevés. Une charge carte confirmée et un crédit bancaire sont deux événements distincts ; le moteur n’atteste pas du versement sur le compte. Le délai de versement est contractuel.
