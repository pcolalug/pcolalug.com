from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_beaker import session_factory_from_settings

from sqlalchemy import engine_from_config
from models import initialize_sql, User

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid

class RequestWithUserAttribute(Request):
    @reify
    def user(self):
        username = unauthenticated_userid(self)

        if username is not None:
            return User.get_by_username(username)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    authn_policy = AuthTktAuthenticationPolicy('pc0lalugs0secret')
    authz_policy = ACLAuthorizationPolicy()

    session_factory = session_factory_from_settings(settings)

    config = Configurator(settings=settings)

    config = Configurator(
        settings=settings,
        root_factory='pcolalug.models.RootFactory',
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        session_factory=session_factory
    )

    config.set_request_factory(RequestWithUserAttribute)

    config.add_static_view('static', 'pcolalug:static', cache_max_age=3600)
    config.add_route('index', '/') 
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.scan()

    return config.make_wsgi_app()

