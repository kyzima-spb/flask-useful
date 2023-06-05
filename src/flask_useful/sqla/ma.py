from __future__ import annotations
import typing as t

from marshmallow.validate import (
    Validator,
    ValidationError,
)
from sqlalchemy import inspect, select

from .session import sqla_session
from .utils import get_primary_columns


__all__ = (
    'ExistsEntity',
)


class ExistsEntity(Validator):
    """The validator checks that an entity exists."""

    def __init__(
        self,
        model_class: t.Type[t.Any],
        columns: t.Optional[t.Sequence[str]] = None,
        error: str = '',
    ) -> None:
        """
        Arguments:
            model_class:
                Reference to the model class.
            columns (iterable):
                Model attributes that must be unique.
            error (str):
                Error message.
        """
        if columns is None:
            self.columns = get_primary_columns(model_class)
        else:
            ins = inspect(model_class).columns
            self.columns = tuple(ins[c] for c in columns)

        self.error = error

    def __call__(self, *values: t.Any) -> None:
        criteria = tuple(c == v for c, v in zip(self.columns, values))
        result = sqla_session.scalar(
            select(1).where(*criteria)
        )
        if not result:
            if len(values) == 1:
                raise self.make_error(
                    'An instance with %(name)s=%(value)s does not exist.',
                    name=self.columns[0].name,
                    value=values[0],
                )
            else:
                raise self.make_error(
                    'An instance with %(attrs)s attributes does not exist.',
                    attrs=', '.join(
                        f'{c.name}={v}' for c, v in zip(self.columns, values)
                    )
                )

    def make_error(self, message: str, **kwargs: str) -> ValidationError:
        if self.error:
            message = self.error
        return ValidationError(message % kwargs)
