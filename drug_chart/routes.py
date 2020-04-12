from drug_chart.utils import convert_binary, generate_chart, match_hours, convert_time
from flask import Blueprint, request, render_template, session, redirect, url_for
from flask_login import login_required
from models import Medication
from app import db

drug_chart = Blueprint('drug_chart', __name__)

@drug_chart.route('/drugchart', methods=['GET', 'POST'])
def medication():
    medicationsList = Medication.query.all()
    if request.method == 'POST':
        selected = [med for med in medicationsList if med.name in request.form]
        session['meds'] = {med.name: 'checked' for med in selected}
        return render_template('drug_chart/chart.html', chart=generate_chart(selected))

    return render_template('drug_chart/index.html', medications=medicationsList)

@drug_chart.route('/drugchart/add', methods=['GET', 'POST'])
@login_required
def add_medication():
    if request.method == 'POST':
        if not match_hours(request.form['hours']):
            return redirect(url_for('drug_chart.medication'))

        hours = request.form['hours'].replace(' ', '').split(',')
        medication = Medication(
            name = request.form['name'],
            indications = request.form['indications'],
            given_hours = convert_binary(hours)
        )

        db.session.add(medication)
        db.session.commit()
        return redirect(url_for('drug_chart.medication'))

    return render_template('drug_chart/create.html')

@drug_chart.route('/drugchart/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_medication(id):
    medication = Medication.query.get(id)
    hours_repr = ', '.join(convert_time(medication.given_hours))

    if request.method == 'POST':
        if medication and match_hours(request.form['hours']):
            hours = request.form['hours'].replace(' ', '').split(',')
            medication.name = request.form['name']
            medication.indications = request.form['indications']
            medication.given_hours = convert_binary(hours)
            db.session.commit()
        
        return redirect(url_for('drug_chart.medication'))

    return render_template('drug_chart/edit.html', medication=medication, hours=hours_repr)

@drug_chart.route('/drugchart/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_medication(id):
    medication = Medication.query.get(id)
    hours_repr = ', '.join(convert_time(medication.given_hours))

    if request.method == 'POST':
        if medication:
            db.session.delete(medication)
            db.session.commit()
        
        return redirect(url_for('drug_chart.medication'))

    return render_template('drug_chart/delete.html', medication=medication, hours=hours_repr)