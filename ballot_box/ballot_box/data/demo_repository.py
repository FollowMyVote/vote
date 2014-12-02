import random
import uuid
import json
from base_repository import BaseRepository
from ballot_box import log
from ballot_box.modules import api
from models import Contest, Decision, DataItem, DataType
from datetime import datetime
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


    @staticmethod
    def log_query(q):
        """Log Query
        :param q: Query
        """
        statement = q.statement.compile(dialect=sqlite.dialect())
        if statement.params:
            query_str = '{0}\n{1}'.format(statement, statement.params)
        else:
            query_str = str(statement)

        log.debug(query_str)

    def end_session(self):
        """provide any cleanup that needs to happen at the end of a database session """
        self.db_session.remove()

    def insert(self, item):
        """inserts a data item"""
        self.db_session.add(item)

    def delete(self, item):
        """deletes a data item"""
        self.db_session.delete(item)

    def commit(self):
        """commits changes to the database """
        self.db_session.commit()

    def rollback(self):
        """rolls back changes to the database """
        self.db_session.rollback()

    def get_item(self, key, default=None):
        """gets a data item by key, return the default if it is not exiting
        default can be callable """

        q = self.query(DataItem).filter(DataItem.key == key)
        self.log_query(q)

        data = q.first()

        if data:
            return data
        else:
            if callable(default):
                return default()
            else:
                return default

    def get_items_by_value(self, value, data_type_key):
        """gets items by value and type"""

        q = self.query(DataItem)\
            .filter(DataItem.data_type_key == data_type_key, DataItem.value == value)\
            .order_by(DataItem.sort)


        self.log_query(q)

        return q.all()




    def get_items_by_data_type(self, data_type_key):
        """gets all items of a particular data type """
        q = self.query(DataItem) \
            .filter(DataItem.data_type_key == data_type_key) \
            .order_by(DataItem.sort)
        self.log_query(q)
        return q.all()

    def get_data_type(self, key, default=None):
        """gets a data type by key, return the default if it is not exiting
        default can be callable """

        q = self.query(DataType).filter(DataType.key == key)
        self.log_query(q)
        data = q.first()

        if data:
            return data
        else:
            if callable(default):
                return default()
            else:
                return default


    def get_contest(self, contest_id):
        """returns a single contest by id"""
        item = self.get_item(contest_id)
        if item:
            return Contest(json.loads(item.value))
        else:
            return None


    def get_all_contests(self):
        """returns all contests """
        q = self.query(DataItem) \
            .filter(DataItem.data_type_key == DataType.DATA_TYPE_CONTEST) \
            .order_by(DataItem.sort)

        self.log_query(q)
        return q.all()


    def get_contest_decisions(self, contest):
        return self.get_test_contest_decisions(contest)

    @staticmethod
    def _api_get_contest_by_id(contest_id):
        """returns a single contest by id
        """
        result = api.ballot_get_contest_by_id(contest_id).get('result')
        if result:
            return Contest(contest_id, result)
        else:
            return None

    @classmethod
    def _api_get_all_contests(cls):
        """returns a list of contest model objects

        the reason we are loading them in a loop instead of the batch method is because
        the batch method does not return id's hopefully this is something we can
        fix in the future

        """
        contest_ids = api.ballot_list_contests(limit=10000).get('result')
        if contest_ids:
            return [cls._api_get_contest_by_id(c) for c in contest_ids]
        else:
            return []

    def _create_contest_group(self, group_name):
        """creates  a contest group"""
        key = str(uuid.uuid4())
        group = DataItem(key=key, value=group_name, data_type_key=DataType.DATA_TYPE_CONTEST_GROUPING)
        self.insert(group)
        return group

    def _get_contest_group(self, group_name):
        """gets a contest group creates it if it doesnt exist """
        group = self.query(DataItem).filter(DataItem.value == group_name).first()
        if not group:
            group = self._create_contest_group(group_name)

        return group

    @staticmethod
    def _get_test_contest_decisions(contest):
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

    _counties = {
        "Alameda": [13, 15, 17],
        "Alpine": [4],
        "Amador": [4],
        "Butte": [1],
        "Calaveras": [4],
        "Colusa": [3],
        "Contra Costa": [5, 9, 11, 15],
        "Del Norte": [2],
        "El Dorado": [4],
        "Fresno": [4, 16, 21, 22],
        "Glenn": [1, 3],
        "Humboldt": [2],
        "Imperial": [51],
        "Inyo": [8],
        "Kern": [21, 23],
        "Kings": [21],
        "Lake": [3, 5],
        "Lassen": [1],
        "Los Angeles": [23, 25, 26, 17, 28, 29, 30, 32, 33, 34, 35, 37, 38, 39, 40, 43, 44, 47],
        "Madera": [4, 16],
        "Marin": [2],
        "Mariposa": [4],
        "Mendocino": [2],
        "Merced": [16],
        "Modoc": [1],
        "Mono": [8],
        "Monterey": [20],
        "Napa": [5],
        "Nevada": [1, 4],
        "Orange": [38, 39, 45, 46, 47, 48, 49],
        "Placer": [1, 4],
        "Plumas": [1],
        "Riverside": [36, 41, 42, 50],
        "Sacramento": [3, 6, 7, 9],
        "San Benito": [20],
        "San Bernardino": [8, 27, 31, 35, 39],
        "San Diego": [49, 50, 51, 52, 53],
        "San Francisco": [12, 13, 14],
        "San Joaquin": [9, 10],
        "San Luis Obispo": [24],
        "San Mateo": [14, 18],
        "Santa Barbara": [24],
        "Santa Clara": [17, 18, 19, 20],
        "Santa Cruz": [18, 20],
        "Shasta": [1],
        "Sierra": [1],
        "Siskiyou": [1],
        "Solano": [3, 5],
        "Sonoma": [2, 5],
        "Stanislaus": [10],
        "Sutter": [3],
        "Tehama": [1],
        "Trinity": [2],
        "Tulare": [21, 22, 23],
        "Tuolumne": [4],
        "Ventura": [24, 25, 26, 30],
        "Yolo": [3, 6],
        "Yuba": [3]}


    def _debug_load_demo_contests(self):
        """loads the contests from the api into the db, if the contest exists it will update
        otherwise it will create the contest

        this is just for the demo site, this is just an example of loading data
        """

        contests = self._api_get_all_contests()
        groups = {}

        election = DataItem(key=str(uuid.uuid4()), value='2014 Mid-Term Election',
                            data_type_key='Election', sort=0)

        self.insert(election)

        districts = {}
        def get_post_fix(i):
            if i == 1:
                return 'st'
            elif i == 2:
                return 'nd'
            elif i == 3:
                return 'rd'
            else:
                return 'th'

        for i in range(1, 54):
            district_text = '{0}{1}'.format(i, get_post_fix(i))
            items = self.get_items_by_value(district_text, 'Congressional District')
            if items:
                district = items[0]
            else:
                district = DataItem(key=str(uuid.uuid4()), value= district_text,
                                data_type_key='Congressional District', sort=1)
                self.insert(district)

            district.parents.append(election)
            districts[i] = district

        sort = 0
        for key in self._counties.keys():
            sort += 1
            items = self.get_items_by_value(key, 'County')

            if items:
                county_data = items[0]
            else:
                county_data = DataItem(key=str(uuid.uuid4()), value=key,
                                       data_type_key='County', sort=sort)
                self.insert(county_data)

            for d in self._counties[key]:
                county_data.parents.append(districts[d])

        for c in contests:
            item = self.get_item(c.id)
            group_name = c.tag('region', 'Other')

            group = groups.get(group_name)
            if not group:
                group = self._get_contest_group(group_name)
                groups[group_name] = group

            if item:
                item.value = c.to_json()
            else:
                item = DataItem(key=c.id, value=c.to_json(), data_type_key=DataType.DATA_TYPE_CONTEST)
                self.insert(item)

            item.parents.append(group)
            item.parents.append(election)









