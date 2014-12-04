from ballot_box.modules import helpers
from ballot_box import db, cache, log
from ballot_box.data.models import Opinion, Contest, DataType

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
        self.all_opinion_summary = []
        self.official_opinion_summary = []
        self.contest = None
        self.search_results = request.values.get('search_results', '')

    def get_contest_id_filters(self):
        """this returns a list of contest ids to filter on"""

        contest_ids = []
        if len(self.search) > 30:
            #it could be a voter
            contest_ids = db.get_voter_contest_ids(self.search)
            if contest_ids:
                self.search_results = self.search

        return contest_ids





    def get_filtered_contests(self, contests):
        """ Filters contests by the form filters """
        if not contests:
            return []

        # for f in self.filters:
        #     if f.value:
        #         contests = [c for c in contests if c.tag(f.name) == f.value]
        #
        #     if not contests:
        #         break
        contest_ids = self.get_contest_id_filters()
        if contests and self.search:
            contests = [c for c in contests if c.search(self.search, contest_ids)]

        contests.sort(key=lambda x: x.name)

        return contests

    def get_contest_groups(self, contests):
        """gets contests grouped by contest groups"""
        groups = db.get_items_by_data_type(DataType.DATA_TYPE_CONTEST_GROUPING)
        return_val = []
        for g in groups:
            group_contests = [c for c in contests if
                              c.parents(DataType.DATA_TYPE_CONTEST_GROUPING, lambda x: x.value == g.value)]
            return_val.append({'group': g.value, 'contests': group_contests})

        return return_val





    def set_form_contest(self):
        """sets the contest data """
        if self.contest_id:
            try:
                self.contest = db.get_contest(self.contest_id)
            except:
                log.error("Contest ID: {0} not found".format(self.contest_id))
                self.contest_id = ''
        elif self.contests:
            self.contest_id = self.contests[0].id
            self.contest = self.contests[0]

        if self.contest:
            def get_decisions():
                return db.get_contest_decisions(self.contest)


            #eventually we got to only return only a page of opinions at a time,
            #but we don't have a real database yet so we have to do our summaries manually in code

            #we don't want to cache for the demo we want results right away.
            # self.contest.decisions = helpers.get_cache(cache, 'all_decisions_{0}'.format(self.contest.id),
            #                                             get_decisions, 300)

            self.contest.decisions = get_decisions()



            self.all_opinions = self.contest.get_all_opinions()
            self.official_opinions = self.contest.get_official_opinions()
            self.all_opinion_summary = Opinion.get_opinion_summary(
                self.all_opinions, self.contest.contestants,self.contest.decision_type, self.contest.allow_write_ins)
            self.official_opinion_summary = Opinion.get_opinion_summary(
                self.official_opinions, self.contest.contestants,
                self.contest.decision_type, self.contest.allow_write_ins)



            


