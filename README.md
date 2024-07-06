# To-do-list-app-python
# Liste de Tâches - TodoListApp

## Description

Ce programme est une application de liste de tâches basée sur `tkinter`, une bibliothèque graphique de Python. Il permet aux utilisateurs de créer, éditer, supprimer et gérer des tâches avec des fonctionnalités telles que la recherche, le tri, la catégorisation, et les rappels.

## Fonctionnalités

- Ajouter, éditer et supprimer des tâches.
- Filtrer les tâches par catégories.
- Rechercher des tâches par titre.
- Trier les tâches par date limite.
- Marquer les tâches comme terminées.
- Supprimer les tâches terminées.
- Sauvegarder et charger des tâches à partir de fichiers.
- Sauvegarder et charger les catégories.
- Rappels pour les tâches proches de leur date limite.

## Installation

1. Cloner le dépôt ou télécharger les fichiers.
2. Assurez-vous d'avoir Python installé sur votre machine.
3. Installez les dépendances nécessaires avec la commande suivante :
    
    ```bash
    pip install tk
    
    ```
    

## Utilisation

1. Exécutez le script principal `TodoListApp.py` :
    
    ```bash
    python TodoListApp.py
    
    ```
    
2. Utilisez l'interface graphique pour gérer vos tâches et catégories.

## Sauvegarde et Chargement des Données

- Les tâches peuvent être sauvegardées dans un fichier texte et chargées à partir de celui-ci.
- Les catégories sont sauvegardées dans un fichier JSON (`categories.json`).

## Rappels

Un thread en arrière-plan vérifie régulièrement les rappels de tâches et affiche une notification 30 minutes avant la date limite de chaque tâche.

## Auteur

Ce programme a été développé par [Votre Nom].

## Remarques

- Assurez-vous que le fichier `categories.json` est dans le même répertoire que le script principal pour que le chargement des catégories fonctionne correctement.
- Si vous rencontrez des problèmes, vérifiez les permissions d'écriture et de lecture pour les fichiers utilisés par l'application.
