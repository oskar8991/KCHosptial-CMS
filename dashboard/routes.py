from flask import render_template, Blueprint
from flask_login import login_required
from dashboard.utils import *
from models import Helpful

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/dashboard")
@login_required
def dashboard_panel():
    analytics_data = {
        'weekData': week_data(datetime.today()),

        #User Platform Usage Queries
        'windowsCount': platform_usage('windows'),
        'macCount': platform_usage('macos'),
        'linuxCount': platform_usage('linux'),
        'mobileCount': platform_usage('mobile'),

        #General Count Queries
        'visitorCount': count_visitors(),
        'mostVisitedPage': most_visited(),

        'totalVisits': total_visits()
    }

    return render_template('dashboard.html', analyticsUsage=analytics_data)

@dashboard.route("/dashboard/helpful-pages")
@login_required
def helpful_pages():
    data = Helpful.query.all()

    return render_template('helpful_pages.html', stats=data)