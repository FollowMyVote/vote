import json
from ballot_box.modules import helpers


class Contestant:
    def __init__(self, dict = {}):
        """Initialize contestant"""
        self.name = dict.get('name', '')
        self.description = dict.get('description', '')
    
    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        return self.__dict__        
       
    def to_json(self):
        """convert object to json string"""
        return json.dumps(self.__dict__)


class Contest:
    def __init__(self, dict = {}):
        """Initialize contest"""

        #tags is an array of arbitary tags used to describe contests
        self.tags = dict.get('tags',[])
        self.name = self.tag('name', '')
        self.description = dict.get('description', '')
        

        if dict.has_key('contestants'):
            self.contestants = [Contestant(c)  for c in dict['contestants']]
            x = [Contestant(c)  for c in dict['contestants']]
            print(self.contestants[0])
        else:
            self.contestants = []

        
        

    
    
    def __repr__(self):
        return self.to_json()

    def to_dict(self):
        """convert object to dictionary"""
        dict = self.__dict__
        dict['contestants'] = [c.to_dict() for c in self.contestants]
        
          
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






