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
        print(result)
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