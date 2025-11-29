from flask import Blueprint, render_template, request, redirect, url_for
from models.table_model import TableModel

table_bp = Blueprint('table_salle', __name__)

@table_bp.route('/table/add', methods=['GET', 'POST'])
def add_table():
    error = None
    if request.method == 'POST':
        num_table = request.form['num_table']
        nom_table = request.form['nom_table']

        # Check if num_table exists
        existing_num = TableModel.get_by_num(num_table)
        if existing_num:
            error = f"Numéro table '{num_table}' existe déjà."

        # Check if nom_table exists
        existing_nom = TableModel.get_by_nom(nom_table)
        if existing_nom:
            if error:
                error += f" Nom table '{nom_table}' existe déjà."
            else:
                error = f"Nom table '{nom_table}' existe déjà."

        if not error:
            table = {
                'num_table': num_table,
                'nom_table': nom_table,
                'capacite': request.form['capacite'],
                'localisation': request.form['localisation']
            }
            TableModel.create(table)
            return redirect(url_for('table_salle.list_table'))

    return render_template('table/add.html', error=error)


@table_bp.route('/table')
def list_table():
    data = list(TableModel.get_all())
    data.sort(key=lambda x: x['num_table'])
    return render_template('table/list.html', tables=data)


@table_bp.route('/table/edit/<int:id_table>', methods=['GET', 'POST'])
def edit_table(id_table):
    table = TableModel.get_by_id(id_table)
    error = None

    if request.method == 'POST':
        num_table = request.form['num_table']
        nom_table = request.form['nom_table']

        # Check if num_table exists and not the current one
        existing_num = TableModel.get_by_num(num_table)
        if existing_num and existing_num['id_table'] != id_table:
            error = f"Numéro table '{num_table}' existe déjà."

        # Check if nom_table exists and not the current one
        existing_nom = TableModel.get_by_nom(nom_table)
        if existing_nom and existing_nom['id_table'] != id_table:
            if error:
                error += f" Nom table '{nom_table}' existe déjà."
            else:
                error = f"Nom table '{nom_table}' existe déjà."

        if not error:
            updated = {
                'num_table': num_table,
                'nom_table': nom_table,
                'capacite': request.form['capacite'],
                'localisation': request.form['localisation']
            }
            TableModel.update(id_table, updated)
            return redirect(url_for('table_salle.list_table'))

    return render_template('table/add.html', table=table, error=error)


@table_bp.route('/table/delete/<int:id_table>')
def delete_table(id_table):
    TableModel.delete(id_table)
    return redirect(url_for('table_salle.list_table'))
