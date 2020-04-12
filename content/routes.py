from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required
from app import db
from models import Content
from content.utils import *
import json

content = Blueprint('content', __name__)

@content.route('/save_record', methods=["POST"])
@login_required
def save_record():
    data = request.get_json()
    # inputText = request.args.get('jsdata')
    inputText = data['text']
    inputText = add_class(inputText, "img", "img-fluid")
    inputText = add_img_id(inputText)
    # inputTitle = request.args.get('title')
    # inputHeader = request.args.get('header')
    inputTitle = data['title']
    inputHeader = data['header']


    article = Content.query.filter_by(title=inputTitle, header=inputHeader).first()
    if article:
        article.content = inputText
    else:
        article = Content(header=inputHeader, title=inputTitle, content=inputText)
        db.session.add(article)

    db.session.commit()

    return redirect(url_for('main.index'))

@content.route('/delete_record', methods=["GET"])
@login_required
def delete_record():
    inputTitle = request.args.get('title')
    inputHeader = request.args.get('header')

    record_to_delete = db.session.query(Content.title).filter_by(title=inputTitle, header=inputHeader).delete()
    db.session.commit()

    return redirect(url_for('main.index'))


@content.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_content():

    contentDictionary = {
        "headings" : get_headings(),
        "records" : get_records()
    }

    return render_template('dashboard/edit.html', content=contentDictionary)

@content.route('/edit_record_content', methods=["GET"])
def edit_record_content():
    given_id = int(request.args.get('id'))
    record = Content.query.get(given_id)
    if record:
        return record.content
    else:
        return "error"
    # record_content = ''
    # for record in get_records():
    #     if record.title == text:
    #         record_content = record


    # return render_template('dashboard/editor.html', content=record_content)
