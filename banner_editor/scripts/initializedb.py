import os
import sys
import transaction
import string

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars
from ..lib.util import delete_contents
from ..security import hash_password

from ..models import (
    DBSession,
    Base
)

from ..security import (
    Admin,
    Group
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def create_subdirectories(folder):
    symbs = string.ascii_letters + string.digits + '?'
    for symb in symbs:
        os.mkdir(os.path.join(folder, symb))


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    static_folder = os.path.join(
        os.getcwd(), "banner_editor", "banner_editor", "static", "banners")
    delete_contents(static_folder)
    Base.metadata.create_all(engine)
    with transaction.manager:
        group = Group(name='admins')
        admin = Admin(login='admin', password=hash_password('lol'))
        group.admins.append(admin)
        DBSession.add(group)
        DBSession.flush()
