from datetime import datetime, timedelta
from sqlalchemy import func, and_, desc
from app import db
from models import FlaskUsage

def week_data(start_date):
    last_visits = (db.session
        .query(FlaskUsage.id)
        .filter(FlaskUsage.datetime > func.DATE(start_date))
        .count()
    )

    week_data = {
        'month': start_date.strftime("%m"),
        '0': {'date': start_date.strftime("%d/%m"), 'count': last_visits}
    }

    # 1(day ago) - yesterday, 2 - 2 days ago, 3 - 3 days ago .. etc. up to 6 days ago - represents a week
    for i in range(1, 7):
        day = start_date - timedelta(days=i)

        count = db.session.query(FlaskUsage.id).filter(and_(
            FlaskUsage.datetime < func.DATE(day + timedelta(days=1)),
            FlaskUsage.datetime > func.DATE(day)
        )).count()

        #Visits for the specified day
        week_data[str(i)] = {'date' : day.strftime("%d/%m") , 'count' : count}

    return week_data

def platform_usage(platform):
    return FlaskUsage.query.filter_by(ua_platform = platform).count()

def count_visitors():
    return db.session.query(FlaskUsage.remote_addr).distinct().count()

def most_visited():
    return (db.session
        .query(FlaskUsage.path,func.count(FlaskUsage.path).label('value_occurrence'))
        .group_by(FlaskUsage.path)
        .order_by(desc('value_occurrence'))
        .first()
    )

def total_visits():
    return db.session.query(FlaskUsage.id).count()