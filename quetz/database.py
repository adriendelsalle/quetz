# Copyright 2020 QuantStack
# Distributed under the terms of the Modified BSD License.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import StaticPool

Base = declarative_base()


def get_session(db_url, echo: bool = False, **kwargs) -> Session:

    kwargs['echo'] = echo

    if db_url.startswith('sqlite'):
        kwargs.setdefault('connect_args', {'check_same_thread': False})

    if db_url.endswith(':memory:'):
        # If we're using an in-memory database, ensure that only one connection
        # is ever created.
        kwargs.setdefault('poolclass', StaticPool)

    engine = create_engine(db_url, **kwargs)
    Base.metadata.create_all(engine)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()
