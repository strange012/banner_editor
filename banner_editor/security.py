import bcrypt

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship

from models import Base, DBSession

from pyramid.security import (
    Allow
)

admin_group = Table('association', Base.metadata,
                    Column('admin_id', Integer, ForeignKey('admin.id')),
                    Column('group_id', Integer, ForeignKey('group.id'))
                    )


class Root(object):
    __name__ = ''
    __acl__ = [
        (Allow, 'group:admins', 'edit'),
        (Allow, 'group:admins', 'view')
    ]

    def __init__(self, request):
        pass


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    login = Column(String, nullable=False, unique=True)
    password = Column(Text)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    admins = relationship(
        'Admin',
        secondary=admin_group,
        backref='groups')

    def __str__(self):
        return 'group:' + self.name


def hash_password(pw):
    hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    return hashed_pw.decode('utf-8')


def check_password(expected_hash, pw):
    if expected_hash is not None:
        return bcrypt.checkpw(pw.encode('utf-8'), expected_hash.encode('utf-8'))
    return False


def groupfinder(login, request):
    admin = DBSession.query(Admin).filter(Admin.login == login).first()
    if admin:
        return [str(x) for x in admin.groups]
    return None
