from base_repository import BaseRepository
from models import Identity, Ballot, Voter
from verifier import log
from verifier.modules import api
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import scoped_session, sessionmaker, Query


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
        """gets the identity by id does not change status"""
        response = api.verifier_peek_request(long(identity_id))
        if 'result' in response:
            return Identity(response['result'])
        else:
            log.error(response)
            return None

    @staticmethod
    def get_identity_for_processing(identity_id):
        """gets the identity for processing sets status to in processing"""
        response = api.verifier_take_pending_request(long(identity_id))
        if 'result' in response:
            return Identity(response['result'])
        else:
            log.error(response)
            return None

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
        return self.query(Ballot).order_by(Ballot.ballot_name).all()


    def log_query(self, q):
        """
        Log Query
        :param q: Query
        """
        query_str =str(q.statement.compile(dialect=sqlite.dialect()))

        log.debug(query_str)


    def search_voters(self, search_terms, limit=5):
        """searches for voters for voters matching the search terms provided """
        q = self.query(Voter)

        for t in search_terms:
            term = t + '%'
            term_full = '%{0}%'.format(t)

            q = q.filter(
                and_(
                    or_(Voter.first_name.like(term),
                    Voter.last_name.like(term),
                    Voter.middle_name.like(term),
                    Voter.suffix.like(term),
                    Voter.address_1.like(term_full),
                    Voter.birth_date.like(term),
                    Voter.city.like(term),
                    Voter.zip.like(term),
                    Voter.state.like(term))))


        q = q.order_by(Voter.last_name, Voter.first_name, Voter.middle_name)
        if limit:
            q = q.limit(limit)

        self.log_query(q)
        return q.all()


    def get_identities(self, status=Identity.STATUS_AWAITING_PROCESSING):
        """gets requests by status"""

        response = api.verifier_list_requests(status)
        results = []
        if 'result' in response:
            results = [Identity(r) for r in response['result']]

        return results








