from models.database import mysql

class PlacementModel:

    @staticmethod
    def clear_all():
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM placement")
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def save(id_inv, id_table, nb_personnes, reste):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO placement (id_inv, id_table, nb_personnes, place_restant)
            VALUES (%s, %s, %s, %s)
        """, (id_inv, id_table, nb_personnes, reste))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT p.id_table, t.num_table, t.nom_table, p.id_inv,
                   i.nom_prenoms, i.famille,
                   p.nb_personnes, p.place_restant
            FROM placement p
            JOIN table_salle t ON p.id_table = t.id_table
            JOIN invitee i ON p.id_inv = i.id_inv
            ORDER BY p.id_table
        """)
        rows = cur.fetchall()
        cur.close()
        return rows

    @staticmethod
    def generate_plan(tables, invites):
        # Trier familles du plus grand au plus petit
        invites = sorted(invites, key=lambda x: x['nb'], reverse=True)

        # Trier tables par capacité (pas par reste)
        tables = sorted(tables, key=lambda t: t['capacite'], reverse=True)

        plan = []
        not_placed = []

        # max_cap = max([t['capacite'] for t in tables])
        if len(tables) == 0:
            max_cap = 0
        else:
            max_cap = max([t['capacite'] for t in tables])

        for inv in invites:

            fam = inv['famille']
            qty = inv['nb']
            id_inv = inv['id_inv']

            # CAS 1 → Famille plus grande que toute table : SPLIT FORCÉ
            if qty > max_cap:
                remaining = qty

                for table in tables:
                    if remaining <= 0:
                        break

                    take = min(table['reste'], remaining)

                    if take > 0:
                        plan.append({
                            "id_table": table['id'],
                            "id_inv": id_inv,
                            "famille": fam,
                            "nb": take,
                            "reste_table": table['reste'] - take
                        })

                        table['reste'] -= take
                        remaining -= take

                if remaining > 0:
                    not_placed.append({"famille": fam, "nb": remaining, "id_inv": id_inv})

                continue

            # CAS 2 → Famille peut tenir dans UNE table → NE PAS COUPER
            possible = [table for table in tables if table['reste'] >= qty]
            if possible:
                tight = [t for t in possible if t['reste'] - qty <= 2]
                if tight:
                    best_table = min(tight, key=lambda t: t['reste'] - qty)
                else:
                    best_table = min(possible, key=lambda t: t['reste'] - qty)
            else:
                best_table = None

            if best_table:
                # Placer la famille entière
                plan.append({
                    "id_table": best_table['id'],
                    "id_inv": id_inv,
                    "famille": fam,
                    "nb": qty,
                    "reste_table": best_table['reste'] - qty
                })
                best_table['reste'] -= qty
            else:
                # Impossible
                not_placed.append({"famille": fam, "nb": qty, "id_inv": id_inv})

        # Post-processing to fill gaps, allowing splitting
        not_placed = sorted(not_placed, key=lambda x: x['nb'], reverse=True)  # Large first
        placed_in_post = True
        while placed_in_post and not_placed:
            placed_in_post = False
            for p in not_placed[:]:
                for table in tables:
                    if table['reste'] > 0:
                        take = min(p['nb'], table['reste'])
                        plan.append({
                            "id_table": table['id'],
                            "id_inv": p['id_inv'],
                            "famille": p['famille'],
                            "nb": take,
                            "reste_table": table['reste'] - take
                        })
                        table['reste'] -= take
                        p['nb'] -= take
                        placed_in_post = True
                        if p['nb'] == 0:
                            not_placed.remove(p)
                        break

        return plan, not_placed, tables
