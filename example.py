import random

import pyker_engine

# 1-2 no limit 6 player texas hold'em
config = pyker_engine.configs.NOLIMIT_HOLDEM_6P_ENV
dealer = pyker_engine.Dealer(**config)
obs = dealer.reset()

while True:
    # number of chips a player must bet to call
    call = obs['call']
    # smallest number of chips a player is allowed to bet for a raise
    min_raise = obs['min_raise']
    # largest number of chips a player is allowed to bet for a raise
    max_raise = obs['max_raise']

    rand = random.random()
    # 10% chance to fold
    if rand < 0.1:
        bet = 0
    # 80% chance to call
    elif rand < 0.80:
        bet = call
    # 10% to raise
    else:
        bet = random.randint(min_raise, max_raise)

    obs, rewards, done = dealer.step(bet)

    if all(done):
        break

print(rewards)
