from sqlalchemy import func, and_, desc
from collections import OrderedDict
from app import db
from models import Content, FlaskUsage, Glossary


def get_headings():
    '''
    Retrieves all distinct headings from database to display in edit page.
    '''
    all_headings = (db.session
        .query(Content.header)
        .distinct()
    )

    headings = []
    for heading in all_headings:
        headings.append(heading.header)
    return headings

def get_records():
    '''
    Retrives all records from content table.
    '''
    all_records = (db.session
        .query(Content.title, Content.content, Content.header, Content.page_id)
    )


    return all_records

def get_glossary():
    '''
    Retrieves a list of all the terms in the glossary.
    '''
    words = (db.session
        .query(Glossary.term, Glossary.description)
    )

    initials = {word.term[0] for word in words}

    glossary = {
        initial: [word for word in words if word.term[0] == initial] \
        for initial in initials
    }

    return OrderedDict(sorted(glossary.items()))
