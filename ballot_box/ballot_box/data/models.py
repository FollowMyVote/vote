import json
from itertools import ifilter
from ballot_box.modules import helpers
from sqlalchemy import Column, DateTime, Float, ForeignKey, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base as real_declarative_base



declarative_base = lambda cls: real_declarative_base(cls=cls)

@declarative_base
class Base(object):
    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """

    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]

    @property
    def column_items(self):
        return dict([ (c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.column_items)

    def to_json(self):
        return json.dumps(self.column_items)

metadata = Base.metadata

class DataItem(Base):
    __tablename__ = 'data_item'

    key = Column(Text, primary_key=True)
    value = Column(Text)
    data_type_key = Column(ForeignKey(u'data_type.key'), nullable=False, index=True)
    retired_date = Column(DateTime)
    deleted_date = Column(DateTime)
    sort = Column(Float, nullable=False, server_default=text("0"))
    data_type = relationship(u'DataType')

    children = relationship(
        u'DataItem',
        secondary='data_item_map',
        primaryjoin=u'DataItem.key == data_item_map.c.parent_data_key',
        secondaryjoin=u'DataItem.key == data_item_map.c.child_data_key'
    )

    parents = relationship(
        u'DataItem',
        secondary='data_item_map',
        primaryjoin=u'DataItem.key == data_item_map.c.child_data_key',
        secondaryjoin=u'DataItem.key == data_item_map.c.parent_data_key'
    )


t_data_item_map = Table(
    'data_item_map', metadata,
    Column('parent_data_key', ForeignKey(u'data_item.key'), primary_key=True, nullable=False),
    Column('child_data_key', ForeignKey(u'data_item.key'), primary_key=True, nullable=False)
)


class DataType(Base):
    __tablename__ = 'data_type'
    DATA_TYPE_CONTEST = "Contest"
    DATA_TYPE_CONTEST_GROUPING = "Contest Grouping"



    key = Column(Text, primary_key=True)
    retired_date = Column(DateTime)
    deleted_date = Column(DateTime)

class Opinion:
    """This class represents one opinion, the opinion number is usually 1"""

    def __init__(self, contestant=None, opinion=0, write_in=None, is_official=False, decision=None):

        self.contestant = contestant
        self.write_in = write_in
        self.opinion = opinion
        self.is_official = is_official
        self.decision = decision

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        d = self.__dict__.copy()
        d['contestant'] = self.contestant.to_dict() if self.contestant else None
        d['decision'] = self.decision.id if self.decision else None
        return d

    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.to_dict())

    def get_contestant(self):
        if self.contestant:
            return self.contestant.name
        else:
            return self.write_in

    @staticmethod
    def get_opinion_summary(opinions, contestants, decision_type, allow_write_in):
        """summarizes the opinions from the array of opinions"""
        summary = []
        total = 0

        if decision_type == Contest.DECISION_TYPE_VOTE_YES_NO:
            # we need to make sure that all opinions count so if there is a decision wihtout an opinion
            # we need to create a dummy no opinion since no opinion counts as a no
            total = len(opinions)
            yes_total = sum([o.opinion for o in opinions if o.opinion])
            no_total = total - yes_total
            summary.append({
                'name': "YES",
                'description' : '',
                'y': round(helpers.safe_division(yes_total , float(total)) * 100, 1),
                'total': yes_total})
            summary.append({
                'name': "NO",
                'description' : '',
                'y': round(helpers.safe_division(no_total, float(total)) * 100, 1),
                'total' :no_total})
        else:
            for c in contestants:
                contestant_total = sum([o.opinion for o in opinions if o.contestant and o.contestant.index == c.index])
                total += contestant_total
                summary.append({
                    'name': c.name,
                    'description' : c.description,
                    'y': contestant_total,
                    'total': contestant_total})

            if allow_write_in:
                other_total = sum([o.opinion for o in opinions if not o.contestant])
                total += other_total
                summary.append({
                    'name': "Other",
                    'description' : '',
                    'y': other_total,
                    'total': other_total})

        for s in summary:
            s['y'] = round(helpers.safe_division(s['total'], float(total)) * 100, 1)

        summary.sort(key=lambda x: x['name'])
        summary.sort(key=lambda x: x['total'], reverse=True)

        return summary

    @staticmethod
    def filter_opinion_summary(summaries, name):
        """this function filters a list of summaries by name

            if an object with name is not found then we will
            return a summary with the name with a 0.0 value
        """
        summary = {'name': name,
                   'y': 0,
                   'total': 0}
        if summaries:
            temp_summaries = [s for s in summaries if s['name'] == name]
            if temp_summaries:
                summary = temp_summaries[0]
        return summary


class Decision:
    """This class represents a decision by the voter for a contest it can contain multiple opinions"""

    def __init__(self, contest, d=None):

        if not contest:
            raise ValueError('contest must be set')

        if not d:
            d = {}

        self.id = d.get('decision_id')
        self.contest_id = d.get('contest_id')
        self.contest = contest
        self.ballot_id = d.get('ballot_id')
        self.write_in_names = d.get('write_in_names')
        self.authoritative = d.get('authoritative')
        self.timestamp = d.get('timestamp')
        self.decision_id = d.get('decision_id')
        self.voter_id = d.get('voter_id')
        self.voter_opinions = self.get_opinions(d.get('voter_opinions'), self.contest.decision_type)

    def get_opinions(self, opinions, decision_type):
        """get a set of opinions given the dictionary of opinions and the contestants, and the write ins """
        voter_opinions = []
        if not opinions:
            return []

        contestants = self.contest.contestants
        write_in_names = self.write_in_names

        ##not sure if the opinions are a a list of dicts or a list of lists
        ##once we get real data we will know for sure
        opinions_local = {}
        if type(opinions) is list:
            opinions_local = {x[0]: x[1] for x in opinions}
        else:
            opinions_local = opinions

        for key in opinions_local.keys():
            #the key values indicates the index of the contestant
            #if the index falls out of the range of the contestants
            #then it is a write in contestant

            if contestants and key < len(contestants):
                ##get the contestant with the matching index
                if decision_type == Contest.DECISION_TYPE_VOTE_YES_NO:
                    if opinions_local[key]:
                        contestant = Contestant({'name':'YES'})
                    else:
                        contestant = Contestant({'name':'YES'})
                else:
                    contestant = next(ifilter(lambda x: x.index == key, contestants), None)
                voter_opinions.append(Opinion(contestant, opinions_local[key], is_official=self.authoritative,
                                              decision=self))
            elif write_in_names and (key - len(contestants)) < len(write_in_names):
                #it is a write-in
                #
                # from the api documentation:
                #    The contestant ID is the index of the contestant in the contest structure . Write-in
                #     contestant IDs are the sum of the size of the list of official contestants and the
                #    index of the desired write-in contestant in the vector write_in_names, thus if there
                #    are 4 official contestants, the first contestant in write_in_names would be ID 4;
                #     the next would be ID 5, etc.
                write_in = write_in_names[key - len(contestants)]
                voter_opinions.append(Opinion(opinion=opinions_local[key], write_in=write_in,
                                              is_official=self.authoritative, decision=self))
        return voter_opinions

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        d = self.__dict__.copy()
        d.pop('contest', None)
        d['voter_opinions'] = [o.to_dict() for o in self.voter_opinions]
        d['timestamp'] = str(d['timestamp'])

        return d

    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.to_dict())


class Filter:
    """This class is for defining filters """

    def __init__(self, name, label=None, options=None, value='', filter_type='dropdown'):
        """initialize the filter
        name must be a valid attribute html attribute name            
        options should be a list of key value pairs the key will be the displayed option name
        """
        if not options:
            options = []
        self.name = name
        self.options = options
        self.value = value
        self.type = filter_type
        self.label = label
        if not label:
            self.label = name

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        return self.__dict__.copy()

    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.to_dict())

    def css_class(self):
        """return a css class based on name """
        return helpers.to_css_class(self.name)


class Contestant:
    """defines a contestant"""

    def __init__(self, d=None, index=0):
        """Initialize contestant"""
        if not d:
            d = {}
        self.name = d.get('name', '')
        self.description = d.get('description', '')
        self.index = index

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        return self.__dict__.copy()

    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.to_dict())


class Contest:
    """Defines a contest"""

    DECISION_TYPE_VOTE_ONE = 'vote one'
    DECISION_TYPE_VOTE_YES_NO = 'vote yes/no'
    DECISION_TYPE_VOTE_MANY = 'vote many'

    def __init__(self, contest_id='', d=None, data_item=None):

        """
        :param contest_id:
        :param d: dict
        :param data_item: DataItem

        """

        if not d:
            d = {}

        # tags is an array of arbitrary tags used to describe contests
        self.id = contest_id
        self.tags = d.get('tags', [])
        self.name = self.tag('name', '')
        self.decision_type = self.tag('decision type', '')
        self.description = d.get('description', '')
        self.allow_write_ins = bool(self.tag('write-in slots', False))
        self.decisions = []
        self.contestants = []
        self.group = self.tag('region')

        self.data_item = data_item if data_item else None
        """:type : DataItem"""


        if 'contestants' in d:
            self.contestants = [Contestant(c[1], c[0]) for c in enumerate(d['contestants'])]

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        return {
            'tags': self.tags,
            'description': self.description,
            'contestants': [c.to_dict() for c in self.contestants]}

    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.to_dict())

    def tag(self, name, default=None):
        """gets a tag value"""
        matches = [x for x in self.tags if x[0] == name]
        if matches:
            return matches[0][1]
        else:
            return default

    def tag_values(self):
        """ returns all tag values """
        return [x[1] for x in self.tags]

    def get_official_opinions(self):
        """gets all the official opinions for the contest"""
        return [o for o in self.get_all_opinions() if o.is_official]

    def get_all_opinions(self):
        """gets all opinions for the contest"""
        return [o for d in self.decisions for o in d.voter_opinions]

    @staticmethod
    def _get_relations(relations, data_type_key=None, predicate=None):
        """gets returns sorted non-deleted relations """
        return_val = []
        if data_type_key:
            return_val = [r for r in relations if not r.deleted_date and r.data_type_key == data_type_key]
        else:
            return_val = [r for r in relations if not r.deleted_date]

        if return_val and callable(predicate):
            return_val = [r for r in return_val if predicate(r)]

        if return_val:
            return_val.sort(key=lambda x: x.value)
            return_val.sort(key=lambda x: x.sort)

        return return_val


    def parents(self, data_type_key=None, predicate=None):
        """gets parents optionally by data type"""
        parents = []
        if self.data_item and self.data_item.parents:
            parents = self._get_relations(self.data_item.parents, data_type_key, predicate)

        return parents

    def children(self, data_type_key=None, predicate=None):
        """gets children optionally by data type"""
        children = []
        if self.data_item and self.data_item.children:
            children = self._get_relations(self.data_item.children, data_type_key, predicate)

        return children



    def search(self, search_text, contests_ids=[]):
        """Searches all the test in the contest for a partial match of the search text or list of contest_ids

        right now it cannot search both tesxt and id's it should be possible just time constraints for
        demo right now
        """

        if contests_ids:
            if any(x == self.id for x in contests_ids):
                #not in list of contest ids
                return True
            else:
                return False
        else:
            search = search_text.lower()

            return search in self.name or \
                   search in self.description or \
                   any(search in contestant.name.lower() for contestant in self.contestants) or \
                   any(search in contestant.description.lower() for contestant in self.contestants) or \
                   any(search in tag_value.lower() for tag_value in self.tag_values())

    def get_chart_description(self):
        """gets a description for the chart area """
        description = ""
        if self.decision_type == self.DECISION_TYPE_VOTE_YES_NO and self.contestants:
            if self.contestants[0].description:
                description += self.contestants[0].description

            if self.contestants[0].name:
                description += ', ' + self.contestants[0].name

        description = description.lstrip(', ')

        return description


    def get_list_description(self):
        """gets a description for the contest area """
        description = self.description


        if not description:
            if self.decision_type == self.DECISION_TYPE_VOTE_YES_NO and self.contestants:
                if self.contestants[0].description:
                    description += self.contestants[0].description

                if self.contestants[0].name:
                    description += ', ' + self.contestants[0].name
            else:
                description = ", ".join([c.name for  c in self.contestants])

        description = description.lstrip(', ')



        return description
       







