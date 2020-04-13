LEDUC_TWO_PLAYER = {
    'num_players': 2,
    'num_streets': 2,
    'blinds': 0,
    'antes': 1,
    'raise_sizes': 2,
    'num_raises': 2,
    'num_suits': 2,
    'num_ranks': 3,
    'num_hole_cards': 1,
    'num_community_cards': [0, 1],
    'num_cards_for_hand': 2,
    'mandatory_num_hole_cards': 0,
    'start_stack': 10
}

KUHN_THREE_PLAYER = {
    'num_players': 3,
    'num_streets': 1,
    'blinds': 0,
    'antes': 1,
    'raise_sizes': [1],
    'num_raises': [1],
    'num_suits': 1,
    'num_ranks': 4,
    'num_hole_cards': 1,
    'num_community_cards': [],
    'num_cards_for_hand': 1,
    'mandatory_num_hole_cards': 0,
    'start_stack': 10
}

LIMIT_HOLDEM_TWO_PLAYER = {
    'num_players': 2,
    'num_streets': 4,
    'blinds': [1, 2],
    'antes': 0,
    'raise_sizes': [2, 2, 4, 4],
    'num_raises': [3, 4, 4, 4],
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

LIMIT_HOLDEM_SIX_PLAYER = {
    'num_players': 6,
    'num_streets': 4,
    'blinds': [1, 2, 0, 0, 0, 0],
    'antes': 0,
    'raise_sizes': [2, 2, 4, 4],
    'num_raises': [3, 4, 4, 4],
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

LIMIT_HOLDEM_NINE_PLAYER = {
    'num_players': 9,
    'num_streets': 4,
    'blinds': [1, 2, 0, 0, 0, 0, 0, 0, 0],
    'antes': 0,
    'raise_sizes': [2, 2, 4, 4],
    'num_raises': [3, 4, 4, 4],
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

NO_LIMIT_HOLDEM_TWO_PLAYER = {
    'num_players': 2,
    'num_streets': 4,
    'blinds': [1, 2],
    'antes': 0,
    'raise_sizes': float('inf'),
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

NO_LIMIT_HOLDEM_SIX_PLAYER = {
    'num_players': 6,
    'num_streets': 4,
    'blinds': [1, 2, 0, 0, 0, 0],
    'antes': 0,
    'raise_sizes': float('inf'),
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

NO_LIMIT_HOLDEM_NINE_PLAYER = {
    'num_players': 9,
    'num_streets': 4,
    'blinds': [1, 2, 0, 0, 0, 0, 0, 0, 0],
    'antes': 0,
    'raise_sizes': float('inf'),
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

NO_LIMIT_HOLDEM_BB_ANTE_NINE_PLAYER = {
    'num_players': 9,
    'num_streets': 4,
    'blinds': [2, 4, 0, 0, 0, 0, 0, 0, 0],
    'antes': [0, 1, 0, 0, 0, 0, 0, 0, 0],
    'raise_sizes': float('inf'),
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200
}

POT_LIMIT_OMAHA_TWO_PLAYER = {
    'num_players': 2,
    'num_streets': 4,
    'blinds': [1, 2],
    'antes': 0,
    'raise_sizes': ['pot', 'pot', 'pot', 'pot'],
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 4,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 2,
    'start_stack': 200
}

POT_LIMIT_OMAHA_SIX_PLAYER = {
    'num_players': 6,
    'num_streets': 4,
    'blinds': [1, 2, 0, 0, 0, 0],
    'antes': 0,
    'raise_sizes': ['pot', 'pot', 'pot', 'pot'],
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 4,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 2,
    'start_stack': 200
}

POT_LIMIT_OMAHA_NINE_PLAYER = {
    'num_players': 9,
    'num_streets': 4,
    'blinds': [1, 2, 0, 0, 0, 0, 0, 0, 0],
    'antes': 0,
    'raise_sizes': ['pot', 'pot', 'pot', 'pot'],
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 4,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 2,
    'start_stack': 200
}

SHORT_DECK_TWO_PLAYER = {
    'num_players': 2,
    'num_streets': 4,
    'blinds': [1, 2],
    'antes': 0,
    'raise_sizes': float('inf'),
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 9,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200,
    'order': ['sf', 'fk', 'fl', 'fh', 'st', 'tk', 'tp', 'pa', 'hc']
}

SHORT_DECK_SIX_PLAYER = {
    'num_players': 6,
    'num_streets': 4,
    'blinds': [1, 2, 0, 0, 0, 0],
    'antes': 0,
    'raise_sizes': float('inf'),
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200,
    'order': ['sf', 'fk', 'fl', 'fh', 'st', 'tk', 'tp', 'pa', 'hc']
}

SHORT_DECK_NINE_PLAYER = {
    'num_players': 9,
    'num_streets': 4,
    'blinds': [1, 2, 0, 0, 0, 0, 0, 0, 0],
    'antes': 0,
    'raise_sizes': float('inf'),
    'num_raises': float('inf'),
    'num_suits': 4,
    'num_ranks': 13,
    'num_hole_cards': 2,
    'num_community_cards': [0, 3, 1, 1],
    'num_cards_for_hand': 5,
    'mandatory_num_hole_cards': 0,
    'start_stack': 200,
    'order': ['sf', 'fk', 'fl', 'fh', 'st', 'tk', 'tp', 'pa', 'hc']
}