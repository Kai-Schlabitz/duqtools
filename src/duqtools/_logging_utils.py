from __future__ import annotations

import logging

import click


class TermEscapeCodeFormatter(logging.Formatter):
    """A class to strip the escape codes from the."""

    def format(self, record):
        record.msg = click.unstyle(record.msg)
        return super().format(record)


class LoggingContext:
    """Context manager to Temporarily change logging configuration.

    From https://docs.python.org/3/howto/logging-cookbook.html

    Parameters
    ----------
    logger : None, optional
        Logging instance to change, defaults to root logger.
    level : None, optional
        New log level, i.e. `logging.CRITICAL`.
    handler : None, optional
        Log handler to use.
    close : bool, optional
        Whether to close the handler after use.
    """

    def __init__(self, logger=None, level=None, handler=None, close=True):
        if not logger:
            logger = logging.getLogger()
        self.logger = logger
        self.level = level
        self.handler = handler
        self.close = close

    def __enter__(self):
        if self.level is not None:
            self.old_level = self.logger.level
            self.logger.setLevel(self.level)
        if self.handler:
            self.logger.addHandler(self.handler)

    def __exit__(self, et, ev, tb):
        if self.level is not None:
            self.logger.setLevel(self.old_level)
        if self.handler:
            self.logger.removeHandler(self.handler)
        if self.handler and self.close:
            self.handler.close()


# Logger to use in duqtools
duqlog_screen = logging.getLogger("screen")  # logger to log to the screen (and the log)


def initialize_duqlog_screen():
    # Logger for stdout
    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter("%(message)s"))
    duqlog_screen.addHandler(stream)
