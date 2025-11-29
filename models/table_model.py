from models.database import mysql

class TableModel:

    @staticmethod
    def create(table):
        cur = mysql.connection.cursor()
        sql = """
            INSERT INTO table_salle (num_table, nom_table, capacite, localisation)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (
            table['num_table'],
            table['nom_table'],
            table['capacite'],
            table['localisation']
        ))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM table_salle")
        data = cur.fetchall()
        cur.close()
        return data

    @staticmethod
    def get_by_id(id_table):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM table_salle WHERE id_table = %s", (id_table,))
        data = cur.fetchone()
        cur.close()
        return data

    @staticmethod
    def update(id_table, table):
        cur = mysql.connection.cursor()
        sql = """
            UPDATE table_salle SET
                num_table=%s, nom_table=%s, capacite=%s, localisation=%s
            WHERE id_table=%s
        """
        cur.execute(sql, (
            table['num_table'],
            table['nom_table'],
            table['capacite'],
            table['localisation'],
            id_table
        ))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_by_num(num_table):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM table_salle WHERE num_table = %s", (num_table,))
        data = cur.fetchone()
        cur.close()
        return data

    @staticmethod
    def get_by_nom(nom_table):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM table_salle WHERE nom_table = %s", (nom_table,))
        data = cur.fetchone()
        cur.close()
        return data

    @staticmethod
    def delete(id_table):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM table_salle WHERE id_table = %s", (id_table,))
        mysql.connection.commit()
        cur.close()
