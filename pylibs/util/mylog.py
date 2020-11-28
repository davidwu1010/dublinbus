#!/usr/bin/env python
#coding=utf-8

import os
import time
import logging
from logging import handlers


class Logger(object):

    def __init__(self, log_name, log_dir=os.getcwd(), clevel=logging.DEBUG, Flevel = logging.DEBUG):
        self.log_dir = log_dir
        self.init_log_dir()
        log_name = '{}_{}.log'.format(log_name, time.strftime('%Y-%m-%d',time.localtime(time.time())))
        log_path = os.path.join(self.log_dir, log_name)

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # set CMD log
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # set file log
        fh = handlers.TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=30)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        if not self.logger.handlers:
            self.logger.addHandler(sh)
            self.logger.addHandler(fh)
        # print log
        self.logger.info("{} start log...".format(log_name))
    
    def init_log_dir(self):
        try:
            os.makedirs(self.log_dir)
        except:
            pass

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


def _test_log():
    logtest = Logger('test',logging.ERROR,logging.DEBUG)
    logtest.debug('debug msg')
    logtest.info('info msg')
    logtest.war('warning msg')
    logtest.error('error msg')
    logtest.cri('critical msg')


if __name__ =='__main__':
    _test_log()