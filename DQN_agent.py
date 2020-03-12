import collections
import os
from tictactoe_game import tictactoe
import random
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, BatchNormalization
from keras import initializers, regularizers


class DQNagent:
    def network_init(self, input_dim, layer_1, layer_2):
        elastic_net = regularizers.l1_l2(l1=0.0001, l2=0.0001)
        self.training_model = Sequential()
        self.training_model.add(
            Dense(layer_1, input_dim=input_dim, W_regularizer=elastic_net)
        )
        self.training_model.add(Activation("relu"))
        self.training_model.add(Dense(layer_2, W_regularizer=elastic_net))
        self.training_model.add(Activation("relu"))
        self.training_model.add(Dense(1))
        self.training_model.add(Activation("linear"))
        self.training_model.compile(
            loss="mse", optimizer="rmsprop", metrics=["accuracy"]
        )

    def __init__(self, dimension1, dimension2, order, layer_1, layer_2, epsilon=0.1):
        self.network_init(dimension1 * dimension2 * 2, layer_1, layer_2)
        self.ER_mem_size = 3000
        self.minibatch_size = 148
        self.episodes_before_update = 6
        self.epsilon = epsilon
        self.dimension1 = dimension1
        self.dimension2 = dimension2
        self.order = order
        # This will be used for action replay
        self.experience_replay_state_action_reward = []
        self.Qpath = os.path.join(
            "saved_agents",
            "DQNagent-"
            + str(self.dimension1)
            + "-"
            + str(self.dimension2)
            + "-"
            + str(self.order),
        )

    def save_DQN(self):
        """ Pickle the agent object instance to save the agent's state. """
        self.training_model.save(self.Qpath)

    def load_DQN(self):
        self.training_model = load_model(self.Qpath)

    def state_hash(self, game):
        # c for crosses, n for naughts, e for emptys
        state_list = []
        for i in game.board:
            for j in i:
                if j == "X":
                    state_list.append(1)
                elif j == "O":
                    state_list.append(-1)
                else:
                    state_list.append(0)
        return state_list

    def action_decode(self, action, whose_move):
        action_hot_encode = [0] * (self.dimension1 * self.dimension2)
        action_code = action[0] * self.dimension1 + action[1]
        if whose_move == "X":
            action_hot_encode[action_code] = 1
        else:
            action_hot_encode[action_code] = -1
        return action_hot_encode

    def get_action_train(self, game):
        # may probably want to vectorize predict to take inputs for all action and choose argmax
        # Make sure we only consider empty board spaces
        s = self.state_hash(game)
        possible_actions = game.moves_generator()
        if random.random() < self.epsilon:
            # Random choose.
            action = possible_actions[random.randint(0, len(possible_actions) - 1)]
        else:
            # Greedy choose. At least one action will always be possible
            # when this function is called.
            model_inputs = []
            for i in possible_actions:
                model_inputs.append(s + self.action_decode(i, game.whose_move))
            model_inputs = np.array(model_inputs)
            scores = self.training_model.predict(model_inputs)

            if game.whose_move == "X":
                action = possible_actions[np.argmax(scores)]
            else:
                action = possible_actions[np.argmin(scores)]
        return action

    def get_reward(self, game):
        if game.gamestate == "in_play":
            return 0
        elif game.gamestate == "win_x":
            return 1
        else:
            return -1

    def experience_replay_add(
        self, state, action, reward, new_state, whose_move, length
    ):
        if len(self.experience_replay_state_action_reward) == length:
            del self.experience_replay_state_action_reward[0]
        self.experience_replay_state_action_reward.append(
            [state, action, reward, new_state, whose_move]
        )

    def experience_replay_sample(self, minibatch_size):
        if len(self.experience_replay_state_action_reward) > minibatch_size:
            rand_smpl = [
                self.experience_replay_state_action_reward[i]
                for i in sorted(
                    random.sample(
                        range(len(self.experience_replay_state_action_reward)),
                        minibatch_size,
                    )
                )
            ]
        else:
            rand_smpl = self.experience_replay_state_action_reward
        return rand_smpl

    def clip(x):  # clip reward to rannge [1, -1]
        if x > 1:
            return 1
        elif x < -1:
            return -1
        else:
            return x

    def update_nn(self):
        # In game play _s must be an array of all state-action pairs
        rand_smpl = self.experience_replay_sample(self.minibatch_size)
        X = [i[0] + i[1] for i in rand_smpl]
        X = np.array(X)
        y = []
        r = 0
        for s, a, r, _s, move in rand_smpl:  # state action reward next_state
            # print _s
            if (
                r == 0
            ):  # update the reward if it's a non terminal step. the reward is 0 for all non terminal steps
                # IF O would want min rather than max
                if move == "X":
                    r = np.max(
                        self.training_model.predict(np.array(_s))
                    )  # gamma*Q(s', a)
                if move == "O":
                    r = np.min(self.training_model.predict(np.array(_s)))
            y.append(r)
        y = np.array(y)
        self.training_model.train_on_batch(X, y)

    def make_correct_form_new_state(self, game):
        final_state = []
        possible_actions = game.moves_generator()
        state_hash = self.state_hash(game)
        for i in possible_actions:
            final_state.append(state_hash + self.action_decode(i, game.whose_move))
        return final_state

    def train_with_itself(self, number_of_episode_games):
        batch_results = []
        for i in range(number_of_episode_games):
            game = tictactoe(self.dimension1, self.dimension2, self.order)
            while game.gamestate == "in_play":
                old_state = self.state_hash(game)
                # reward previous O game
                action = self.get_action_train(game)
                # Store whose move was made, as next line the mover is change
                whose_move = game.whose_move
                game.make_move(action)
                # need to change this one:
                new_state = self.make_correct_form_new_state(game)
                r = self.get_reward(game)
                self.experience_replay_add(
                    old_state,
                    self.action_decode(action, whose_move),
                    r,
                    new_state,
                    game.whose_move,
                    self.ER_mem_size,
                )
            batch_results.append(game.gamestate)
            #            game.print_board()
            # ocassionaly tell progress
            if i % self.episodes_before_update == 0:
                self.update_nn()
            if i % 100 == 0:
                print("Training Game " + str(i))
                print("Following are the results of last 100 games:")
                print(collections.Counter(batch_results))
                batch_results = []
            if i % 5000 == 0:
                if i != 0:
                    self.save_DQN()
                game.print_board()

    def suggest_move(self, game):
        s = self.state_hash(game)
        possible_actions = game.moves_generator()
        model_inputs = []
        for i in possible_actions:
            model_inputs.append(s + self.action_decode(i, game.whose_move))
        model_inputs = np.array(model_inputs)
        scores = self.training_model.predict(model_inputs)

        if game.whose_move == "X":
            action = possible_actions[np.argmax(scores)]
        else:
            action = possible_actions[np.argmin(scores)]
        return action


# test=DQNagent(4,4,4,40,20,epsilon=0.03)
# test.load_DQN()
# test.train_with_itself(200002)
# print('\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a')
