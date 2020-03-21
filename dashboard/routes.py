from flask import render_template, Blueprint
from flask_login import login_required
from dashboard.utils import *

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
