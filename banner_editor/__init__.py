from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import (
    DBSession,
    Base,
)

from .security import (
    groupfinder,
    Root
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = SignedCookieSessionFactory('banner_editor_secret')
    authn_policy = AuthTktAuthenticationPolicy(
        'banner_editor_secret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    with Configurator(settings=settings) as config:
        config.include('pyramid_mako')
        config.add_static_view('static', 'static', cache_max_age=3600)

        config.add_route('home', '/')
        config.add_route('admin', '/admin')
        config.add_route('login', '/login')
        config.add_route('logout', '/logout')
        config.add_route('banner_add', '/admin/banner/create')
        config.add_route('banner_edit', '/admin/banner/{id}/update')
        config.add_route('banner_delete', '/admin/banner/{id}/delete')
        config.add_route('banner_move', '/admin/banner/{id}/move')

        config.set_root_factory(Root)
        config.set_session_factory(session_factory)
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)

        config.scan()
        return config.make_wsgi_app()
