# Rapport : Simulation de Transport de Conteneurs

## 1. Introduction

Ce projet implémente une simulation de transport de conteneurs sur l'axe Seine, mettant l'accent sur le transport fluvial. La simulation modélise le mouvement des conteneurs entre différents terminaux portuaires en utilisant un système de barges.

## 2. Architecture du Système

### 2.1 Composants Principaux

#### Terminal (`Terminal`)
- Représente un point de chargement/déchargement
- Attributs :
  - Capacité maximale
  - Nombre actuel de conteneurs
  - Identifiant unique
  - Nom

#### Conteneur (`Container`)
- Unité de base du transport
- Attributs :
  - Type (TEU)
  - Terminal d'origine et de destination
  - Dates (demande, disponibilité, échéance)
  - Priorité
  - Statut (en attente, en transit, livré)

#### Service (`Service`)
- Définit une liaison régulière entre deux terminaux
- Attributs :
  - Terminaux d'origine et de destination
  - Capacité
  - Durée du trajet
  - Horaires de départ
  - Charge actuelle

#### Barge (`Barge`)
- Véhicule de transport
- Attributs :
  - Capacité
  - Terminal actuel
  - Service actuel
  - Liste des conteneurs
  - Statut (idle, loading, in_transit, unloading)

### 2.2 Contrôleur de Simulation (`TransportSimulation`)

Gère l'ensemble de la simulation avec les fonctionnalités suivantes :
- Ajout de terminaux, services, barges et conteneurs
- Mise à jour des positions des barges
- Gestion des statuts des conteneurs
- Calcul des métriques de performance
- Affichage des statistiques

## 3. Fonctionnement de la Simulation

### 3.1 Cycle de Simulation

1. Initialisation :
   - Création des terminaux
   - Définition des services
   - Ajout des barges
   - Enregistrement des demandes de transport

2. Boucle principale (pas de 30 minutes) :
   - Mise à jour des positions des barges
   - Affectation des barges disponibles aux services
   - Mise à jour des statuts des conteneurs
   - Affichage des statistiques

### 3.2 Logique de Transport

- Les barges sont affectées aux services en fonction de :
  - Leur position actuelle
  - La disponibilité des conteneurs
  - La capacité du service
- Les conteneurs sont chargés selon :
  - Leur priorité
  - Leur date de disponibilité
  - La capacité des barges

## 4. Métriques de Performance

La simulation suit plusieurs indicateurs :
- Nombre total de conteneurs
- Conteneurs livrés/en transit/en attente
- Nombre de barges actives
- Taux d'utilisation des terminaux

## 5. Scénario Implémenté

### 5.1 Infrastructure

- 5 terminaux :
  - Le Havre (2000 TEU)
  - Rouen (1500 TEU)
  - Paris (1800 TEU)
  - Gennevilliers (1200 TEU)
  - Bonneuil (1000 TEU)

### 5.2 Services

- Le Havre → Rouen : 4 services/jour
- Rouen → Paris : 3 services/jour
- Paris → Gennevilliers : 6 services/jour
- Paris → Bonneuil : 4 services/jour

### 5.3 Flotte

- 2 grandes barges maritimes (100 et 80 TEU)
- 1 barge fluviale moyenne (60 TEU)
- 2 petites barges fluviales (40 TEU chacune)

## 6. Extensions Possibles

1. Intégration d'autres modes de transport :
   - Transport ferroviaire
   - Transport routier

2. Améliorations du modèle :
   - Conditions météorologiques
   - Pannes et maintenance
   - Contraintes de navigation
   - Coûts de transport

3. Optimisations :
   - Algorithmes d'affectation plus sophistiqués
   - Planification dynamique des services
   - Gestion des priorités plus complexe

## 7. Conclusion

Cette simulation fournit une base solide pour modéliser le transport fluvial de conteneurs. Elle permet d'analyser les flux de transport et d'identifier les goulots d'étranglement potentiels dans le système. Les extensions proposées permettraient d'enrichir le modèle pour une représentation plus fidèle de la réalité opérationnelle.
