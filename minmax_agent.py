import copy

# from game import tictactoe
class minmaxagent:
    def __init__(self):
        pass

    def first_central_move(self, game):
        move1 = int(round(game.dimension / 2 + 0.1)) - 1
        move2 = int(round(game.dimension2 / 2 + 0.1)) - 1
        return [move1, move2]

    def choose_move_minmax(self, game):
        if len(game.sequence_x) == 0:
            self.move_index = -2
            return
        if game.gamestate != "in_play":
            return game.gamestate
        else:
            checker = []
            checker2 = []
            possible_moves = game.moves_generator()
            # Simple cutoff

            for i in possible_moves:
                game_copy = copy.deepcopy(game)
                game_copy.make_move(i)
                checker.append(game_copy.gamestate)
            if (len(game.sequence_x) + len(game.sequence_o)) % 2 == 0:
                if "win_x" in checker:
                    self.move_index = checker.index("win_x")
                    return "win_x"
                z = 0
                for i in possible_moves:
                    # recursive call
                    game_copy = copy.deepcopy(game)
                    game_copy.make_move(i)
                    outcome = self.choose_move_minmax(game_copy)
                    if outcome == "win_x":
                        self.move_index = z
                        return "win_x"
                    else:
                        checker2.append(outcome)
                    z += 1
                if "draw" in checker2:
                    self.move_index = checker2.index("draw")
                    return "draw"
                else:
                    self.move_index = -1
                    return "win_o"
            else:
                #                print("O turn")
                if "win_o" in checker:
                    self.move_index = checker.index("win_o")
                    return "win_o"
                z = 0
                for i in possible_moves:
                    # recursive call
                    game_copy = copy.deepcopy(game)
                    game_copy.make_move(i)
                    outcome = self.choose_move_minmax(game_copy)
                    if outcome == "win_o":
                        self.move_index = z
                        return "win_o"
                    else:
                        checker2.append(outcome)
                    z += 1
                if "draw" in checker2:
                    self.move_index = checker2.index("draw")
                    return "draw"
                else:
                    self.move_index = -1
                    return "win_x"

    def suggest_move(self, game):
        possible_moves = game.moves_generator()
        self.choose_move_minmax(game)
        print("the move index")
        print(self.move_index)
        if self.move_index == -1:
            return possible_moves[0]
        elif self.move_index < -1.5:
            return self.first_central_move(game)
        else:
            return possible_moves[self.move_index]


def alpha_beta(obj):
    pass


def genetic_alpha_beta(obj):
    pass


# agent=minmaxagent()
# start=datetime.datetime.now()
# x=tictactoe(3,3,3)
# x.make_move([1,1])
# print(agent.suggest_move(x))
