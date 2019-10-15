class Player:
    def __init__(self, name):
        self.name = name
        self.nb_camel = 0
        self.hand = []
        self.hand_str = []
        self.score = 0
        self.bonus = []
        self.bonus_int = 0

    def buy(self, ressource, nb):
        if self.hand_str.count(ressource) >= nb:
            for i in range(0, nb):
                self.hand_str.remove(ressource)
            return True
        else:
            return False

    def add_score(self, int):
        self.score += int
