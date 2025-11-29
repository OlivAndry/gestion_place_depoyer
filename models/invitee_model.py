from models.database import mysql

class InviteeModel:

    @staticmethod
    def create(invitee):
        cur = mysql.connection.cursor()
        sql = """
            INSERT INTO invitee (nom_prenoms, famille, nb_personnes)
            VALUES (%s, %s, %s)
        """
        cur.execute(sql, (
            invitee['nom_prenoms'],
            invitee['famille'],
            invitee['nb_personnes'],
        ))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM invitee")
        data = cur.fetchall()
        cur.close()
        return data

    @staticmethod
    def get_by_id(id_inv):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM invitee WHERE id_inv = %s", (id_inv,))
        data = cur.fetchone()
        cur.close()
        return data

    @staticmethod
    def update(id_inv, invitee):
        cur = mysql.connection.cursor()
        sql = """
            UPDATE invitee SET
                nom_prenoms=%s, famille=%s, nb_personnes=%s
            WHERE id_inv=%s
        """
        cur.execute(sql, (
            invitee['nom_prenoms'],
            invitee['famille'],
            invitee['nb_personnes'],
            id_inv
        ))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete(id_inv):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM invitee WHERE id_inv = %s", (id_inv,))
        mysql.connection.commit()
        cur.close()
