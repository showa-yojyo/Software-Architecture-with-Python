#!/usr/bin/env python
# Code Listing #9
"""

Custom loggers - simple logger object and a custom Logger class logging time spent in functions

"""


import logging
import logging.handlers
import time
from functools import partial


def create_logger(app_name, logfilename=None,
                  console=False, syslog=False):
    """ Build and return a custom logger. Accepts the application name,
    log filename, loglevel and console logging toggle and syslog toggle """

    log = logging.getLogger(app_name)
    log.setLevel(logging.DEBUG)
    # Add file handler
    if logfilename:
        # ファイルにも出力する
        log.addHandler(logging.FileHandler(logfilename))

    if syslog:
        # 特別なログファイルにも出力する
        log.addHandler(logging.handlers.SysLogHandler(
            address='/dev/log'))

    if console:
        # 標準出力または標準エラー出力にも出力する
        log.addHandler(logging.StreamHandler())

    # Add formatter
    for handle in log.handlers:
        # 2020-05-08 16:20:55 [00:00:00]: INFO     - xxxxx
        formatter = logging.Formatter(
            '%(asctime)s : %(levelname)-8s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        handle.setFormatter(formatter)

    return log


class LoggerWrapper:
    """ A wrapper class for logger objects with
    calculation of time spent in each step """

    def __init__(self, app_name, filename=None, level=logging.INFO, console=False):
        self.log = logging.getLogger(app_name)
        self.log.setLevel(level)

        # Add handlers
        if console:
            self.log.addHandler(logging.StreamHandler())

        if filename:
            self.log.addHandler(logging.FileHandler(filename))

        # Set formatting
        for handle in self.log.handlers:
            formatter = logging.Formatter(
                '%(asctime)s [%(timespent)s]: %(levelname)-8s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
            handle.setFormatter(formatter)
        for name in ('debug', 'info', 'warning', 'error', 'critical'):
            # Creating convenient wrappers by using functools
            func = partial(self._dolog, name)
            # Set on this class as methods
            setattr(self, name, func)

        # Mark timestamp
        self._markt = time.time()

    def _calc_time(self):
        """ Calculate time spent so far """

        tnow = time.time()
        tdiff = int(round(tnow - self._markt))

        # divmod() を時刻計算に応用するのは初めて見る
        hr, rem = divmod(tdiff, 3600)
        mins, sec = divmod(rem, 60)
        # Reset mark
        self._markt = tnow
        return '%.2d:%.2d:%.2d' % (hr, mins, sec)

    def _dolog(self, levelname, msg, *args, **kwargs):
        """ Generic method for logging at different levels """

        logfunc = getattr(self.log, levelname)
        return logfunc(msg, *args, extra={'timespent': self._calc_time()})


if __name__ == "__main__":
    log = LoggerWrapper('myapp', filename='myapp.log', console=True)
    log.info("Starting application...")
    log.info("Initializing objects.")
    time.sleep(14)
    log.info("Initialization complete.")
    log.info("Loading configuration and data ...")
    time.sleep(115)
    log.info('Loading complete. Listening for connections ...')
