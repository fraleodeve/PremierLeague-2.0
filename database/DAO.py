from database.DB_connect import DBConnect

class DAO():

    @staticmethod
    def getAllSquadre():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM teams"
        cursor.execute(query)

        res = []

        for row in cursor:
            res.append()

        cursor.close()
        conn.close()

        return res