import abc


class BaseRepository(object):
    """Provides a base class that concrete respositories must inherit from

    I am trying to seperate the data model objects
    """
    __metaclass__  = abc.ABCMeta

    @staticmethod
    @abc.abstractmethod
    def get_all_contests():
        """returns a list of contest model objects"""
        return

    @staticmethod
    @abc.abstractmethod
    def get_contest_decisions():
        """gets a list of contest """
        return



