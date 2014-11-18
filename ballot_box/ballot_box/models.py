import json

from ballot_box.modules import helpers


class Opinion:
    """This class represents one opinion, the opinion number is usually 1"""
    def __init__(self, contestant=None, opinion = 0, write_in=None, is_official=False, decision=None):

        self.contestant = contestant
        self.write_in = write_in
        self.opinion = opinion
        self.is_official = is_official
        self.decision = decision

    def get_contestant(self):
        if self.contestant:
            return self.contestant.name
        else:
            return self.write_in

class Decision:
    """This class represents a decision by the voter for a contest it can contain multiple votes"""
    def __init__(self, decision_id=None, contest_id=None, ballot_id=None, write_ins=None, opinions=None,
                 is_official=False):
        if not opinions:
            opinions = []
        if not write_ins:
            write_ins = []
        self.id = decision_id
        self.contest_id = contest_id
        self.ballot_id = ballot_id
        self.write_ins = write_ins
        self.opinions = opinions
        self.is_official = is_official


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

    def __init__(self, d=None):
        """Initialize contestant"""
        if not d:
            d = {}
        self.name = d.get('name', '')
        self.description = d.get('description', '')

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
        self.description = d.get('description', '')
        self.decisions = []



        if 'contestants' in d:
            self.contestants = [Contestant(c) for c in d['contestants']]

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

       







