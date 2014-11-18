"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect
from ballot_box import app, settings, cache
from ballot_box.forms import BallotBoxForm
from ballot_box.modules import api
from ballot_box.models import Contest, Decision, Opinion
from ballot_box.modules.helpers import log, get_cache
import json
import uuid
import random


@app.route('/')
@app.route('/home')
def home():
    """Get Home Page"""
    log().debug("Render Page: Home")
    return redirect('/ballot-box')
    return render_template('index.html',
                           title='Home Page', )


def get_all_contests():
    """gets all contests """

    def get_all_contests_internal():
        contest_ids = api.ballot_get_all_contests()['result']
        contests = [Contest(c, api.ballot_get_contest_by_id(c)['result']) for c in contest_ids]
        return [c for c in contests if c.name]

    return get_cache(cache, 'all_contests', get_all_contests_internal)


def get_filtered_contests(form):
    """ Filters contests by the form filters """
    contests = get_all_contests()

    for f in form.filters:
        if f.value:
            contests = [c for c in contests if c.tag(f.name) == f.value]

        if not contests:
            break

    if contests and form.search:
        contests = [c for c in contests if c.search(form.search)]

    return contests


def get_contest_decisions(contest):
    """This method gets all contest decisions"""

    def get_contest_decisions_internal():
        random.seed()
        decisions = []
        ballot_ids = [uuid.uuid4() for x in range(4)]
        for i in range(1000):
            decision = Decision(str(uuid.uuid4()), contest.id, ballot_ids[random.randint(1, 10000) % 4])

            if (random.randint(1, 10000) % 10) == 0:
                # # it non-official
                decision.is_official = False
            else:
                decision.is_official = True

            if (random.randint(1, 10000) % 6) == 0:
                # make it a write in
                write_in = "Write In {0}".format(random.randint(1, 4))
                decision.opinions.append(Opinion(opinion=1, write_in=write_in,
                                                 is_official=decision.is_official, decision=decision))
            else:
                candidate = contest.contestants[random.randint(0, len(contest.contestants) - 1)]
                decision.opinions.append(Opinion(candidate, 1, is_official=decision.is_official, decision=decision))
            decisions.append(decision)


        return decisions

    return get_cache(cache, 'all_decisions_{0}'.format(contest.id), get_contest_decisions_internal)




def set_form_contest(form):
    """sets the form contest using the request data and api lookups"""
    if form.contest_id:
        try:
            form.contest = Contest(form.contest_id, api.ballot_get_contest_by_id(form.contest_id)['result'])
        except:
            log().error("Contest ID: {0} not found".format(form.contest_id))
            form.contest_id = ''
    elif form.contests:
        form.contest_id = form.contests[0].id
        form.contest = form.contests[0]

    if form.contest:
        form.contest.decisions = get_contest_decisions(form.contest)
        form.all_opinions = form.contest.get_all_opinions()
        form.official_opinions = form.contest.get_official_opinions()
        form.all_opinion_summary = Opinion.get_opinion_summary(form.all_opinions, form.contest.contestants)
        form.official_opinion_summary = Opinion.get_opinion_summary(form.official_opinions, form.contest.contestants)
    else:
        form.all_opinion_summary = []
        form.official_opinion_summary = []
        




@app.route('/ballot-box', methods=['GET', 'POST'])
def ballot_box():
    """Get Ballot Box Page"""
    log().debug("Render Page: ballot-box")
    form = BallotBoxForm(request, settings.BALLOT_BOX_FILTERS)
    form.contests = get_filtered_contests(form)
    set_form_contest(form)

    return render_template('ballot-box.html',
                           title='Ballot Box',
                           form=form)