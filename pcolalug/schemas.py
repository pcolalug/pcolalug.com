import colander
import deform

from pyramid_signup.schemas import ProfileSchema
from pyramid_signup.managers import UserGroupManager
from pyramid.security import has_permission

@colander.deferred
def choices_widget(node, kw):
    request = kw.get('request')

    if request.context:
        is_admin = has_permission('group:admin', request.context, request)
        mgr = UserGroupManager(request)

        groups = mgr.get_all()

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

class LUGProfileSchema(ProfileSchema):
    group = colander.SchemaNode(
        colander.String(),
        widget=choices_widget,
        default=choices_default,
        missing=colander.null,
    )
