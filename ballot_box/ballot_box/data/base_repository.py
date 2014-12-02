import abc


class BaseRepository(object):
    """Provides a base class that concrete repositories must inherit from

    This is an attempt  separate the interface for getting the data from the
      implementation so we can swap it out later
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def end_session(self):
        """provide any cleanup that needs to happen at the end of a database session """
        return

    @abc.abstractmethod
    def insert(self, item):
        """inserts a data item"""
        return

    def delete(self, item):
        """deletes a data item"""
        return

    @abc.abstractmethod
    def commit(self):
        """commits changes to the database """
        return

    @abc.abstractmethod
    def rollback(self):
        """rolls back changes to the database """
        return

    @abc.abstractmethod
    def get_item(self, key, default=None):
        """gets a data item by key, return the default if it is not exiting default can be callable """
        return
    @abc.abstractmethod
    def get_data_type(self, key, default=None):
        """gets a data type by key, return the default if it is not exiting
        default can be callable """
        return

    @abc.abstractmethod
    def get_items_by_value(self, value, data_type_key):
        """gets items by value and type """

    @abc.abstractmethod
    def get_items_by_data_type(self, data_type_key):
        """gets all items of a particular data type """
        return


    @abc.abstractmethod
    def get_contest(self, contest_id):
        """returns a single contest by id"""
        return

    @abc.abstractmethod
    def get_all_contests(self):
        """returns a list of contest model objects"""
        return

    @abc.abstractmethod
    def get_contest_decisions(cls, contest):
        """gets a list of contest """
        return






