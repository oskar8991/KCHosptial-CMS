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
    inputHeader = request.args.get('header')

    print(inputText)
    if (db.session.query(Content.title).filter_by(title=inputTitle, header=inputHeader).count()) == 1:
        db.session.query(Content.title).filter_by(title=inputTitle, header=inputHeader).update({Content.content:inputText})
        db.session.commit()
        print("update")
    else:
        newRecord = Content(header=inputHeader, title=inputTitle, content=inputText)
        db.session.add(newRecord)
        db.session.commit()
        print("New")
    print("Finish")
    return redirect(url_for('main.index'))

@content.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_content():

    contentDictionary = {
        "headings" : get_headings(),
        "records" : get_records()
    }

    return render_template(
        'edit.html',
        content=contentDictionary
    )

@content.route('/edit_record_content', methods=["GET"])
def edit_record_content():
    text = request.args.get('jsdata')
    for record in get_records():
        if record.title == text:
            record_content = record


    return render_template('editor.html', content=record_content)
