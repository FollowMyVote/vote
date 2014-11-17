import json
import re
from ballot_box.modules import helpers

class Filter:
    def __init__(self, name, label = None, options = [], value='', type='dropdown', ):
        """initialize the filter
        name must be a valid attribute html attribute name            
        options should be a list of key value pairs the key will be the displayed option name
        """
        self.name = name
        self.options = options
        self.value = value
        self.type = type
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
    def __init__(self, dict = {}):
        """Initialize contestant"""
        self.name = dict.get('name', '')
        self.description = dict.get('description', '')
    
    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        return self.__dict__.copy()       
       
    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.to_dict())


class Contest:
    def __init__(self, id='', dict = {}):
        """Initialize contest"""

        #tags is an array of arbitary tags used to describe contests
        self.id = id
        self.tags = dict.get('tags',[])
        self.name = self.tag('name', '')
        self.description = dict.get('description', '')
        self.contestants = []

        if dict.has_key('contestants'):
            self.contestants = [Contestant(c)  for c in dict['contestants']]
        
    
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
        

    def tag(self, name, default = None):
        """gets a tag value"""
        matches = [x for x in self.tags if x[0] == name]
        if (matches):
            return matches[0][1]
        else:
            return default;

    def tag_values(self):
        """ returns all tag values """
        return [x[1] for x in self.tags]

    def search(self, search_text):
        """Searches all the test in the contest for a partial match of the search text"""
           
        
        search = search_text.lower()

        return search in self.name or \
               search in self.description or \
               any( search in contestant.name.lower() for contestant in self.contestants) or \
               any( search in contestant.description.lower() for contestant in self.contestants) or \
               any( search in tag_value.lower() for tag_value in self.tag_values())

       







