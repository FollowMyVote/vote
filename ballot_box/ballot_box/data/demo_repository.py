from base_repository import BaseRepository
from ballot_box.modules import api
from models import Contest, Decision
from datetime import datetime
import random
import uuid


class DemoRepository(BaseRepository):
    """This is the repository implementation for the demo it will be a mix of api and database calls """

    @staticmethod
    def get_contest_by_id(contest_id):
        """returns a single contest by id"""
        result = api.ballot_get_contest_by_id(contest_id).get('result')
        if result:
            return Contest(contest_id, result)
        else:
            return None

    @classmethod
    def get_all_contests(cls):
        """returns a list of contest model objects"""
        contest_ids = api.ballot_list_contests(limit=10000).get('result')
        if contest_ids:
            return [cls.get_contest_by_id(c) for c in contest_ids]
        else:
            return []

    @classmethod
    def get_contest_decisions(cls, contest):
        return cls.get_test_contest_decisions(contest)

    @staticmethod
    def get_test_contest_decisions(contest):
        random.seed()
        decisions = []
        ballot_ids = [uuid.uuid4() for x in range(7)]
        for i in range(100):

            voter_opinions = {}
            write_in_names = []

            if contest.decision_type == contest.DECISION_TYPE_VOTE_YES_NO:
                voter_opinions[0] = random.randint(0, 1)
            else:
                if contest.allow_write_ins and (random.randint(1, 10000) % 25) == 0:
                    # # enter a write in
                    write_in_names.append("Write In {0}".format(random.randint(1, 4)))
                    voter_opinions[len(contest.contestants)] = 1
                else:
                    # #pick a candidate ar random
                    voter_opinions[random.randint(0, len(contest.contestants) - 1)] = 1

            decision = Decision(
                contest,
                {'decision_id': str(uuid.uuid4()),
                 'contest_id': contest.id,
                 'ballot_id': ballot_ids[random.randint(1, 10000) % 7],
                 'timestamp': datetime.now(),
                 'contest': contest,
                 'authoritative': True,
                 'voter_id': str(uuid.uuid4()),
                 'voter_opinions': voter_opinions,
                 'write_in_names': write_in_names})

            decisions.append(decision)

        return decisions




