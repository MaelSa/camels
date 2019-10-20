class Player:
    def __init__(self, name, socket, oponnent_socket):
        self.name = name
        self.nb_camel = 0
        self.hand = []
        self.hand_str = []
        self.score = 0
        self.bonus = []
        self.bonus_int = 0
        self.socket = socket
        self.oponent_socket = oponnent_socket

    def buy(self, ressource, nb):
        cpt = int(self.hand_str.count(ressource))
        if cpt >= nb:
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

    def show_hand(self):
        strn = ''
        for c in self.hand_str:
            strn += c + ', '
        return (f'Votre main est {strn}')



    def take_card(self, card):
        self.hand_str.append(card)

    def take_camels(self, nb):
        self.nb_camel += nb

    def add_hand(self, card):
        self.hand_str.append(card)
