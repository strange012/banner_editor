from sqlalchemy import (
    Column,
    Index,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    text,
    func,
    Numeric,
    Sequence,
    event
)
from pyramid.threadlocal import get_current_registry
from sqlalchemy.ext.declarative import declarative_base
from exceptions import IOError

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

from lib.util import PictureSize, image_resize

import os
import string
import shutil

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Banner(Base):
    __tablename__ = 'banner'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(Text)
    image = Column(Text)
    seq_pos = Sequence(
        name='seq_pos',
        metadata=Base.metadata,
        start=1001,
        increment=1
    )
    enabled = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text('false')
    )
    pos = Column(
        Numeric(20, 10),
        nullable=False,
        default=seq_pos.next_value(),
        server_default=seq_pos.next_value()
    )

    date_created = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        server_default=func.now()
    )
    date_edited = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def full_path(self):
        if self.image:
            path = os.path.join(
                get_current_registry().settings['work.directory'],
                'banner_editor',
                'static',
                'banners',
                self.image[0] if (self.image[0] in (
                    string.ascii_letters + string.digits)) else '?',
                self.image[1] if (self.image[1] in (
                    string.ascii_letters + string.digits)) else '?',
                str(self.id)
            )
            if not os.path.isdir(path):
                os.makedirs(path)
            return path
        else:
            return ""

    def static_path(self, size):
        if self.image:
            path = os.path.join(
                'static',
                'banners',
                self.image[0] if (self.image[0] in (
                    string.ascii_letters + string.digits)) else '?',
                self.image[1] if (self.image[1] in (
                    string.ascii_letters + string.digits)) else '?',
                str(self.id)
            )
            temp_path = os.path.join(self.full_path(), size)
            try:
                if not os.path.isdir(temp_path):
                    os.mkdir(temp_path)
                if not os.path.isfile(os.path.join(temp_path, self.image)):
                    image_resize(self.full_path(), self.image,
                                 PictureSize[size])
            except IOError:
                return ""
            return os.path.join(os.path.sep, path, size, self.image)
        else:
            return ""


@event.listens_for(Banner, 'before_delete')
def receive_before_delete(mapper, connection, target):
    if target.image:
        path = target.full_path()
        if os.path.isdir(path):
            shutil.rmtree(path)


Index('idx_banner_pos', Banner.pos)
