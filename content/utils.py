from sqlalchemy import func, and_, desc
from app import db
from models import Content, FlaskUsage


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
