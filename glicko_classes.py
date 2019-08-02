# Copyright (c) 2016 by Matt Sewall.
# All rights reserved.


class GlickoPlayer:
    def __init__(self, id, place, score, rating, confidence, volatility):
        self.id = id
        self.place = place
        self.score = score
        self.rating = rating
        self.confidence = confidence
        self.volatility = volatility

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class RatingPeriod:
    competitors = []

    def addCompetitor(self, id, place, score, rating, confidence,
                      volatility):
        competitor = GlickoPlayer(id, place, score, rating, confidence,
                                  volatility)
        self.competitors.append(competitor)
