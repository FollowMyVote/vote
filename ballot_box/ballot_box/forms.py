from  flask import request
from ballot_box.modules import helpers
class BallotBoxForm():
    def __init__(self, request, filters):
        """Initialize the ballot box form data
        
        filters are a list of type filter         
        """
        self.filters = filters

        for x in request.values.keys():
            filter = helpers.get_first([f for f in self.filters if f.name == x])
            if filter:
                filter.value = request.values[x]

        self.contest_id = request.values.get('contest_id', '')

        self.search = request.values.get('search', '')

        self.contests = []        
            


