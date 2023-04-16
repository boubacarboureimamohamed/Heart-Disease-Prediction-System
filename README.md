# MALADIE_CARDIAQUE


## Implémentation d’une Systéme de Prédiction des Maladies Cardiaques


## Contexte du projet

Ce projet consiste à l’implémentation d'une plateforme de prédiction des maladies cardiaques pour une meilleure détection précoce des maladies cardiaques chez les patients, avec pour objectifs de réduire les coûts de détection, de connaître correctement le stade de la maladie cardiaque, d'accroître la sensibilisation sur les maladies cardiaques et de développer un modèle de prédiction efficace.

La plateforme aura une interface utilisateur/admin pour saisir les données des patients, un système de prédiction pour traiter les données et prédire les maladies cardiovasculaires, et un modèle de classification des données de santé pour permettre une bonne prise en charge des patients.

Le projet comprend également une analyse des performances de l'application et une étude de cas pour les patients cardiopathie. 


## Aperçu du projet

Une plateforme web simple qui utilise des algorithmes d'apprentissage automatique pour prédire l'état cardiaque d'une personne en fournissant des informations sur la santé de la personne, telles que l'âge, le sexe, la tension artérielle, le taux de cholestérol, etc., construite à l'aide du framework "Flask" du langage de programmation "Python".


### Aspect technique
 
  Ce projet est principalement divisé en deux parties :
 
  1. Exploration du jeu de données et l’implémentation des modèles à l'aide de "Sklearn".
  2. Développement de l'application web utilisant le framework "Flask".


### À propos de la structure du référentiel 

- Le projet consiste en un script `app.py` qui est utilisé pour exécuter l'application et qui est le moteur de cette application. L'API qui prend l'entrée de l'utilisateur et calcule une valeur prédite basée sur les modèles.
- `prediction.py` contient du code pour entrainner et tester les modèles d'apprentissage automatique.
- Le dossier *templates* contient des fichiers qui décrivent la structure et le comportement de cette application Web. Ces fichiers sont connectés à Python via le framework Flask.
- Le dossier *statique* contient les fichiers qui ajoute du style et améliore l'apparence de l'application. 


### Installation

Le code est écrit en Python. Si Python n'est pas installé, vous pouvez le trouver [ici](https://www.python.org/downloads/). Si vous utilisez une version inférieure de Python, vous pouvez effectuer une mise à niveau à l'aide du package pip, en vous assurant que vous disposez de la dernière version de pip. Pour installer les packages et les bibliothèques requis, exécutez cette commande dans le répertoire du projet après avoir cloné le dépôt :

```
pip install flask
pip install -r requirements.txt

```

**Pour cloner le dépôt**

```
git clone https://github.com/boubacarboureimamohamed/heart-disease-prediction.git

```

**Pour exécuter l'application**

```
python app.py

```

### Technologies utilisées

[![Python]](https://www.python.org/)  

[![Flask]](http://flask.pocoo.org/)  


**Quelques ressources utiles**

- **Documentation de démarrage rapide Flask** : (https://flask.palletsprojects.com/en/1.1.x/quickstart/)


### Travail futur

- Améliorer les performances du modèle.
- Ajoutez un meilleur style à l'interface utilisateur.









  
  
  


