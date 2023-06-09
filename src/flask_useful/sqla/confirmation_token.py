from __future__ import annotations
import typing as t

from sqlalchemy import delete, select

from ..confirmation_token import (
    ConfirmationToken as _ConfirmationToken,
    ConfirmationTokenSerializer as _ConfirmationTokenSerializer,
    TokenProtocol,
)
from ..decorators import getattr_or_implement
from .session import sqla_session


__all__ = (
    'ConfirmationToken',
    'ConfirmationTokenSerializer',
)


class SQLATokenMixin:
    model_class: t.Type[t.Any]

    def delete_user_tokens(self, user: t.Any) -> None:
        model = self.get_model_class()
        sqla_session.execute(
            delete(model).where(model.user == user)
        )
        sqla_session.commit()

    def find_token(self, value: str) -> t.Optional[TokenProtocol]:
        model = self.get_model_class()
        return sqla_session.scalar(
            select(model).where(model.value == value)
        )

    def find_user_tokens(self, user: t.Any) -> t.Sequence[TokenProtocol]:
        model = self.get_model_class()
        return sqla_session.scalars(
            select(model).where(model.user == user)
                         .with_for_update()
        ).all()

    @getattr_or_implement
    def get_model_class(self) -> t.Type[t.Any]:
        return self.model_class

    def save_token(self, token_dict: t.Dict[str, t.Any]) -> None:
        token = self.get_model_class()(**token_dict)
        sqla_session.add(token)
        sqla_session.commit()


class ConfirmationToken(SQLATokenMixin, _ConfirmationToken):
    pass


class ConfirmationTokenSerializer(SQLATokenMixin, _ConfirmationTokenSerializer):
    pass
