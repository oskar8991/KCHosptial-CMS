from flask import render_template, Blueprint, request, redirect, url_for, jsonify
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
    header = data['header']
    title = data['title']
    content = data['text']
    content = add_class(content, "img", "img-fluid")
    content = add_img_id(content)

    if 'id' in data:
        id = data['id']
        article = Content.query.get(id)
        if not article:
            return jsonify("An error occured")

        article.header = header
        article.title = title
        article.content = content
    else:
        article = Content(header=header, title=title, content=content)
        db.session.add(article)
    
    db.session.commit()
    return jsonify("Action executed with success")

@content.route('/delete_record', methods=["GET"])
@login_required
def delete_record():
    id = request.args.get('id')

    record = Content.query.get(id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify("Action executed with success.")
    else:
        return jsonify("The record doesn't exists.")


@content.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_content():

    contentDictionary = {
        "headings" : get_headings(),
        "records" : get_records()
    }

    return render_template('dashboard/edit.html', content=contentDictionary)

@content.route('/edit_record_content', methods=["GET"])
@login_required
def edit_record_content():
    given_id = int(request.args.get('id'))
    record = Content.query.get(given_id)
    if record:
        return jsonify(record.content)
    else:
        return jsonify("error")
