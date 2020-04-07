from collections import OrderedDict
from app import db
from models import Content, FlaskUsage, Glossary, Questions
from quiz.utils import get_questions


def get_headings():
    '''
    Retrieves all distinct headings from database to display in edit page.
    '''
    headings = db.session.query(Content.header).distinct()
    return [heading.header for heading in headings]

def get_records():
    '''
    Retrives all records from content table.
    '''
    return Content.query.all()

def get_glossary():
    '''
    Retrieves a list of all the terms in the glossary.
    '''
    words = Glossary.query.all()
    initials = {word.term[0] for word in words}
    glossary = {
        initial: [word for word in words if word.term[0] == initial] \
        for initial in initials
    }

    return OrderedDict(sorted(glossary.items()))

def get_by_title(title):
    return Content.query.filter_by(title = title).first()

def assossiated_questions():
    quiz = {
        record.page_id: get_questions(record.page_id)
        for record in Content.query.all() if get_questions(record.page_id)
    }

    return quiz
