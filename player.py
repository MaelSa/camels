class Player:
    def __init__(self, name, socket, oponnent_socket, position):
        """
        Creates a player, with a name, a socket and the opponent's socket
        :param name: string
        :param socket: socket
        :param oponnent_socket: socket
        """
        self.name = name
        self.nb_camel = 0
        self.hand = []
        self.hand_str = []
        self.score = 0
        self.bonus = []
        self.bonus_int = 0
        self.socket = socket
        self.oponent_socket = oponnent_socket
        self.position = position
        self.is_turn = False
        self.is_turn = False
        self.other_player = None

    def buy(self, ressource, nb):
        """
        Fun to buy ressource in nb quantity
        :param ressource: string
        :param nb: int
        :return:
        """
        cpt = int(self.hand_str.count(ressource))
        if cpt >= nb:
            for i in range(0, nb):
                self.hand_str.remove(ressource)
            return True
        else:
            return False

    def add_score(self, int):
        """
        Adds int to the player's score
        :param int: integer
        :return:
        """
        self.score += int

    def ok_choice_take_card(self):
        """
        Is it ok for this player to take a card ?
        :return: bool
        """
        return len(self.hand_str) < 5

    def ok_choice_trade(self):
        """
        is it ok for this player to trade ?
        :return: bool
        """
        return (len(self.hand_str) + self.nb_camel) > 1

    def ok_choice_sell(self):
        """
        Is it ok for this player to sell ?
        :return: bool
        """
        return len(self.hand_str) > 0

    def show_hand(self):
        """
        Shows the player's hand
        :return: string
        """
        strn = ''
        for c in self.hand_str:
            strn += c + ', '
        return (f'Votre main est {strn}')

    def take_card(self, card):
        """
        Takes the selected card
        :param card: string
        :return:
        """
        self.hand_str.append(card)

    def take_camels(self, nb):
        """
        Adds nb camels to the player
        :param nb: int
        :return:
        """
        self.nb_camel += nb

    def add_hand(self, card):
        """
        Add card to the player's hand
        :param card: string
        :return:
        """
        self.hand_str.append(card)
