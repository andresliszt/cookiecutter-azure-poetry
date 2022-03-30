# -*- coding: utf-8 -*-
"""Logger configuration."""

import logging.config
import uuid
from functools import wraps

import structlog

from {{cookiecutter.package_name}}.exc import EnvVarNotFound
from {{cookiecutter.package_name}}.settings import Settings
from {{cookiecutter.package_name}}.settings import LogDest
from {{cookiecutter.package_name}}.settings import LogFormatter

try:  # pragma: no cover
    import colorama  # pylint: disable=W0611,

    COLORAMA_INSTALLED = True

except ImportError:
    COLORAMA_INSTALLED = False


COMMON_CHAIN = [
    structlog.threadlocal.merge_threadlocal_context,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]


def _control_logging(
    settings: Settings,
):

    level = settings.LOG_LEVEL
    formatter = settings.LOG_FORMAT
    dest = settings.LOG_DESTINATION
    log_file = settings.LOG_PATH

    if formatter == LogFormatter.JSON.value:
        fmt = {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": COMMON_CHAIN,
        }
    elif formatter == LogFormatter.COLOR.value:

        fmt = {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=COLORAMA_INSTALLED),
            "foreign_pre_chain": COMMON_CHAIN,
        }

    else:
        raise NotImplementedError("Pydantic should not allow this.")  # pragma: no cover

    if dest == LogDest.CONSOLE.value:
        hndler = {
            "level": level,
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    elif dest == LogDest.FILE.value:

        if not log_file:
            raise EnvVarNotFound(env_var=f"{settings.Config.env_prefix}LOG_PATH")

        hndler = {
            "level": level,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(log_file),
            "formatter": "default",
            "maxBytes": 10e6,
            "backupCount": 100,
        }
        log_file.parent.mkdir(parents=True, exist_ok=True)
    else:
        raise NotImplementedError(
            "Pydantic should not allow this."
        )  # pragma: no cover

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"default": fmt},
            "handlers": {"default": hndler},
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": level,
                    "propagate": True,
                }
            },
        }
    )
    structlog.configure_once(
        processors=[
            structlog.stdlib.filter_by_level,
            *COMMON_CHAIN,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def configure_logging(
    name: str,
    settings: Settings,
    kidnap_loggers: bool = False,
):
    """logger configuration.

    :param name: logger name.
    :param settings: Setting class with logger information
            with configuration information.

    """

    if kidnap_loggers:
        _control_logging(settings)

    logger = structlog.get_logger(name)
    logger.trace = trace_using(logger)  # pylint: disable=assignment-from-none
    return logger


def trace_using(logger):
    """Factory of decorators to trace callables."""

    def real_decorator(func):  # pylint: disable=unused-variable
        """Decorate a callable for the args, kwargs and returns."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            uuid_ = str(uuid.uuid4())
            qual = func.__qualname__
            args_repr = ",".join(repr(a) for a in args)
            kwargs_repr = ",".join(k + "=" + repr(v) for k, v in kwargs.items())
            repr_ = f"{qual}({args_repr},{kwargs_repr})"
            with structlog.threadlocal.tmp_bind(
                logger,
                repr=repr_,
                uuid=uuid_,
                func=qual,
                args=args,
                kwargs=kwargs,
            ) as tmp_log:

                tmp_log.info(event="CALLED")
                retval = func(*args, **kwargs)
                tmp_log.info(event="RETURN", value=retval)
            return retval

        return wrapper

    return real_decorator
