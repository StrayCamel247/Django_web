#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __date__: 2020/06/05 17:00:11


import logging

import logging
 
 
 
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
 
#The background is set with 40 plus the number of the color, and the foreground with 30
 
#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
 
def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message
 
COLORS = {
    'WARNING': YELLOW,
    'INFO': BLUE,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': RED
}

LEVEL_COLORS = {
    logging.DEBUG: '\033[00;32m',  # GREEN
    logging.INFO: '\033[00;36m',  # CYAN
    logging.WARN: '\033[01;33m',  # BOLD YELLOW
    logging.ERROR: '\033[01;31m',  # BOLD RED
    logging.CRITICAL: '\033[01;31m',  # BOLD RED
}
class ColoredFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        # logging.Formatter.__init__(self, msg)
        self.use_color = True
        super().__init__(*args, **kwargs)
 
    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)
 
 
 
# Custom logger class with multiple destinations
# class ColoredLogger(logging.Logger):
#     FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
#     COLOR_FORMAT = formatter_message(FORMAT, True)
#     def __init__(self, name):
#         logging.Logger.__init__(self, name, logging.DEBUG)                
 
#         color_formatter = ColoredFormatter(self.COLOR_FORMAT)
 
#         console = logging.StreamHandler()
#         console.setFormatter(color_formatter)
 
#         self.addHandler(console)
#         return
 
# 
 
# logging.setLoggerClass(ColoredLogger)
# color_log = logging.getLogger(__name__)
# color_log.setLevel(logging.DEBUG)
 
# color_log.debug("test")
# color_log.info("test")
# color_log.warning("test")
# color_log.error("test")
# color_log.critical("test")

class ColorHandler(logging.StreamHandler):
    """Log handler that sets the 'color' key based on the level

    To use, include a '%(color)s' entry in the logging_context_format_string.
    There is also a '%(reset_color)s' key that can be used to manually reset
    the color within a log line.
    """
    LEVEL_COLORS = {
        logging.DEBUG: '\033[00;32m',  # GREEN
        logging.INFO: '\033[00;36m',  # CYAN
        logging.WARN: '\033[01;33m',  # BOLD YELLOW
        logging.ERROR: '\033[01;31m',  # BOLD RED
        logging.CRITICAL: '\033[01;31m',  # BOLD RED
    }

    def format(self, record):
        record.color = self.LEVEL_COLORS[record.levelno]
        record.reset_color = '\033[00m'
        return logging.StreamHandler.format(self, record) + record.reset_color
