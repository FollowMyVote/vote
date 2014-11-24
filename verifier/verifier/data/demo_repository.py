from base_repository import BaseRepository
from models import Identity, Ballot
import sqlalchemy
from verifier.modules import api
from sqlalchemy import create_engine, sql
from sqlalchemy.orm import scoped_session, sessionmaker, query


class DemoRepository(BaseRepository):
    """This is the repository implementation for the demo it will be a mix of api and database calls """

    def __init__(self, connection_string):

        self.engine = create_engine(connection_string, convert_unicode=True)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                     autoflush=False,
                                                      bind=self.engine))


        self.query = self.db_session.query



    def end_session(self):
        """provide any cleanup that needs to happen at the end of a database session """
        self.db_session.remove()

    @staticmethod
    def get_next_identity():
        """gets the next identity to be verified"""
        return Identity(api.take_next_request()['result'])

    @staticmethod
    def get_identity(identity_id):
        """gets the identity by id"""
        return Identity(api.verifier_peek_request(long(identity_id))['result'])

    @staticmethod
    def resolve_request(request_id, response):
        """ resolve a verification request

        :param request_id: the request id
        :param response: a VerificationResponse object
        """
        api.verifier_resolve_request(request_id, response.to_dict())

    @staticmethod
    def generate_test_requests(num_requests=5):
        """generates a number of test requests"""
        api.debug_create_test_request(num_requests)

    def get_ballots(self):
        """gets all ballots"""

        return self.db_session.query(Ballot).order_by(Ballot.ballot_name).all()








