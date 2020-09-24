#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/06/05 16:59:25


import logging
import logging.config
import logging.handlers
import os
import sys

import six
import inspect
from six import moves

from .handlers import ColorHandler
from .formatters import New_Format

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

try:
    import syslog
except ImportError:
    syslog = None


def _get_binary_name():
    return os.path.basename(inspect.stack()[-1][1])


def _get_log_file_path(conf, binary=None):
    logfile = conf["LOG_FILE"]
    logdir = conf["LOG_DIR"]

    if logfile and not logdir:
        return logfile

    if logfile and logdir:
        return os.path.join(logdir, logfile)

    if logdir:
        binary = binary or _get_binary_name()
        return '%s.log' % (os.path.join(logdir, binary),)

    return None


class LogConfigError(Exception):
    message = 'Error loading logging config %(log_config)s: %(err_msg)s'

    def __init__(self, log_config, err_msg):
        self.log_config = log_config
        self.err_msg = err_msg

    def __str__(self):
        return self.message % dict(log_config=self.log_config,
                                   err_msg=self.err_msg)


def _iter_loggers():
    """Iterate on existing loggers."""

    # Sadly, Logger.manager and Manager.loggerDict are not documented,
    # but there is no logging public function to iterate on all loggers.

    # The root logger is not part of loggerDict.
    yield logging.getLogger()

    manager = logging.Logger.manager
    for logger in manager.loggerDict.values():
        if isinstance(logger, logging.PlaceHolder):
            continue
        yield logger


def _load_log_config(log_config_append):
    try:
        if not hasattr(_load_log_config, "old_time"):
            _load_log_config.old_time = 0
        new_time = os.path.getmtime(log_config_append)
        if _load_log_config.old_time != new_time:
            # Reset all existing loggers before reloading config as fileConfig
            # does not reset non-child loggers.
            for logger in _iter_loggers():
                logger.level = logging.NOTSET
                logger.handlers = []
                logger.propagate = 1
            logging.config.fileConfig(log_config_append,
                                      disable_existing_loggers=False)
            _load_log_config.old_time = new_time
    except (moves.configparser.Error, KeyError, os.error) as exc:
        raise LogConfigError(log_config_append, six.text_type(exc))


def _create_logging_excepthook():
    def logging_excepthook(exc_type, value, tb):
        extra = {'exc_info': (exc_type, value, tb)}
        logging.getLogger().critical('Unhandled error', **extra)

    return logging_excepthook


def _setup_logging_from_conf(conf, app_name=None):
    log_root = logging.getLogger()
    log_root.setLevel(conf["LOG_LEVEL"])

    # Remove all handlers
    for handler in list(log_root.handlers):
        log_root.removeHandler(handler)

    logpath = _get_log_file_path(conf, app_name)
    if logpath:
        # filelog = logging.handlers.\
        #     RotatingFileHandler(logpath,
        #                         maxBytes=conf['LOG_FILE_MAX_BYTES'],
        #                         backupCount=conf['LOG_FILE_BAKUP_COUNT'],
        #                         encoding="utf-8")
        filelog = logging.handlers. \
            TimedRotatingFileHandler(logpath,
                                     when=conf["LOG_WHEN"],
                                     backupCount=conf['LOG_FILE_BAKUP_COUNT'],
                                     encoding="utf-8"
                                     )
        log_root.addHandler(filelog)

    if conf["LOG_USE_STDERR"]:
        streamlog = ColorHandler()
        log_root.addHandler(streamlog)

    for handler in log_root.handlers:
        handler.setFormatter(New_Format(conf["LOG_FORMAT"],
                                      conf['LOG_DATE_FORMAT']))

    for pair in conf["LOG_DEFAULT_LEVELS"]:
        mod, _sep, level_name = pair.partition('=')
        logger = logging.getLogger(mod)
        numeric_level = None
        try:
            # NOTE(harlowja): integer's are valid level names, and for some
            # libraries they have a lower level than DEBUG that is typically
            # defined at level 5, so to make that accessible, try to convert
            # this to a integer, and if not keep the original...
            numeric_level = int(level_name)
        except ValueError:  # nosec
            pass
        if numeric_level is not None:
            logger.setLevel(numeric_level)
        else:
            logger.setLevel(level_name)


class New_Log(object):
    def __init__(self, app_name=None):
        self.app_name = app_name

    def init_app(self, app):
        """Setup logging for the current application."""
        conf = app.config

        format = '%(color)s%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        datefmt = '''%Y-%m-%d %H:%M:%S'''
        Log_default_levels = ['sqlalchemy=INFO', 'stevedore=INFO', 'werkzeug=INFO', ]

        conf.setdefault("LOG_CONFIG_APPEND", None)
        conf.setdefault("LOG_LEVEL", "INFO")
        conf.setdefault("LOG_DEFAULT_LEVELS", Log_default_levels)
        conf.setdefault("LOG_USE_STDERR", True)
        conf.setdefault("LOG_FORMAT", format)
        conf.setdefault("LOG_DATE_FORMAT", datefmt)

        conf.setdefault("LOG_FILE", None)
        conf.setdefault("LOG_DIR", "logs")
        # conf.setdefault("LOG_FILE_MAX_BYTES", 1024 * 1024 * 10)
        conf.setdefault("LOG_FILE_BAKUP_COUNT", 14)
        conf.setdefault("LOG_WHEN", "D")

        if conf["LOG_CONFIG_APPEND"]:
            _load_log_config(conf.log_config_append)
        else:
            _setup_logging_from_conf(conf, self.app_name)
        sys.excepthook = _create_logging_excepthook()
