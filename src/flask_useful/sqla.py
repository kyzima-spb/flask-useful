from __future__ import annotations
from types import TracebackType
import typing as t
import re

from flask import current_app
import sqlalchemy as sa
from sqlalchemy.orm import Session
from werkzeug.local import LocalProxy


IdentityArgument = t.Union[t.Any, t.Tuple[t.Any, ...], t.Dict[str, t.Any]]


__all__ = (
    'generate_slug',
    'get_sqla_session',
    'normalize_pk',
    'sqla_session',
)


sqla_session = t.cast(
    Session,
    LocalProxy(lambda: get_sqla_session()),
)


def generate_slug(
    slug_field: t.Any,
    slug: str,
    session: t.Optional[Session] = None,
) -> str:
    """
    Generates a unique slug based on the passed value.

    Arguments:
        slug_field: Model attribute containing slug.
        slug (str): The desired slug value.
        session (Session): SQLAlchemy session.
    """
    if session is None:
        session = get_sqla_session()

    pattern = r'^%s(?:-([0-9]+))?$' % slug

    stmt = (
        sa.select(slug_field)
            .where(slug_field.regexp_match(pattern))
            .order_by(slug_field.desc())
            .limit(1)
    )
    found = session.scalar(stmt)

    if not found:
        return slug

    match = re.match(pattern, found)

    if match is None:
        raise AssertionError('The query found one result for the regular expression.')

    return '{}-{}'.format(slug, int(match.group(1)) + 1)


def get_sqla_session() -> Session:
    """Returns the current session instance from application context."""
    ext = current_app.extensions.get('sqlalchemy')

    if ext is None:
        raise RuntimeError(
            'An extension named sqlalchemy was not found '
            'in the list of registered extensions for the current application.'
        )

    return t.cast(Session, ext.db.session)


def normalize_pk(
    value: IdentityArgument,
    model_class: t.Type[t.Any],
) -> t.Dict[str, t.Any]:
    """Returns the primary key with a cast as a dictionary."""
    columns = tuple(
        c for c in sa.inspect(model_class).columns if c.primary_key
    )

    if not isinstance(value, tuple):
        if isinstance(value, dict):
            value = tuple(value[c.name] for c in columns)
        else:
            value = (value,)

    return {
        c.name: c.type.python_type(v) for c, v in zip(columns, value)
    }


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
