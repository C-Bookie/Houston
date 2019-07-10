
import gym
import numpy as np
import tensorflow as tf
from tensorflow.python import debug as tf_debug
import matplotlib.pyplot as plt
import math
import random



MODEL_PATH = "./models/test.h5"  # path to save/load the trained model to/from
SAVE = True  # whether to save the trained model
LOAD = False  # whether to load a saved model
DEMO = False  # whether to skip model training

TENSOR_BOARD = True  # whether to log training statistics
LOG_DIR = "logs\\fit"  # location to save training statistics
DEBUG_PORT = "CRAY-2:6007"  # port for to host model training debugging

smallestAmt = 5  # size of the cheapest chip in the game

moves = {  # list of actions
    "CHECK": 0,
    "CALL": 1,
    "RAISE": 2,
    "FOLD": 3
}

def sigmoid(x):
  return 1 / (1 + math.exp(-x))


def ask(msg, options, cruise = False):  # asks a player to select action, returns the selected action
    assert len(options) > 0

    msg += " | "
    for i in range(len(options)):
        if i != 0:
            msg += " / "
        msg += "(" + str(i) + ")" + options[i]
    msg += "> "

    if cruise:
        # print(msg)
        return random.randint(0, len(options) - 1)

    while True:
        choice = input(msg)
        n = int(choice)
        if 0 <= n and n < len(options):
            return n

def askAmt(msg, low, high, cruise = False):  # asks a player to select an amount, returns the selected amount
    low += smallestAmt
    assert low >= 0
    assert low <= high

    msg += " | " + str(low) + "-" + str(high) + ">"

    if cruise:
        # print(msg)
        limit = (high - low) / smallestAmt
        # assert limit % 1 == 0  # fixme
        limit = (int)(limit)
        # return low
        return low + (random.randint(0, limit) * smallestAmt)

    while True:
        choice = input(msg)
        n = int(choice)
        if low > n:
            print("must be above " + str(low))
        elif high < n:
            print("must be below " + str(high))
        elif n % smallestAmt != 0:
            print("must be a multiple of " + str(smallestAmt))
        else:
            return n


class Trainer:  # a class for repetitive model training
    def __init__(self, env, responses):
        self.env = env  # an instance of the holdem OpenAI gym environment, used for all poker logic
        self.responses = responses  # a list of what wach player is: ann=artificial neural network, player=asks the player for input, rand=choose random action, safe=default safe option. the first must be ann
        self.LR = 1e-3  # the learning rate for model training
        self.useModel = False  # whether to use the model for predictions yet (set to true after initial training)
        self.buildModel()

    def __del__(self):
        self.env.close()

    def buildModel(self):  # builds/loads a Keras model capable of taking in the state of the game and predicting the best action
        self.outputSize = 2

        if LOAD:
            self.model = tf.keras.models.load_model(MODEL_PATH)
            self.useModel = True
        else:
            self.model = tf.keras.models.Sequential([
                tf.keras.layers.Dense(128, activation='relu', name="big"),
                tf.keras.layers.Dropout(0.8),
                tf.keras.layers.Dense(52, activation='relu'),
                tf.keras.layers.Dropout(0.8),
                tf.keras.layers.Dense(self.outputSize, activation='linear')
            ])
            self.model.compile(loss='mse', optimizer="adam")

        if TENSOR_BOARD:
            self.tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=LOG_DIR)  # attaches a callback to record training statistics

    def workout(self, training=True):
        if training:
            if self.useModel:
                initial_games = 10
            else:
                initial_games = 100
        else:
            initial_games = 5  # runs through 5 games to demonstrate the current capabilities of the model between each training sesion

        training_data = []  # stores a log of all performed actions and their results to be used as training data
        scores = []  # stores the resulting score of each set of training data
        for i in range(initial_games):
            game_memory = []
            for player in range(self.env.n_seats):  # reset the game
                self.env.remove_player(player)
                self.env.add_player(player, stack=2000)
            (player_states, (community_infos, community_cards)) = self.env.reset()

            terminal = False
            score = 0
            while not terminal:
                if not training:
                    self.env.render(mode='human')

                # actions = np.array(holdem.safe_actions(community_infos, n_seats=self.env.n_seats))


			reference = jazZy
            scores += [get_score(reference)]
            print("M" if self.useModel else "T", "|cycle: ", i, " | ", score)
            for data in game_memory:
                training_data += [[data[0], data[1], score]]

        return training_data, scores

    def reflect(self, training_data, scores):  # use the collected training data to re-fit (train) the model to improve the quality of its predictions
        # assert scores[0] != scores[-1]  # bad fitness function
        threshold = 0.1  # scores must be within the top 10%
        scores.sort(reverse=True)
        toBeat = scores[(int)(len(scores)*threshold)]

        x = []
        y = []
        for i in training_data:  # reshape the training data
            if i[2] >= toBeat:
                x += [i[0]]
                y += [i[1]]

        if TENSOR_BOARD:
            self.model.fit(
                np.array(x).astype(np.float32),
                np.array(y).astype(np.float32),
                batch_size=len(x),
                callbacks=[self.tensorboard_callback],  # record training statistics
                epochs=5
            )
        else:
            self.model.fit(
                np.array(x).astype(np.float32),
                np.array(y).astype(np.float32),
                batch_size=len(x),
                epochs=5
            )

        self.useModel = True

def run():
    trainer = Trainer(env = gym.make("TexasHoldem-v1"), responses = [
        "ann",  # artificial neural network
        "rand", #"player",  # asks the player for input
        "rand",  # choose random action
        "safe"  # default safe option
    ])

    for player in range(trainer.env.n_seats):
        trainer.env.add_player(player, stack=2000)

    if DEMO:
        while True:
            trainer.workout(False)
    else:
        # for i in range(200):
        i = 0
        while True:
            trainer.useModel = False
            training_data, scores = trainer.workout()  # collect new training data
            if not DEMO:
                Trainer.reflect(trainer, training_data, scores)
            _training_data, _scores = trainer.workout(False)  # demonstrate the current models predictive skills
            if SAVE:
                trainer.model.save(MODEL_PATH)
            if i % 50 == 0:
                weights = trainer.model.get_layer("big").get_weights()[0]  # render the "big" layer of the models weights
                plt.imshow(weights.astype(np.float32))
                plt.show()
            i += 1

if __name__ == "__main__":
    run()





