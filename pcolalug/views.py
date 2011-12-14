from pyramid.view import view_config
from pyramid.security import has_permission

import urllib
from dateutil import tz
from icalendar import Calendar

from pyramid_signup.managers import UserManager
from pyramid_signup.managers import UserGroupManager
from pyramid_signup.interfaces import ISUSession

DATE_FORMAT = "%B %d, %Y @ %-I:%M %p"
DATE_FORMAT_NO_TIME = "%B %d, %Y @ All Day"

@view_config(route_name='index', renderer='index.jinja2')
def index(request):

    ics = urllib.urlopen("https://www.google.com/calendar/ical/pcolalug%40gmail.com/public/basic.ics").read()
    events = []

    cal = Calendar.from_string(ics)

    for event in cal.walk('vevent'):
        to_zone = tz.gettz('America/Chicago')

        date = event.get('dtstart').dt
        format = DATE_FORMAT
        if hasattr(date, 'astimezone'):
            date = event.get('dtstart').dt.astimezone(to_zone)
        else:
            format = DATE_FORMAT_NO_TIME

        description = event.get('description', '')
        summary = event.get('summary', '')
        location = event.get('location', '')

        if not location:
            location = "TBA"

        events.append({
                    'start': date.strftime(format),
                    'description': description if description else 'No Description',
                    'summary': summary,
                    'location': location
                    })

    sorted_list = sorted(events, key=lambda k: k['start'])

    return {'events': sorted_list[:10]}

@view_config(route_name='contact', renderer='contact.jinja2')
def contact(request):
    return {}

@view_config(route_name='calendar', renderer='calendar.jinja2')
def calendar(request):
    return {}

@view_config(permission='group:admin', route_name='admin', renderer='admin.jinja2')
def admin(request):

    mgr = UserManager(request)
    return {'users': mgr.get_all()}

def handle_profile_group(event):
    request = event.request
#    session = request.registry.getUtility(ISUSession)
#    session.commit()

    if has_permission('group:admin', request.context, request):
        mgr = UserGroupManager(request)
        group_pk = event.values.get('group', None)
        group = mgr.get_by_pk(group_pk)

        if not group in event.user.groups:
            event.user.groups.append(group)
