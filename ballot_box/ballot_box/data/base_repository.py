import abc


class BaseRepository(object):
    """Provides a base class that concrete repositories must inherit from

    This is an attempt  separate the interface for getting the data from the
      implementation so we can swap it out later
    """
    __metaclass__ = abc.ABCMeta

    @classmethod
    @abc.abstractmethod
    def get_all_contests(cls):
        """returns a list of contest model objects"""
        return

    @classmethod
    @abc.abstractmethod
    def get_contest_decisions(cls, contest):
        """gets a list of contest """
        return

    @staticmethod
    @abc.abstractmethod
    def get_contest_by_id(contest_id):
        """returns a single contest by id"""
        return



