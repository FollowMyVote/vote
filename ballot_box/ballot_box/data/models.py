import json
from itertools import ifilter
from ballot_box.modules import helpers


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
                'y': round((yes_total / float(total)) * 100, 1),
                'total': yes_total})
            summary.append({
                'name': "NO",
                'y': round((no_total / float(total)) * 100, 1),
                'total' :no_total})
        else:
            for c in contestants:
                contestant_total = sum([o.opinion for o in opinions if o.contestant and o.contestant.index == c.index])
                total += contestant_total
                summary.append({
                    'name': c.name,
                    'y': contestant_total,
                    'total': contestant_total})

            if allow_write_in:
                other_total = sum([o.opinion for o in opinions if not o.contestant])
                total += other_total
                summary.append({
                    'name': "Other",
                    'y': other_total,
                    'total': other_total})

        for s in summary:
            s['y'] = round((s['total'] / float(total)) * 100, 1)

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
        self.voter_opinions = self.get_opinions(d.get('voter_opinions'))

    def get_opinions(self, opinions):
        """get a set of opinions given the dictionary of opinions and the contestants, and the write ins """
        voter_opinions = []
        if not opinions:
            return []

        contestants = self.contest.contestants
        write_in_names = self.write_in_names

        for key in opinions.keys():
            #the key values indicates the index of the contestant
            #if the index falls out of the range of the contestants
            #then it is a write in contestant

            if contestants and key < len(contestants):
                ##get the contestant with the matching index
                contestant = next(ifilter(lambda x: x.index == key, contestants), None)
                voter_opinions.append(Opinion(contestant, opinions[key], is_official=self.authoritative,
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
                voter_opinions.append(Opinion(opinion=opinions[key], write_in=write_in,
                                              is_official=self.authoritative, decision=self))
        return voter_opinions

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        d = self.__dict__.copy()
        d.pop('contest', None)
        d['voter_opinions'] = [o.to_dict() for o in self.voter_opinions]

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

    def __init__(self, contest_id='', d=None):
        """Initialize contest"""
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

    def search(self, search_text):
        """Searches all the test in the contest for a partial match of the search text"""

        search = search_text.lower()

        return search in self.name or \
               search in self.description or \
               any(search in contestant.name.lower() for contestant in self.contestants) or \
               any(search in contestant.description.lower() for contestant in self.contestants) or \
               any(search in tag_value.lower() for tag_value in self.tag_values())

       







