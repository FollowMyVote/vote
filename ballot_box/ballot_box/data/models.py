import json

from ballot_box.modules import helpers


class Opinion:
    """This class represents one opinion, the opinion number is usually 1"""
    def __init__(self, contestant=None, opinion= 0, write_in=None, is_official=False, decision=None):

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
    def get_opinion_summary(opinions, contestants):
        """summarizes the opinions from the array of opinions"""
        summary = []
        total = float(len(opinions))
        for c in contestants:
            summary.append([c.name, sum([o.opinion for o in opinions if o.contestant and o.contestant.index == c.index])])

        summary.append(['Other', sum([o.opinion for o in opinions if not o.contestant])])

        for s in summary:
            s[1] = round((s[1] / total) * 100, 1)

        summary.sort(key=lambda x: x[0])
        summary.sort(key=lambda x: x[1], reverse=True)

        return summary

    @staticmethod
    def filter_opinion_summary(summaries, name):
        """this function filters a list of summaries by name

            if an object with name is not found then we will
            return a summary with the name with a 0.0 value
        """
        summary = [name, 0]
        if summaries:
            temp_summaries = [s for s in summaries if s[0] == name]
            if temp_summaries:
                summary = temp_summaries[0]
        return summary



class Decision:
    """This class represents a decision by the voter for a contest it can contain multiple votes"""
    def __init__(self, decision_id=None, contest=None, ballot_id=None, write_ins=None, opinions=None,
                 authoritative=False, timestamp=None):
        if not opinions:
            opinions = []

        if not write_ins:
            write_ins = []

        self.id = decision_id
        self.contest = contest
        self.ballot_id = ballot_id
        self.write_ins = write_ins
        self.opinions = opinions
        self.authoritative = authoritative
        self.timestamp = timestamp

    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        d = self.__dict__.copy()
        d['opinions'] = [o.to_dict() for o in self.opinions]
        d['contest'] = self.contest.to_dict() if self.contest else None
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
            'name': self.name,
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
        return [o for d in self.decisions for o in d.opinions]

    def search(self, search_text):
        """Searches all the test in the contest for a partial match of the search text"""

        search = search_text.lower()

        return search in self.name or \
               search in self.description or \
               any(search in contestant.name.lower() for contestant in self.contestants) or \
               any(search in contestant.description.lower() for contestant in self.contestants) or \
               any(search in tag_value.lower() for tag_value in self.tag_values())

       







