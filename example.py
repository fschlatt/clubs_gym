import gym

import clubs

env = gym.make("KuhnTwoPlayer-v0")

env.register_agents([clubs.agent.kuhn.NashKuhnAgent(0.3)] * 2)

obs = env.reset()

while True:
    bet = env.act(obs)
    obs, rewards, done, info = env.step(bet)

    if all(done):
        break

print(rewards)
