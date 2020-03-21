from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required
from app import db
from models import FAQQuestions

faq = Blueprint('faq', __name__)

@faq.route('/faq/create', methods=['GET', 'POST'])
@login_required
def create_faq():
    if request.method == 'POST':
        faq = FAQQuestions(
            category = request.form['categoryID'], 
            question = request.form['question'],
            answer = request.form['answer'], 
        )
        db.session.add(faq)
        db.session.commit()
        return redirect(url_for('main.faq'))

    return render_template('faq/create.html')

@faq.route('/faq/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_faq(id):
    faq = FAQQuestions.query.get(id)
    if request.method == 'POST':
        if faq:
            faq.category = request.form['newCategoryID']
            faq.question = request.form['newQuestion']
            faq.answer = request.form['newAnswer']
            db.session.commit()
        
        return redirect(url_for('main.faq'))

    return render_template('faq/edit.html', faq=faq)

@faq.route('/faq/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_faq(id):
    faq = FAQQuestions.query.get(id)
    if request.method == 'POST':
        if faq:
            db.session.delete(faq)
            db.session.commit()
        
        return redirect(url_for('main.faq'))

    return render_template('faq/delete.html', faq=faq)
