from base_repository import BaseRepository
from ballot_box.modules import  api
from models import Contest, Decision, Opinion
import random
import uuid


class DemoRepository(BaseRepository ):
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

    @staticmethod
    def get_contest_decisions(contest):
        random.seed()
        decisions = []
        ballot_ids = [uuid.uuid4() for x in range(4)]
        for i in range(1000):
            decision = Decision(str(uuid.uuid4()), contest.id, ballot_ids[random.randint(1, 10000) % 4])

            if (random.randint(1, 10000) % 10) == 0:
                # # it non-official
                decision.authoritative = False
            else:
                decision.authoritative = True

            if (random.randint(1, 10000) % 6) == 0:
                # make it a write in
                write_in = "Write In {0}".format(random.randint(1, 4))
                decision.opinions.append(Opinion(opinion=1, write_in=write_in,
                                                 is_official=decision.authoritative, decision=decision))
            else:
                candidate = contest.contestants[random.randint(0, len(contest.contestants) - 1)]
                decision.opinions.append(Opinion(candidate, 1, is_official=decision.authoritative, decision=decision))
            decisions.append(decision)

        return decisions




