from pyramid.view import view_config
from pyramid.security import has_permission

import urllib
from dateutil import tz
from icalendar import Calendar
from pcolalug.models import DBSession
from pcolalug.models import Presentation
from pcolalug.models import File
from pcolalug.models import User
from pcolalug.models import Group
from pcolalug.forms import UNIForm
from pcolalug.schemas import PresentationSchema

from pyramid.httpexceptions import HTTPFound

import os
import deform
import uuid

DATE_FORMAT = "%B %d, %Y @ %-I:%M %p"
DATE_FORMAT_NO_TIME = "%B %d, %Y @ All Day"

@view_config(route_name='index', renderer='index.jinja2')
def index(request):

    ics = urllib.urlopen("https://www.google.com/calendar/ical/pcolalug%40gmail.com/public/basic.ics").read()
    events = []

    cal = Calendar.from_ical(ics)

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
                    'real_date': date,
                    'start': date.strftime(format),
                    'description': description if description else 'No Description',
                    'summary': summary,
                    'location': location
                    })

    sorted_list = sorted(events, key=lambda k: k['real_date'], reverse=True)

    return {'events': sorted_list[:10]}

@view_config(route_name='contact', renderer='contact.jinja2')
def contact(request):
    return {}

@view_config(route_name='calendar', renderer='calendar.jinja2')
def calendar(request):
    return {}

@view_config(permission='group:admin', route_name='admin', renderer='admin.jinja2')
def admin(request):

    return {'users': User.get_all(request)}

@view_config(route_name='presentations', renderer='presentations.jinja2')
def presentations(request):
    presentations = DBSession.query(Presentation).all()

    return {'presentations': presentations}

@view_config(route_name='view_presentation', renderer='presentation.jinja2')
def presentation(request):

    pk = request.matchdict.get('pk')
    presentation = DBSession.query(Presentation).get(pk)

    return {'presentation': presentation}

@view_config(route_name='add_presentation', renderer='add_presentation.jinja2')
def add_presentation(request):
    schema = PresentationSchema()
    schema = schema.bind(request=request)

    form = UNIForm(schema=schema)

    if request.method == 'GET':
        return {'form': form.render()}
    elif request.method == 'POST':
        try:
            controls = request.POST.items()
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            return {'form': e.render(), 'errors': e.error.children}

        presentation = Presentation()
        presentation.name = data['Name']
        presentation.description = data['Description']
        presentation.date = data['Date']

        presentation.presenter_pk = int(data['Presenter'])

        DBSession.add(presentation)

        # data is the posted values from the profile form, was a Photo
        # selected?
        if data['File']:
            # we are going to store this photo as <id>-profile in the upload_dir
            filename = data['File']['filename']
            name_without_ext, ext = os.path.splitext(filename)
            mimetype = data['File']['mimetype']
            uid = str(uuid.uuid4())
            uid = "%s%s" % (uid, ext)
            size = data['File']['size']
            input_file = data['File']['fp']
            upload_dir = request.registry.settings['upload_dir']

            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            file_path = os.path.join(upload_dir, uid)
            output_file = open(file_path, 'wb')
            input_file.seek(0)

            # read in all the bytes from the posted file and write them to disk
            while 1:
                file_data = input_file.read(2<<16)
                if not file_data:
                    break
                output_file.write(file_data)

            output_file.close()

            # if the user already has a profile photo model defined, just re-use it
            # and delete the current file
            if presentation.file:
                f = presentation.file
                try:
                    os.remove(os.path.join(upload_dir, f.uid))
                except OSError:
                    pass

                DBSession.delete(f)

            new_file = File(user_pk=request.user.pk)
            new_file.mimetype = mimetype
            new_file.uid = uid
            new_file.size = size
            new_file.filename = filename

            presentation.file = new_file

            DBSession.add(new_file)

        request.session.flash('Presentation successfully created.', 'success')

        return HTTPFound(location=request.route_url('presentations'))



def handle_profile_group(event):
    request = event.request
#    session = request.registry.getUtility(ISUSession)
#    session.commit()

    if has_permission('group:admin', request.context, request):
        group_pk = event.values.get('group', None)

        if group_pk:
            group = Group.get_by_pk(request, group_pk)

            if not group in event.user.groups:
                event.user.groups.append(group)
        else:
            event.user.groups.pop()
