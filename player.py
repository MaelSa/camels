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

    def ok_choice_take_card(self):
        return len(self.hand_str) < 5

    def ok_choice_trade(self):
        return (len(self.hand_str) + self.nb_camel) > 1

    def ok_choice_sell(self):
        return len(self.hand_str) > 0

    def take_card(self, card):
        self.hand_str.append(card)

    def take_camels(self, nb):
        self.nb_camel += nb
