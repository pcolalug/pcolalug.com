from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_beaker import session_factory_from_settings

from sqlalchemy import engine_from_config
from sqlalchemy import create_engine

from pyramid_signup.interfaces import ISUSession
from pyramid_signup.interfaces import ISULoginForm
from pyramid_signup.interfaces import ISURegisterForm
from pyramid_signup.interfaces import ISUForgotPasswordForm
from pyramid_signup.interfaces import ISUResetPasswordForm
from pyramid_signup.interfaces import ISUProfileForm

import deform
from deform_jinja2 import jinja2_renderer_factory
from deform_jinja2.translator import PyramidTranslator

from pcolalug.models import DBSession
from pcolalug.models import Base
from pcolalug.forms import UNIForm

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    if settings.get('sqlalchemy.url', None):
        engine = engine_from_config(settings, 'sqlalchemy.')
    else:
        from bundle_config import config

        url = u"postgresql+psycopg2://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s" % config['postgres']
        engine = create_engine(url, echo=True)

    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)


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

    renderer = jinja2_renderer_factory(uni_form=True, translator=PyramidTranslator()
    )

    deform.Form.set_default_renderer(renderer)

    config.registry.registerUtility(DBSession, ISUSession)

    config.include('pyramid_mailer')

    config.include('pyramid_signup')

    config.add_view('pyramid_signup.views.AuthController', attr='login', route_name='login',
            renderer='pcolalug:templates/login.jinja2')

    config.add_view('pyramid_signup.views.ForgotPasswordController', attr='forgot_password', route_name='forgot_password',
            renderer='pcolalug:templates/forgot_password.jinja2')

    config.add_view('pyramid_signup.views.ForgotPasswordController', attr='reset_password', route_name='reset_password',
            renderer='pcolalug:templates/reset_password.jinja2')

    config.add_view('pyramid_signup.views.RegisterController', attr='register', route_name='register',
            renderer='pcolalug:templates/register.jinja2')

    config.add_view('pyramid_signup.views.ProfileController', attr='profile', route_name='profile',
            renderer='pcolalug:templates/profile.jinja2')

    override_forms = [
        ISULoginForm, ISURegisterForm, ISUForgotPasswordForm,
        ISUResetPasswordForm, ISUProfileForm
    ]
    for form in override_forms:
        config.registry.registerUtility(UNIForm, form)


    config.add_static_view('static', 'pcolalug:static', cache_max_age=3600)
    config.add_route('index', '/') 
    config.add_route('contact', '/contact')
    config.add_route('calendar', '/calendar')

    config.scan()

    return config.make_wsgi_app()
