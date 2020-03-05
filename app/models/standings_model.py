
# Object to return group standings in
class GroupStandings():
    group = None
    standings = list()

    class Standing():
        user = None
        wins = None
        losses = None

        def __init__(self, user=None, wins=None, losses=None):
            self.user = user
            self.wins = wins
            self.losses = losses

    def __init__(self, group=None, standings=None):
        self.group = group
        self.standings = standings

# Object to return qualifier standings in
class QualifierStandings():
    user = None
    place = None
    average_time = None

    def __init__(self, user=None, place=None, average_time=None):
        self.user = user
        self.place = place
        self.average_time = average_time
