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

    @staticmethod
    @abc.abstractmethod
    def get_next_identity():
        """gets the next identity to be verified"""
        return

    @staticmethod
    @abc.abstractmethod
    def get_identity(identity_id):
        """gets the identity by id"""
        return
    @staticmethod
    @abc.abstractmethod
    def resolve_request(request_id, response):
        """ resolve a verification request

        :param request_id: the request id
        :param response: VerificationResponse object
        """
        return

    @staticmethod
    @abc.abstractmethod
    def generate_test_requests(num_requests=5):
        """generates a number of test requests"""
        return


    @abc.abstractmethod
    def get_ballots(self):
        """gets all ballots"""
        return

    @abc.abstractmethod
    def search_voters(self, search_terms):
        """searches for voters for voters matching the search terms provided """
        return