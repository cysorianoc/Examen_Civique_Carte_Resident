# Simulateur Examen Civique

Bienvenue sur le dépôt du Simulateur de l'Examen Civique Français. 

Cette application a été conçue pour aider les candidats à préparer l'examen de la formation civique, une étape exigée pour l'obtention de certains titres de séjour (notamment la Carte de Résident ou la Carte de Séjour Pluriannuelle) et l'accès à la nationalité française.

## Fonctionnalités

L'application offre un environnement de test fidèle aux conditions réelles de l'examen gouvernemental :

* **Mode Entraînement :** Série de 40 questions de connaissances générales sur la France pour réviser à son rythme.
* **Mode Examen Réel :** Tirage aléatoire simulant l'examen officiel, comprenant 28 questions de connaissances et 12 questions de mises en situation.
* **Conditions d'examen :** Chronomètre strict de 45 minutes intégré à l'interface.
* **Notation officielle :** Application du seuil de réussite fixé à 32 bonnes réponses sur 40 (soit 80 % de réussite).
* **Correction détaillée :** Affichage de vos erreurs et des bonnes réponses à la fin du test pour évaluer votre progression.

## Structure du projet

Le dépôt est organisé de la manière suivante pour faciliter le déploiement sur Streamlit :

* `app.py` : Le fichier principal contenant le code et l'interface de l'application.
* `questions_connaissance_cr.json` : La base de données regroupant les questions théoriques (histoire, géographie, institutions, valeurs de la République).
* `questions_situation_cr.json` : La base de données regroupant les questions pratiques et les cas concrets de la vie quotidienne.
* `requirements.txt` : La liste des dépendances Python nécessaires au bon fonctionnement de l'application.

## Utilisation et Déploiement

Ce projet est configuré pour être déployé directement depuis GitHub vers Streamlit Community Cloud. 

Pour vous entraîner, il vous suffit de cliquer sur le lien de l'application déployée. Sélectionnez ensuite votre mode de révision dans l'interface et lancez le chronomètre pour démarrer votre test.
