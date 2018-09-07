from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from exceptions import IOError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.view import forbidden_view_config
from pyramid.security import (
    remember,
    forget,
    Allow
)

from .models import (
    DBSession,
    Banner
)

from security import (
    Admin,
    check_password
)

from lib.util import delete_contents

from decimal import Decimal
import os
import shutil
import logging

MESSAGES = {
    'db': 'Database operation is unavailable right now.',
    'file': 'Unable to save this file right now.',
    'delete': 'Unable to remove this banner right now.',
    'id': 'Invalid banner ID in URL.',
    'move': 'Unable to move this banner right now.',
    'login': 'Failed to login.'
}
LOG = logging.getLogger(__name__)


class BannerSchema(Schema):

    allow_extra_fields = True
    filter_extra_fields = True

    name = validators.UnicodeString(max=255)
    url = validators.URL()
    pos = validators.Number(min=0, if_missing=Banner.seq_pos.next_value())
    enabled = validators.Bool()


class MoveSchema(Schema):

    allow_extra_fields = True
    filter_extra_fields = True

    upwards = validators.StringBool()


class LoginSchema(Schema):

    allow_extra_fields = True
    filter_extra_fields = True

    login = validators.UnicodeString(max=255)
    password = validators.UnicodeString()


@view_config(route_name='home', renderer='templates/rotator.mako')
def home(request):
    banners = DBSession.query(Banner)
    return {
        'banners': banners
    }


@view_config(route_name='admin', renderer='templates/list.mako', permission='view', require_csrf=True)
def admin(request):
    banners = DBSession.query(Banner)
    return {
        'banners': banners
    }


@view_config(route_name='login', renderer='templates/login.mako')
@forbidden_view_config(renderer='templates/login.mako')
def login(request):
    form = Form(request, schema=LoginSchema())
    renderer = FormRenderer(form, csrf_field='csrf_token')
    error = MESSAGES['login']
    if request.POST and form.validate():
        admin = DBSession.query(Admin).filter(
            Admin.login == form.data['login']).first()
        if admin:
            if check_password(admin.password, form.data['password']):
                headers = remember(request, form.data['login'])
                url = request.route_url('admin')
                return HTTPFound(location=url, headers=headers)
    else:
        error = None

    if error:
        request.session.flash(error)
    return {
        'renderer': renderer
    }


@view_config(route_name='logout', permission='view')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.resource_url(request.context),
                     headers=headers)


@view_config(route_name='banner_add', renderer='templates/editor.mako', permission='edit', require_csrf=True)
def banner_add(request):
    banner = Banner()
    form = Form(request, schema=BannerSchema(), obj=banner)
    renderer = FormRenderer(form, csrf_field='csrf_token')
    if request.POST and form.validate():
        form.bind(banner)
        try:
            DBSession.add(banner)
            DBSession.flush()
            if ('image' in request.POST) and (request.POST['image'] != "") and request.POST['image'].file:
                filename = request.POST['image'].filename
                banner.image = filename
                image = request.POST['image'].file
                path = banner.full_path()
                file_path = os.path.join(path, filename)
                image.seek(0)
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(image, f)
            if not banner.image:
                banner.enabled = False
            DBSession.flush()

            url = request.route_url('admin')
            return HTTPFound(location=url)
        except SQLAlchemyError as e:
            LOG.exception(e.message)
            request.session.flash(MESSAGES['db'])
        except IOError as e:
            LOG.exception(e.message)
            request.session.flash(MESSAGES['file'])
    return {
        'renderer': renderer
    }


@view_config(route_name='banner_edit', renderer='templates/editor.mako', permission='edit', require_csrf=True)
def banner_edit(request):
    try:
        banner = DBSession.query(Banner).get(request.matchdict['id'])
    except SQLAlchemyError as e:
        request.session.flash(MESSAGES['id'])
        url = request.route_url('admin')
        return HTTPFound(location=url)

    form = Form(request, schema=BannerSchema(), obj=banner)
    renderer = FormRenderer(form, csrf_field='csrf_token')

    if request.POST and form.validate():
        form.bind(banner)
        try:
            DBSession.flush()
            if ('image' in request.POST) and (request.POST['image'] != "") and request.POST['image'].file:
                filename = request.POST['image'].filename
                image = request.POST['image'].file
                banner.image = filename
                path = banner.full_path()
                if os.path.isdir(path):
                    delete_contents(path)
                file_path = os.path.join(path, filename)
                image.seek(0)
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(image, f)
            if not banner.image:
                banner.enabled = False
            DBSession.flush()

            url = request.route_url('admin')
            return HTTPFound(location=url)
        except SQLAlchemyError as e:
            LOG.exception(e.message)
            request.session.flash(MESSAGES['db'])
        except IOError as e:
            LOG.exception(e.message)
            request.session.flash(MESSAGES['file'])
    return {
        'renderer': renderer,
        'path': banner.static_path('edit_image')
    }


@view_config(route_name='banner_delete', permission='edit', require_csrf=True)
def banner_delete(request):
    try:
        banner = DBSession.query(Banner).get(request.matchdict['id'])
        DBSession.delete(banner)
        DBSession.flush()
        url = request.route_url('admin')
    except SQLAlchemyError as e:
        LOG.exception(e.message)
        request.session.flash(MESSAGES['delete'])
        url = request.route_url('admin')
    finally:
        return HTTPFound(location=url)


@view_config(route_name='banner_move', permission='edit', require_csrf=True)
def banner_move(request):
    url = request.route_url('admin')
    form = Form(request, schema=MoveSchema())
    if form.validate():
        try:
            banner = DBSession.query(Banner).get(request.matchdict['id'])
            if form.data['upwards']:
                pos1 = DBSession.query(func.max(Banner.pos)).filter(
                    Banner.pos < banner.pos).one_or_none()
                if pos1[0] is None:
                    return HTTPFound(location=url)
                pos1 = Decimal(pos1[0])
                pos2 = DBSession.query(func.max(Banner.pos)).filter(
                    Banner.pos < pos1).one_or_none()
                if pos2[0] is None:
                    pos2 = 0
                else:
                    pos2 = Decimal(pos2[0])
                banner.pos = (pos1 + pos2) / 2
            else:
                pos1 = DBSession.query(func.min(Banner.pos)).filter(
                    Banner.pos > banner.pos).one_or_none()
                if pos1[0] is None:
                    return HTTPFound(location=url)
                pos1 = Decimal(pos1[0])
                pos2 = DBSession.query(func.min(Banner.pos)).filter(
                    Banner.pos > pos1).one_or_none()
                if pos2[0] is None:
                    pos2 = Banner.seq_pos.next_value()
                else:
                    pos2 = Decimal(pos2[0])
                banner.pos = (pos1 + pos2) / 2
            DBSession.flush()
        except SQLAlchemyError as e:
            LOG.exception(e.message)
            request.session.flash(MESSAGES['move'])
            url = request.route_url('admin')
    else:
        url = request.route_url('admin')
    return HTTPFound(location=url)
