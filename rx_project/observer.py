
"""This class is used as interface for the Observer"""
from abc import ABCMeta, abstractmethod




class Observer(object):
    """Interface Observer for managing the error """
    __metaclass__ = ABCMeta



    @abstractmethod
    def log_error(self, *args, **kwargs):
        """Abstract method to manage errors """
        pass




    @abstractmethod
    def log_info(self, *args, **kwargs):
        """Abstract method to manage errors """
        pass
