from __future__ import annotations
from types import TracebackType
import typing as t

from flask import current_app
from sqlalchemy.orm import Session
from werkzeug.local import LocalProxy


__all__ = (
    'get_sqla_session',
    'sqla_session',
    'SessionMixin',
)


sqla_session = t.cast(
    Session,
    LocalProxy(lambda: get_sqla_session()),
)


def get_sqla_session() -> Session:
    """Returns the current session instance from application context."""
    ext = current_app.extensions.get('sqlalchemy')

    if ext is None:
        raise RuntimeError(
            'An extension named sqlalchemy was not found '
            'in the list of registered extensions for the current application.'
        )

    return t.cast(Session, ext.db.session)


class SessionMixin:
    """
    The mixin adds a property with the current session
    and an auto-commit context manager.
    """

    def __enter__(self) -> Session:
        return self.session

    def __exit__(
        self,
        err_type: t.Optional[t.Type[BaseException]],
        err: t.Optional[BaseException],
        traceback: t.Optional[TracebackType]
    ) -> t.Optional[bool]:
        if err is None:
            self.session.commit()
        return None

    @property
    def session(self) -> Session:
        return sqla_session
