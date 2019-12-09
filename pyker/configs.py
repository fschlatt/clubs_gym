LEDUC_2P_ENV = {
    'num_players': 2,
    'num_streets': 2,
    'small_blind': 0,
    'big_blind': 0,
    'ante': 1,
    'raise_size': 2,
    'num_raises': 2,
    'num_suits': 2,
    'num_ranks': 3,
    'num_hole_cards': 1,
    'num_community_cards': [0, 1],
    'num_cards_for_hand': 2,
    'mandatory_num_hole_cards': 0,
    'start_stack': 10
}

KUHN_3P_ENV = {
    'num_players': 3,
    'num_streets': 1,
    'small_blind': 0,
    'big_blind': 0,
    'ante': 1,
    'raise_size': [1],
    'num_raises': [1],
    'num_suits': 1,
    'num_ranks': 4,
    'num_hole_cards': 1,
    'num_community_cards': [],
    'num_cards_for_hand': 1,
    'mandatory_num_hole_cards': 0,
    'start_stack': 10
}

LIMIT_HOLDEM_2P_ENV = {
    'num_players': 2,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': [2, 2, 4, 4],
    'num_raises': 4,
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

LIMIT_HOLDEM_6P_ENV = {
    'num_players': 6,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': [2, 2, 4, 4],
    'num_raises': 4,
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

LIMIT_HOLDEM_9P_ENV = {
    'num_players': 9,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': [2, 2, 4, 4],
    'num_raises': 4,
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

NOLIMIT_HOLDEM_2P_ENV = {
    'num_players': 2,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': 'inf',
    'num_raises': 'inf',
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

NOLIMIT_HOLDEM_6P_ENV = {
    'num_players': 6,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': 'inf',
    'num_raises': 'inf',
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

NOLIMIT_HOLDEM_9P_ENV = {
    'num_players': 9,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': 'inf',
    'num_raises': 'inf',
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

POT_LIMIT_OMAHA_2P_ENV = {
    'num_players': 2,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': ['pot', 'pot', 'pot', 'pot'],
    'num_raises': 'inf',
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 4,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 2,
    'start_stack': 200
}

POT_LIMIT_OMAHA_6P_ENV = {
    'num_players': 6,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': ['pot', 'pot', 'pot', 'pot'],
    'num_raises': 'inf',
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 4,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 2,
    'start_stack': 200
}

POT_LIMIT_OMAHA_9P_ENV = {
    'num_players': 9,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': ['pot', 'pot', 'pot', 'pot'],
    'num_raises': 'inf',
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 4,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 2,
    'start_stack': 200
}

SHORT_DECK_2P_ENV = {
    'num_players': 2,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': 'inf',
    'num_raises': 'inf',
    'num_suits': 4,
    'num_ranks': 9,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

SHORT_DECK_6P_ENV = {
    'num_players': 6,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': 'inf',
    'num_raises': 'inf',
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

SHORT_DECK_9P_ENV = {
    'num_players': 9,
    'num_streets': 4,
    'small_blind': 1,
    'big_blind': 2,
    'ante': 0,
    'raise_size': 'inf',
    'num_raises': 'inf',
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}