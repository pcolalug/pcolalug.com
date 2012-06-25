import colander
import deform

from horus.schemas import ProfileSchema
from pyramid.security import has_permission

from deform.interfaces import FileUploadTempStore

import os

tmpstore = FileUploadTempStore()
from pcolalug.models import Group
from pcolalug.models import User

@colander.deferred
def choices_widget(node, kw):
    request = kw.get('request')

    if request.context:
        is_admin = has_permission('group:admin', request.context, request)
        groups = Group.get_all(request)

        if is_admin:
            choices = [
                ('', '- None -'),
            ]

            for group in groups:
                choices.append((str(group.pk), group.name))

            return deform.widget.SelectWidget(values=choices)

    return deform.widget.HiddenWidget()

@colander.deferred
def choices_default(node, kw):
    request = kw.get('request')

    if request.context:
        if len(request.context.groups) > 0:
            return str(request.context.groups[0].pk)

@colander.deferred
def presenter_widget(node, kw):
    request = kw.get('request')

    choices = [
        ('', '- None -'),
    ]

    for user in User.get_all(request):
        choices.append((str(user.pk), user.display_name))

    return deform.widget.SelectWidget(values=choices)

@colander.deferred
def presenter_default(node, kw):
    request = kw.get('request')
    return str(1)
#
#    return str(request.context.presenter_pk)

class LUGProfileSchema(ProfileSchema):
    group = colander.SchemaNode(
        colander.String(),
        widget=choices_widget,
        default=choices_default,
        missing=colander.null,
    )

@colander.deferred
def file_default(node, kw):
    """ This will get the file from a specific presentation and set it as the
    value in the profile form
    """
    return {'filename': None, 'uid': None}
#    request = kw.get('request')
#
#    upload_dir = request.registry.settings['upload_dir']
#
#    if request.context.profile:
#        if request.context.profile.photo:
#            photo = request.context.profile.photo
#            try:
#                with open(os.path.join(upload_dir, photo.uid)) as f:
#                    # This is the dictionary configuration a file upload widget wants
#                    return {'fp': f,
#                        'mimetype': photo.mimetype,
#                        'preview_url': photo.public_url(request),
#                        'uid': photo.uid,
#                        'filename': photo.filename,
#                        'size': photo.size 
#                    }
#            # If file doesn't exist, don't crash.
#            except IOError:
#                pass
#
#    return {'filename': None, 'uid': None}

class PresentationSchema(colander.Schema):
    Name = colander.SchemaNode(colander.String())
    Description = colander.SchemaNode(colander.String())
    Date = colander.SchemaNode(colander.Date())
    Presenter = colander.SchemaNode(
        colander.String(),
        widget=presenter_widget,
        default=presenter_default,
        missing=colander.null,
    )

    File = colander.SchemaNode(
        deform.FileData(),
        widget=deform.widget.FileUploadWidget(tmpstore),
        missing=None,
        default=file_default
    )
