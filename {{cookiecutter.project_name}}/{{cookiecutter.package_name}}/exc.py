# -*- coding: utf-8 -*-
"""Exceptions handling."""

import abc
from contextlib import contextmanager
from typing import Any
from typing import Generator
from typing import Type
from typing import Union


class ErrorMixin(abc.ABC, BaseException):
    """Base class for custom errors and exceptions.
    Example:
        >>> class MyError(ErrorMixin):
                msg_template = "Value ``{value}`` could not be found"
        >>> raise MyError(value="can't touch this")
        (...)
        MyError: Value `can't touch this` could not be found

    """

    @property
    @abc.abstractmethod
    def msg_template(self) -> str:
        """Un template para imprimir cuando una excepción es levantada.
        Example:
            "Value ``{value}`` is not found "

        """

    def __init__(self, **ctx: Any) -> None:
        self.ctx = ctx
        super().__init__()

    def __str__(self) -> str:
        txt = self.msg_template
        for name, value in self.ctx.items():
            txt = txt.replace("{" + name + "}", str(value))
        txt = txt.replace("`{", "").replace("}`", "")
        return txt


@contextmanager
def change_exception(
    raise_exc: Union[ErrorMixin, Type[ErrorMixin]],
    *except_types: Type[BaseException],
) -> Generator[None, None, None]:
    """Context Manager para remplazar excepciones por propias.
    See also:
        :func:`pydantic.utils.change_exception`

    """
    try:
        yield
    except except_types as exception:
        raise raise_exc from exception  # type: ignore


class EnvVarNotFound(ErrorMixin, NameError):
    """Raise this when a table name has not been found."""

    msg_template = "Enviroment variable `{env_var}` can't be found"
