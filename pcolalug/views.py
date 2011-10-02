from pyramid.security import authenticated_userid, remember, forget
from pyramid.view import view_config
from pyramid.url import route_url
from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound

from models import User

@view_config(permission='view', route_name='index', renderer='index.jinja2')
def index(request):
    return {}

@view_config(permission='view', route_name='contact', renderer='contact.jinja2')
def contact(request):
    return {}

@view_config(permission='view', route_name='login', renderer='login.jinja2')
def login_view(request):
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
    else:
        logged_in = authenticated_userid(request)
        return {'loggedin': logged_in}

    request.session.flash(u'Failed to login.')
    return {}


@view_config(permission='authed', route_name='logout')
def logout_view(request):
    request.session.invalidate()
    request.session.flash(u'Logged out successfully.')
    headers = forget(request)
    return HTTPFound(location=route_url('index', request),
                     headers=headers)   
