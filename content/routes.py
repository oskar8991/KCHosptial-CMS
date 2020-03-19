from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required
from app import db
from models import Content

content = Blueprint('content', __name__)

#This is currently never used; I left it for future usage
#Populate content table with input from add new page content
# @content.route("/populateContent", methods=['POST'])
# def populateContent():
#     db.session.add(Content(content = request.form['editBox']))
#     db.session.commit()
#     return redirect(url_for('index'))

@content.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_content():
    first_page = Content.query.get(1)

    if request.method == 'POST':
        if first_page:
            first_page.content = request.form["editBox"]
        else:
            first_page = Content(
                header = 'default',
                content = request.form["editBox"]
            )
            db.session.add(first_page)
    
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template(
        'edit.html',
        content=first_page.content if first_page else ''
    )