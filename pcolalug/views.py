from pyramid.security import authenticated_userid, remember, forget
from pyramid.view import view_config
from pyramid.url import route_url
from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
import urllib
from models import User
from dateutil import tz
from icalendar import Calendar
DATE_FORMAT = "%B %d, %Y @ %-I:%M %p"
DATE_FORMAT_NO_TIME = "%B %d, %Y @ All Day"

@view_config(permission='view', route_name='index', renderer='index.jinja2')
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

        events.append({
                    'start': date.strftime(format),
                    'description': description if description else 'No Description',
                    'summary': summary,
                    })

    sorted_list = sorted(events, key=lambda k: k['start'])

    return {'events': sorted_list[:10]}

@view_config(permission='view', route_name='contact', renderer='contact.jinja2')
def contact(request):
    return {}

@view_config(permission='view', route_name='calendar', renderer='calendar.jinja2')
def calendar(request):
    return {}

@view_config(permission='view', route_name='login', renderer='login.jinja2')
def login(request):
    main_view = route_url('index', request)
    came_from = request.params.get('came_from', main_view)
    post_data = request.POST

    if 'submit' in post_data:
        login = post_data['login']
        password = post_data['password']

        if User.check_password(login, password):
            headers = remember(request, login)
            request.session.flash(u'Logged in successfully.')
            return HTTPFound(location=came_from, headers=headers)
        request.session.flash(u'Failed to login.')
    else:
        logged_in = authenticated_userid(request)

        if logged_in:
            return HTTPFound(location=came_from, headers=headers)

    return {}


@view_config(permission='authed', route_name='logout')
def logout(request):
    request.session.invalidate()
    request.session.flash(u'Logged out successfully.')
    headers = forget(request)
    return HTTPFound(location=route_url('index', request),
                     headers=headers)   
