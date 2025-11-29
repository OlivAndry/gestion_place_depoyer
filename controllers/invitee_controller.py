from flask import Blueprint, render_template, request, redirect, url_for, make_response
from models.invitee_model import InviteeModel
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from io import BytesIO
import os
from datetime import datetime
from weasyprint import HTML

invitee_bp = Blueprint('invitee', __name__)

@invitee_bp.route('/invitee/add', methods=['GET', 'POST'])
def add_invitee():
    if request.method == 'POST':
        invitee = {
            'nom_prenoms': request.form['nom_prenoms'],
            'famille': request.form['famille'],
            'nb_personnes': request.form['nb_personnes']
        }
        InviteeModel.create(invitee)
        return redirect(url_for('invitee.list_invitee'))

    return render_template('invitee/add.html')


@invitee_bp.route('/invitee')
def list_invitee():
    data = list(InviteeModel.get_all())
    data.sort(key=lambda x: x['nom_prenoms'])
    return render_template('invitee/list.html', invitees=data)


@invitee_bp.route('/invitee/edit/<int:id_inv>', methods=['GET', 'POST'])
def edit_invitee(id_inv):
    invitee = InviteeModel.get_by_id(id_inv)

    if request.method == 'POST':
        updated = {
            'nom_prenoms': request.form['nom_prenoms'],
            'famille': request.form['famille'],
            'nb_personnes': request.form['nb_personnes']
        }
        InviteeModel.update(id_inv, updated)
        return redirect(url_for('invitee.list_invitee'))

    return render_template('invitee/add.html', invitee=invitee)


@invitee_bp.route('/invitee/delete/<int:id_inv>')
def delete_invitee(id_inv):
    InviteeModel.delete(id_inv)
    return redirect(url_for('invitee.list_invitee'))


@invitee_bp.route('/invitee/gener_invitation')
def gener_invitation_page():
    invitees = InviteeModel.get_all()
    return render_template('invitee/gener_invitation.html', invitees=invitees)


@invitee_bp.route('/invitee/gener_pdf')
def download_invitation_pdf():
    invitees = InviteeModel.get_all()
    html = render_template('invitee/pdf_invitations.html', invitees=invitees)
    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=invitations.pdf'

    return response
