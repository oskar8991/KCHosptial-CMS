from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required
from app import db
from models import Content
from content.utils import *
import json

content = Blueprint('content', __name__)

@content.route('/save_record', methods=["GET"])
@login_required
def save_record():
    print("Start")
    inputText = request.args.get('jsdata')
    inputTitle = request.args.get('title')

    print(inputText)
    if (db.session.query(Content.title).filter_by(title=inputTitle).count()) == 1:
        db.session.query(Content.title).filter_by(title=inputTitle).update({Content.content:inputText})
        db.session.commit()
        print("update")
    else:
        newRecord = Content(header="Liver Disease", title=inputTitle, content=inputText)
        db.session.add(newRecord)
        db.session.commit()
        print("New")
    print("Finish")
    return redirect(url_for('main.index'))

@content.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_content():


    first_page = Content.query.get(1)
    contentDictionary = {
        "headings" : get_headings(),
        "records" : get_records()
    }

    if request.method == "POST" and request.form.get('heading'):
        contentDictionary["records"] = get_records()

    if request.method == 'POST' and request.form.get('data'):
        if first_page:
            data=request.form.get('data')

            first_page.content = data
            db.session.commit()
        else:
            first_page = Content(
                header = 'default',
                content = "failure?"
            )
            db.session.add(first_page)

            db.session.commit()


    return render_template(
        'edit.html',
        content=contentDictionary if first_page else ''
    )

@content.route('/edit_record_content', methods=["GET"])
def edit_record_content():
    text = request.args.get('jsdata')
    for record in get_records():
        if record.title == text:
            record_content = record.content


    return render_template('editor.html', content=record_content)
