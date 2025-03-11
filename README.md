# Projet d'Analyse des Tweets - Service Client Engie
Ce projet vise à analyser des tweets adressés au service client d'Engie pour en extraire des informations pertinentes telles que les problèmes rencontrés par les clients, leur sentiment. L'objectif est d'utiliser des techniques de traitement de texte et d'intelligence artificielle pour catégoriser les réclamations et améliorer la gestion des demandes des utilisateurs.


## Méthodologie pour le Traitement des Tweets
Le traitement des tweets se fait en plusieurs étapes clés :
1. **Chargement des Données** : Les tweets sont extraits d'un fichier CSV contenant des informations structurées sous forme de colonnes telles que la date, l'id, l'utilisateur, le texte du tweet.
2. **Extraction des Informations** : Les données brutes sont nettoyées et les informations pertinentes sont extraites, notamment la date (on a separe le jour, le mois et l'annee et l'horaire), l'id de l'utilisateur et le texte du tweet
3. **Filtrage des Données** : Les utilisateurs peuvent filtrer les tweets par période, sentiment, et catégorie pour affiner les résultats.
4. **Analyse de Sentiment** : Un algorithme d'analyse de sentiment est utilisé pour classer les tweets en trois catégories : positif, neutre, ou négatif.
5. **Visualisation** : Les données traitées sont présentées sous forme de graphiques interactifs pour une analyse facile et rapide.


## KPI Retenus et Leur Signification
Les KPI suivants sont utilisés pour évaluer les performances du service client sur la base des tweets :
1. **Total des Tweets** : Le nombre total de tweets reçus dans la période donnée. Ce KPI permet de mesurer l'engagement des clients sur les réseaux sociaux.
2. **Moyenne du Score d'Inconfort** : La moyenne du score d'inconfort attribué à chaque tweet. Ce score évalue l'intensité du problème exprimé par les clients.
3. **Nombre de Catégories** : Le nombre de catégories différentes de réclamations identifiées dans les tweets. Cela permet de comprendre la diversité des problèmes rencontrés par les clients.
4. **Évolution des Tweets par Date** : Le nombre de tweets par mois, ce qui permet de suivre les tendances temporelles des problèmes rencontrés.


## Analyse de Sentiment
Pour l'analyse de sentiment on utilise **Mistral** qui classe chaque les tweets en trois catégories :
- **Positif** : Les tweets exprimant une expérience ou opinion positive.
- **Neutre** : Les tweets n'exprimant ni un avis particulièrement positif ni négatif.
- **Négatif** : Les tweets indiquant des problèmes ou des mécontentements de la part des clients.


### Logique Utilisée pour Détecter les Types de Réclamations
L'agent IA catégorise les tweets en plusieurs types de réclamations, notamment :
- **Problèmes de Facturation** : Tweets relatifs aux erreurs de facturation, aux paiements, ou aux tarifs.
- **Pannes et Urgences** : Tweets relatifs aux pannes, urgences techniques ou coupures de service.
- **Service Client Injoignable** : Tweets indiquant que les clients ne parviennent pas à joindre le service client.
- **Problèmes avec l'Application** : Tweets mentionnant des erreurs ou des difficultés d'utilisation de l'application Engie.


## Choix Technologiques pour la Visualisation
Pour la visualisation des données on a utilise  **Microsoft Excel** :
Excel est utilisé pour des analyses plus détaillées et des visualisations supplémentaires. Des graphiques dynamiques et des tableaux croisés dynamiques sont utilisés pour explorer en profondeur les tendances et les KPI.