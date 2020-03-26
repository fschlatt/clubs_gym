class PokerViewer():

    def __init__(self, num_players, num_hole_cards, num_community_cards):

        self.num_players = num_players
        self.num_hole_cards = num_hole_cards
        self.num_community_cards = num_community_cards

    def render(self, config):
        raise NotImplementedError
