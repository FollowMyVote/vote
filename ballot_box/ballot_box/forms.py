from ballot_box.modules import helpers


class BallotBoxForm():
    """form for the ballot box main page"""
    # noinspection PyShadowingNames
    def __init__(self, request, filters):
        """Initialize the ballot box form data
        
        filters are a list of type filter         
        """
        self.filters = filters

        for x in request.values.keys():
            form_filter = helpers.get_first([f for f in self.filters if f.name == x])
            if form_filter:
                form_filter.value = request.values[x]

        self.contest_id = request.values.get('contest_id', '')

        self.search = request.values.get('search', '')

        self.contests = []
        self.all_opinions = []
        self.official_opinions = []
        self.contest = None

            


