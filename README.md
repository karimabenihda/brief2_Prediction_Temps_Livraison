**Prédiction du Temps de Livraison**

***Développer un pipeline complet de Machine Learning supervisé pour Prédire le temps total de livraison d’une commande pour améliorer le service client et optimiser les tournées.*** 

**Lien trello:https://trello.com/b/8lPlmp3S/briefpredictiontempslivraison**

**🧩 Étape 1 : Analyse exploratoire des données (EDA)**
***Le dataset contient 1000 lignes et 9 colonnes : float64(2), int64(3), object(4)***

***🔍 Description et analyse initiale:***
***Utiliser describe() et info() pour examiner les types de données et détecter les anomalies.***
***Convertir la colonne TotalCharges (type string) en float.***
***Identifier et supprimer les doublons.***
***Traiter les valeurs manquantes (remplacement par la moyenne).***

***📊 Visualisations:***
***Analyse univariée : scatter: Visualiser la distribution de DeliveryTime.***
***Analyse bivariée : ***
***utiliser 4 diagram countplot :(Weather, Traffic_Level, Time_of_Day et  Vehicle_Type ) chaque column avec nombre de commande.***
***utiliser 3 diagram boxplot :(Traffic_Level,Time_of_Day et Weather) permettent de visualiser la répartition, la médiane et la variabilité du Delivery_Time_min selon chaque catégorie, afin d’identifier l’influence de ces variables sur le temps de livraison.***

***🔗 Corrélation:***
***Générer une matrice de corrélation pour observer les relations entre les variables.***


**🧩 Étape 2 : Préparation des données**
***Encodage des variables catégorielles avec LabelEncoder. Réduire la variété des valeurs en utilisant les variables numérique avec StandardScaler***
***Utiliser select Kbest pour selection les plus 3 importantes variables (Distance_km,Preparation_Time_min,Traffic_Level_High)***
***Splitter les colonnes pour train et test : X (toutes les colonnes sauf Delivery_Time_min et Order_ID) et y (Delivery_Time_min) avec train_test_split.***
***Créer un object qui contient le nom de model ,param_grid pour compare RandomForestRegressor et SVR à l’aide de GridSearchCV, évalue leurs performances sur un jeu de test à l’aide des métriques MAE et R², puis sélectionne le meilleur modèle en fonction de l’erreur moyenne absolue.***

**🧩 Étape 3 : Tests unitaires avec Pytest (test_pipeline.py)**
***La fonction test_dimension() est un test unitaire (destiné à être exécuté avec pytest) qui vérifie deux choses essentielles :***
***La cohérence des dimensions entre les variables explicatives (X) et la variable cible (y).***
***La performance minimale du meilleur modèle (via la métrique MAE).***

**🧩 Étape 4 : Rédiger le rapport (README.md)**
***Tracer un tableau récapitulatif qui décrit la différence entre les deux modèles au niveau de R² et mae.***


