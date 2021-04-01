import gym

import clubs_gym

env = gym.make("KuhnTwoPlayer-v0")

env.register_agents([clubs_gym.agent.kuhn.NashKuhnAgent(0.3)] * 2)

obs = env.reset()

while True:
    bet = env.act(obs)
    obs, rewards, done, info = env.step(bet)

    if all(done):
        break

print(rewards)
