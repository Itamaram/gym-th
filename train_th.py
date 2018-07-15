import gym
import gym_th

from baselines import deepq


def main():
    env = gym.make("th-v0")
    model = deepq.models.cnn_to_mlp(
        convs=[(1, 5, 1), (1, 5, 1)],
        hiddens=[7 * 8 * 2],
    )
    act = deepq.learn(
        env,
        q_func=model
    )
    print("Saving model to th_model.pkl")
    act.save("th_model.pkl")


if __name__ == '__main__':
    main()