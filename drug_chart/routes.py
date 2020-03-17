from drug_chart.utils import medicationsList, generate_chart
from flask import Blueprint, request, render_template, session

drug_chart = Blueprint('drug_chart', __name__)

@drug_chart.route('/medication', methods=['GET', 'POST'])
def medication():
    if request.method == 'POST':
        selected = [med for med in medicationsList if med.name in request.form]
        return render_template('chart.html', chart=generate_chart(selected))

    return render_template('medication.html', medications=medicationsList)