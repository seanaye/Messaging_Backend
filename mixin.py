import logging

class LoggerMixin(object):
    """Mixin for adding logger to a class"""
    @property
    def logger(self):
        name = '.'.join([
            self.__module__,
            self.__class__.__name__
        ])
        return logging.getLogger(name)
