import collections
import pickle
import os
from tictactoe_game import tictactoe
import random
import numpy as np

# from game import tictactoe
class Qagent:
    def constant_factory(self):
        # encourage exploration
        return 0.9

    def __init__(
        self, dimension1, dimension2, order, Q={}, alpha=0.3, gamma=0.9, epsilon=0.1
    ):
        self.Q = Q
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.dimension1 = dimension1
        self.dimension2 = dimension2
        self.order = order
        self.action = []
        self.Qpath = os.path.join(
            "saved_agents",
            "Qagent-"
            + str(self.dimension1)
            + "-"
            + str(self.dimension2)
            + "-"
            + str(self.order),
        )
        for i in range(0, dimension1):
            for j in range(0, dimension1):
                self.action.append((i, j))
        for action in self.action:
            #           self.Q[action] = collections.defaultdict(int)
            self.Q[action] = collections.defaultdict(self.constant_factory)

    def save_Q(self):
        """ Pickle the agent object instance to save the agent's state. """
        if os.path.isfile(self.Qpath):
            os.remove(self.Qpath)
        f = open(self.Qpath, "wb")
        pickle.dump(self.Q, f)
        f.close()

    def load_Q(self):
        f = open(self.Qpath, "rb")
        self.Q = pickle.load(f)
        f.close()

    def state_hash(self, game):
        # c for crosses, n for naughts, e for emptys
        final_hash = ""
        for i in game.board:
            for j in i:
                if j == "X":
                    final_hash += "c"
                elif j == "O":
                    final_hash += "n"
                else:
                    final_hash += "e"
        return final_hash

    def get_action_train(self, game):
        # Make sure we only consider empty board spaces
        s = self.state_hash(game)
        possible_actions = game.moves_generator()
        if random.random() < self.epsilon:
            # Random choose.
            action = possible_actions[random.randint(0, len(possible_actions) - 1)]
        else:
            # Greedy choose. At least one action will always be possible
            # when this function is called.
            Q_max = -np.inf
            for a in possible_actions:
                if self.Q[tuple(a)][s] > Q_max:
                    Q_max = self.Q[tuple(a)][s]
                    action = a
        return action

    def update_endog(self, s, s_, a, r):
        """ Perform the Q-Learning step update of Q values. """
        # Endogenous update looking at Q values of the opponent which are negative for the person
        # Update Q(s,a)
        # Hold list of Q values for all a_,s_ pairs so we can access max later
        if r == 0:
            # if not the endstate. THis is done to speed up learning
            Q_options = []
            for action in self.action:
                if self.Q[tuple(action)][s_] != 0.9:
                    Q_options += [self.Q[tuple(action)][s_]]
                # usualy it is plus near max, but here it is minus
            try:
                the_update = max(Q_options)
            except:
                the_update = 0
            self.Q[tuple(a)][s] = (1 - self.alpha) * self.Q[tuple(a)][
                s
            ] + self.alpha * (r - self.gamma * the_update)
        else:
            # if endstate.
            self.Q[tuple(a)][s] = (1 - self.alpha) * self.Q[tuple(a)][
                s
            ] + self.alpha * (r)

    def get_reward(self, game):
        if game.gamestate == "in_play":
            return 0
        elif game.gamestate == "draw":
            return 0.5
        else:
            return 1

    def train_with_itself(self, number_of_episode_games):
        batch_results = []
        for i in range(number_of_episode_games):
            game = tictactoe(self.dimension1, self.dimension2, self.order)
            while game.gamestate == "in_play":
                old_state = self.state_hash(game)
                # reward previous O game
                action = self.get_action_train(game)
                game.make_move(action)
                new_state = self.state_hash(game)
                r = self.get_reward(game)
                self.update_endog(old_state, new_state, action, r)
            batch_results.append(game.gamestate)
            #            game.print_board()
            # ocassionaly tell progress
            if i % 100 == 0:
                print("Training Game " + str(i))
                print("Following are the results of last 100 games:")
                print(collections.Counter(batch_results))
                batch_results = []
            if i % 5000 == 0:
                self.save_Q()
                game.print_board()

    def suggest_move(self, game):
        s = self.state_hash(game)
        possible_actions = game.moves_generator()
        Q_max = -np.inf
        for a in possible_actions:
            if self.Q[tuple(a)][s] > Q_max:
                Q_max = self.Q[tuple(a)][s]
                action = a
        return action


# test=Qagent(5,5,4,alpha=0.8,gamma=0.8,epsilon=0.025)
# test.load_Q()
# test.train_with_itself(100000)
# test.load_Q()
# print(test.Q)
# test.train_with_itself(1000000)
