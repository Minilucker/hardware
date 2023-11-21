import mysql.connector
import re


db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'rfid'
    }
def check_db(uid):

    if not re.match("^[0-9]+$", uid):
        print(f"Invalid UID format: {uid}")
        return False

   
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM idtable WHERE identifier = %s"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        result = cursor.fetchone()
        if (result):
            if result[2] == 0:
                return True
            return False
        return False

    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

uid_a_verifier = '991299458'
if check_db(uid_a_verifier):
    print(f"L'UID {uid_a_verifier} est présent dans la base de données.")
else:
    print(f"L'UID {uid_a_verifier} n'est pas présent dans la base de données.")