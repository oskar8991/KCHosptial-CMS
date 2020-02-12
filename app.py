from medications import medicationsList, generateChart

from flask import Flask, render_template, request, Response, stream_with_context
app = Flask(__name__)


@app.route('/medication', methods=['GET', 'POST'])
def medication():
    if request.method == 'POST':
        selected = [med for med in medicationsList if med.name in request.form]
        return render_template('chart.html', chart=generateChart(selected))

    return render_template('medication.html', medications=medicationsList)


if __name__ == '__main__':
    app.run(debug=True)