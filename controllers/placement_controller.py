from flask import Blueprint, render_template, request, make_response, redirect, url_for
from models.database import mysql
from models.placement_model import PlacementModel
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
import os
from datetime import datetime
from weasyprint import HTML

placement_bp = Blueprint('placement', __name__)

@placement_bp.route('/placement/generate', methods=['GET'])
def generate():
    cur = mysql.connection.cursor()

    # Tables
    cur.execute("SELECT id_table, nom_table, capacite FROM table_salle")
    t = cur.fetchall()
    tables = [{"id": x["id_table"], "nom": x["nom_table"], "capacite": x["capacite"], "reste": x["capacite"]} for x in t]

    # Invites
    cur.execute("SELECT id_inv, famille, nb_personnes FROM invitee")
    i = cur.fetchall()
    invites = [{"id_inv": x["id_inv"], "famille": x["famille"], "nb": x["nb_personnes"]} for x in i]
    cur.close()

    # Algorithme
    plan, not_placed, updated_tables = PlacementModel.generate_plan(tables, invites)

    # Enrich not_placed with nom_prenoms
    cur = mysql.connection.cursor()
    for np in not_placed:
        cur.execute("SELECT nom_prenoms FROM invitee WHERE id_inv = %s", (np['id_inv'],))
        inv = cur.fetchone()
        np['nom'] = inv['nom_prenoms']
    cur.close()

    # Calculer stats
    total_not_placed = sum(p['nb'] for p in not_placed)
    remaining_tables = [t for t in updated_tables if t['reste'] > 0]
    num_remaining_tables = len(remaining_tables)
    all_remaining_zero = all(t['reste'] == 0 for t in updated_tables)

    # Save DB
    PlacementModel.clear_all()
    for row in plan:
        PlacementModel.save(row["id_inv"], row["id_table"], row["nb"], row["reste_table"])

    saved = PlacementModel.get_all()

    # Create dict of table capacities
    table_capacities = {t['id']: t['capacite'] for t in tables}

    # Group by table for display
    grouped_tables = {}
    for row in saved:
        table_id = row['id_table']
        if table_id not in grouped_tables:
            grouped_tables[table_id] = {
                'num_table': row['num_table'],
                'nom_table': row['nom_table'],
                'capacite': table_capacities.get(table_id, 0),
                'localisation': row.get('localisation', ''),
                'guests': []
            }
        grouped_tables[table_id]['guests'].append({
            'nom': row['nom_prenoms'],
            'famille': row['famille'],
            'nb_personnes': row['nb_personnes']
        })

    # Sort tables by num_table numerically
    sorted_tables = sorted(grouped_tables.values(), key=lambda x: int(x['num_table']))

    return render_template("placement/result.html",
                           tables_grouped=sorted_tables,
                           not_placed=not_placed,
                           tables=updated_tables,
                           total_not_placed=total_not_placed,
                           num_remaining_tables=num_remaining_tables,
                           all_remaining_zero=all_remaining_zero)


@placement_bp.route('/placement/table_generer')
def table_generer():
    saved = PlacementModel.get_all()

    # Group by guest
    grouped_guests = {}
    for row in saved:
        guest_id = row['id_inv']
        if guest_id not in grouped_guests:
            # Get total invited from invitee
            cur = mysql.connection.cursor()
            cur.execute("SELECT nb_personnes FROM invitee WHERE id_inv = %s", (guest_id,))
            total_inv = cur.fetchone()['nb_personnes']
            cur.close()
            grouped_guests[guest_id] = {
                'nom': row['nom_prenoms'],
                'famille': row['famille'],
                'nb_personnes': total_inv,
                'tables': []
            }
        grouped_guests[guest_id]['tables'].append({
            'num_table': row['num_table'],
            'nom_table': row['nom_table'],
            'nb_placed': row['nb_personnes']
        })

    # Sort guests by nom
    sorted_guests = sorted(grouped_guests.values(), key=lambda x: x['nom'])

    return render_template("placement/table_generer.html", grouped_guests=sorted_guests)


@placement_bp.route('/placement/reset')
def reset_placement():
    PlacementModel.clear_all()
    return redirect('/')


@placement_bp.route('/placement/pdf')
def download_placement_pdf():
    saved = PlacementModel.get_all()

    # Group by guest
    grouped_guests = {}
    for row in saved:
        guest_id = row['id_inv']
        if guest_id not in grouped_guests:
            # Get total invited from invitee
            cur = mysql.connection.cursor()
            cur.execute("SELECT nb_personnes FROM invitee WHERE id_inv = %s", (guest_id,))
            total_inv = cur.fetchone()['nb_personnes']
            cur.close()
            grouped_guests[guest_id] = {
                'nom': row['nom_prenoms'],
                'famille': row['famille'],
                'nb_personnes': total_inv,
                'tables': []
            }
        grouped_guests[guest_id]['tables'].append({
            'num_table': row['num_table'],
            'nom_table': row['nom_table'],
            'nb_placed': row['nb_personnes']
        })

    # Sort guests by nom
    sorted_guests = sorted(grouped_guests.values(), key=lambda x: x['nom'])

    html = render_template("placement/pdf_placement.html", grouped_guests=sorted_guests)
    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=plan_table.pdf'

    return response
