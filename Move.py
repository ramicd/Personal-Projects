
class Move:
    """
    Move Class: defines the attributes of each move
    """
    def __init__(self, name, type, category, contest, pp, power, accuracy):
        self.name = name
        self.type = type
        self.category = category
        self.contest = contest
        self.pp = pp
        self.power = power
        self.accuracy = accuracy
