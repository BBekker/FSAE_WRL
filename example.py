# Glicko
# python 3.4.3
# Copyright (c) 2016 by Matt Sewall.
# All rights reserved.
import math
import csv
import json
import os
import shutil
from sys import argv
from datetime import datetime
from operator import itemgetter
from glicko import *
from glicko_classes import *
import pandas as pd

# Ratings dictionaries contain athletes keyed to an elo value
# Entries dictionaries contain athletes keyed to history of their results

COMBUSTION_CLASS = 1
ELECTIC_CLASS = 2

teams = {}
_INITRAT = 1500.0
_INITCONF = 350.0
_INITVOL = .06


def do_glicko(data):
    # Add players to competition and calculate ratings

    meet = RatingPeriod()
    meet.competitors = []
    for competitor in data:
        #get this teams score
        team = teams[competitor['id']]
        meet.addCompetitor(competitor['id'], competitor['rank'], competitor['score'], team['rating'], team['confidence'], team['volatility'])
    if len(meet.competitors) > 1:
        calculateGlicko(meet.competitors)

        # Take results of competition and append data
        for runner in meet.competitors:
            teams[runner.id]['rating'] = runner.rating
            teams[runner.id]['confidence'] = runner.confidence
            teams[runner.id]['volatility'] = runner.volatility


def load_data(filename):
    events = []
    currentEvent = 0
    data = pd.read_csv(filename)
    data = data[data['class'] == ELECTIC_CLASS]
    for row in data.itertuples():
        teams[row.university] = dict(id = row.university,name = row.university_name, rating = _INITRAT, confidence = _INITCONF, volatility = _INITVOL)

        team = {'id': int(row.university),
                'score': float(row.total),
                'rank': int(row.rank)}

        #Add team to event      
        if(int(row.world_event) == currentEvent):
            events[-1]['results'].append(team)
        else:
            #new event

            events.append({
                'id': int(row.world_event),
                'results': [team]
                })
            currentEvent = int(row.world_event)
    return events

def main():
    events = load_data(argv[1])
    count = 0
    for event in events:
        do_glicko(event['results']) 
        # print(teams[41])
    res = []
    for k, v in teams.items():
        res.append((v['name'], v['rating'], v['confidence']))
    res.sort(key=itemgetter(1),reverse=True)
    for i in res:
        print(f"{i[0]:35s} points:{i[1]:<10.2f}  95% int:{i[2]*2:<10.2f}")
    #print(f"{v['name']} : {v['rating']}")


if __name__ == '__main__':
    main()
