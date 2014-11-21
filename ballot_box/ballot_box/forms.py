from modules import helpers
from ballot_box import db, cache
from data.models import Opinion, Contest

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

    def get_filtered_contests(self, contests):
        """ Filters contests by the form filters """
        if not contests:
            return []

        for f in self.filters:
            if f.value:
                contests = [c for c in contests if c.tag(f.name) == f.value]

            if not contests:
                break

        if contests and self.search:
            contests = [c for c in contests if c.search(self.search)]

        return contests


    def set_form_contest(self):
        """sets the contest data """
        if self.contest_id:
            try:
                self.contest = db.get_contest_by_id(self.contest_id)
            except:
                helpers.log().error("Contest ID: {0} not found".format(self.contest_id))
                self.contest_id = ''
        elif self.contests:
            self.contest_id = self.contests[0].id
            self.contest = self.contests[0]

        if self.contest:

            def get_decisions():
                return db.get_contest_decisions(self.contest)

            self.contest.decisions =  helpers.get_cache(cache, 'all_decisions_{0}'.format(self.contest.id),
                                                        get_decisions, 3600)
            self.all_opinions = self.contest.get_all_opinions()
            self.official_opinions = self.contest.get_official_opinions()
            self.all_opinion_summary = Opinion.get_opinion_summary(self.all_opinions, self.contest.contestants)
            self.official_opinion_summary = Opinion.get_opinion_summary(self.official_opinions, self.contest.contestants)
        else:
            self.all_opinion_summary = []
            self.official_opinion_summary = []


            


