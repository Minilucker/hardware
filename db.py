import mysql.connector
import re

# Configuration de la base de données (hôte, utilisateur, mot de passe, base de données).
# super secure
db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'rfid'
    }
def check_db(uid):

    if not re.match("^[0-9]+$", uid):  # Vérifie si l'UID a un format valide (composé uniquement de chiffres).
        print(f"Invalid UID format: {uid}") 
        return False

    # Bloc 'try' pour gérer les erreurs potentielles lors de la connexion à la base de données.
    try:
        conn = mysql.connector.connect(**db_config) # Établissement de la connexion à la base de données.
        cursor = conn.cursor()
        query = "SELECT * FROM idtable WHERE identifier = %s" # Requête SQL pour sélectionner toutes les colonnes de la table 'idtable' où 'identifier' est égal à 'uid'.
        cursor.execute(query, (uid,)) 
        result = cursor.fetchone() # Récupération de la seule ligne de résultat de la requête.
        
        if (result): # Vérifie si un résultat a été obtenu.
            if result[2] == 0: # Vérifie que l'uid n'est pas révoké
                return True
            return False
        return False
    
    # Gestion des erreurs MySQL.
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
    # pour fermer la connexion, quel que soit le résultat.
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()