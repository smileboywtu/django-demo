# -*- coding: utf-8 -*-

# http://my.oschina.net/leejun2005/blog/126713
# utils for logger
# Created: 2016--27
# Copyright: (c) 2016<smileboywtu@gmail.com>

import logging
import logging.config


class LoggerSystem(object):
    """管理应用的应用级别的日志"""

    def __init__(self, config_file):

        logging.config.fileConfig(config_file)

        self.logger = logging.getLogger('root')
        self.logger.info('日志设置成功.')

        self._loggers = (
            'ms.basic', 'ms.task', 'ms.utils',
            'ms.environment', 'ms.version'
        )

    @property
    def loggers(self):
        """获取所有可用的logger"""
        return self._loggers

    def get_logger(self, name):
        "获取logger"
        if name not in self._loggers:
            self.logger.warning('logger: {0} does not exist.'.format(name))
            return None
        return logging.getLogger(name)


if __name__ == '__main__':
    logger = LoggerSystem('logger.cfg')
    print logger.loggers