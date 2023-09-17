#!/usr/bin/env python

# dogdaemon.py: monitor KDLP ORBIT for service degradation
#
# Author: Joel Savitz <joelsavitz@gmail.com>

from time import sleep
from datetime import datetime
from loguru import logger
from requests import get
from sys import stderr
from os import path, getcwd
from signal import signal, SIGINT
from socket import gethostname

from config import DOGDAEMON_WATCHDOG_INTERVAL_SECS as INTERVAL_SECS
from config import DOGDAEMON_WATCHDOG_DOGLOG_FILENAME as DOGLOG_FILENAME

def send_urgent_alert(message):
    r = get('http://localhost:6060', params={'msg': message })
    logger.info(f'alert delivery server: {r.text}')

class ErrorState:
    _e = False

    @classmethod
    def ok(cls):
        # if we just discovered the server to be up,
        # send an urgent alert
        if cls._e:
            send_urgent_alert(f'{datetime.utcnow()}@{gethostname()} ORBIT FOUND TO BE OPERATIONAL')
            cls._e = False
            logger.warning('(NEWS): Discovered orbit to be online')

    @classmethod
    def error(cls):
        # if we just discovered the server to be down,
        # send an urgent alert
        if not cls._e:
            send_urgent_alert(f'{datetime.utcnow()}@{gethostname()} ORBIT OUTTAGE DETECTED!!!')
            cls._e = True
            logger.warning('(NEWS): Discovered orbit to be offline')

def watchdog():
    r = get('https://kdlp.underground.software')
    logger.info('GET https://kdlp.underground.software HTTP/1.1')
    if r.status_code != 200:
        logger.error(f'CODE [{r.status_code: ^3}]: KDLP ORBIT IS DOWN!')
        ErrorState.error()
    else:
        logger.success('200 OK: ORBIT is operational')
        ErrorState.ok()

class DogLog:
    logfile=None

    @classmethod
    def open(cls, mode):
        cls.logfile = open(DOGLOG_FILENAME, mode)
        logger.info(f'writing (mode {mode}) to logfile {getcwd()}/{DOGLOG_FILENAME}')

    @classmethod
    def write(cls, bone):
        print(bone, file=stderr)

        if cls.logfile is not None:
            print(bone, file=cls.logfile)

def down_dog(signum, frame):
    logger.info('SIGINT received: stop watchdog daemon')
    exit(0)

def up_dog():
    logger.remove(0)
    logger.add(DogLog,
            format = "<yellow>[</yellow><blue>{time}</blue> <magenta>|</magenta> <red>{level: <8}</red><yellow>]</yellow><magenta>:</magenta> <green>{message}</green>",
            colorize=True)
    # register cleanup handler to run on Ctrl-C
    signal(SIGINT, down_dog)

    ret = None
    # if it exists, append to it instead of zeroing
    if path.isfile(DOGLOG_FILENAME):
        ret = lambda: logger.info('existing logfile found, setting mode to append')
        DogLog.open('a')
    else:
        ret = lambda : logger.info('existing logfile found, setting mode to append')
        DogLog.open('w')

    # return a callable that logs output from up_dog so we can print it after:
    #   a) the logfile is open
    #   b) the start message(s)
    return ret

def main():
    I = up_dog()

    mins = '{:.2f}'.format(INTERVAL_SECS / 60.0)
    logger.info(f'start watchdog daemon with {mins} minute interval')

    I()

    while True:
        watchdog()
        sleep(INTERVAL_SECS)

if __name__ == "__main__":
    main()
