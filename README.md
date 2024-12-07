SQL Injection Dumper est un script Python conçu pour tester et exploiter les vulnérabilités d'injection SQL sur des sites Web en utilisant une série de payloads SQL. Ce projet a pour objectif de démontrer comment une injection SQL peut être utilisée pour récupérer des informations sensibles depuis une base de données. Le script permet de réaliser plusieurs actions :

Tester la vulnérabilité d'injection SQL : Il envoie une série de payloads SQL pour détecter si l'application est vulnérable.
Extraire des informations de la base de données : Une fois la vulnérabilité confirmée, il peut récupérer le nom de la base de données cible.
Lister les tables de la base de données : Le script permet de découvrir les tables présentes dans la base de données.
Explorer les colonnes des tables : Après avoir identifié les tables, il permet de récupérer les colonnes de chaque table.
Dumper les données des tables : En dernier lieu, l'outil extrait les données des tables vulnérables en fonction des colonnes sélectionnées.
Fonctionnalités :
Test d'injection SQL avec plusieurs types de payloads (Union-based, Boolean-based, etc.).
Extraction de la base de données, des tables et des colonnes via des requêtes SQL injectées.
Dumping des données des tables vulnérables dans un format brut.
Personnalisation des payloads : Vous pouvez facilement ajouter de nouveaux payloads à la liste.
Interface en ligne de commande avec une sortie colorée pour une meilleure lisibilité des résultats.
Prérequis :
Python 3.x
La bibliothèque requests (installez-la via pip install requests)
Usage :
Test de base (avec un paramètre dans l'URL) :

bash
Copier le code
python Dumper.py https://exemple.com/news.php?id=1
Test avec un fichier de payloads personnalisé :

bash
Copier le code
python Dumper.py https://exemple.com/news.php?id=1 --file payload_list.txt
Test avec une URL (en utilisant l'argument -u pour passer l'URL):

bash
Copier le code
python Dumper.py -u https://exemple.com/news.php?id=1
Explication du code :
SQL_PAYLOADS : Liste de payloads SQL utilisés pour tester les injections sur les paramètres de l'URL.
test_sql_injection : Fonction qui envoie les payloads pour vérifier si l'URL est vulnérable à une injection SQL.
get_database_name, get_tables, get_columns, et dump_table_data : Fonctions qui permettent respectivement d'extraire le nom de la base de données, les tables, les colonnes, et de dumper les données des tables vulnérables.
Remarques importantes :
Usage éthique : Ce script est fourni à des fins éducatives. Vous devez obtenir une autorisation explicite avant de tester toute cible.
Licence : Ce projet est sous licence MIT. Utilisez-le à vos propres risques.
Avertissement :
L'utilisation de cet outil pour compromettre des sites Web sans autorisation est illégale et peut entraîner des conséquences juridiques. L'auteur ne sera pas responsable de l'utilisation malveillante de ce code.
