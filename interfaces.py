from minmax_agent import minmaxagent
from tictactoe_game import tictactoe
import Q_agent
import DQN_agent


def console_play():
    # DEPRECATED!!!! USE CONSOLE_PLAY_MINMAX
    print("please input parameters of the game:")
    dim1 = int(input("dimension1"))
    dim2 = int(input("dimension2"))
    order = int(input("orer"))
    stopper = ""
    while stopper != "stop":
        test = tictactoe(dim1, dim2, order)
        whose_move = "X"
        while test.gamestate == "in_play":
            test.print_board()
            print(whose_move + " move")
            move = [int(x) for x in input("Enter move in format 0-0 ").split("-")]
            test.make_move(move)
        print(test.gamestate)
        stopper = input("press Enter to play again or type stop")


def change_move(move):
    if move == "X":
        return "O"
    else:
        return "X"


def console_play_minmax():
    print("please input parameters of the game:")
    dim1 = int(input("dimension1"))
    dim2 = int(input("dimension2"))
    order = int(input("order"))
    type_player_x = input("choose X player human (0) or minmax (1) or Q")
    type_player_o = input("choose O player human (0) or minmax (1) or Q")
    if type_player_x == "minmax":
        agent_x = minmaxagent()
    elif type_player_x == "Q":
        agent_x = Q_agent.Qagent(dim1, dim2, order, epsilon=0)
        agent_x.load_Q()
    elif type_player_x == "DQN":
        agent_x = DQN_agent.DQNagent(dim1, dim2, order, 30, 10, epsilon=0)
        agent_x.load_DQN()
    if type_player_o == "minmax":
        agent_o = minmaxagent()
    elif type_player_o == "Q":
        agent_o = Q_agent.Qagent(dim1, dim2, order, epsilon=0)
        agent_o.load_Q()
    elif type_player_o == "DQN":
        agent_o = DQN_agent.DQNagent(dim1, dim2, order, 30, 10, epsilon=0)
        agent_o.load_DQN()
    stopper = ""
    while stopper != "stop":

        test = tictactoe(dim1, dim2, order)
        whose_move = "X"
        while test.gamestate == "in_play":
            test.print_board()
            print(whose_move + " move")
            if whose_move == "X":
                if type_player_x != "human":
                    move = agent_x.suggest_move(test)
                else:
                    move = [
                        int(x) for x in input("Enter move in format 0-0 ").split("-")
                    ]
            if whose_move == "O":
                if type_player_o != "human":
                    move = agent_o.suggest_move(test)
                else:
                    move = [
                        int(x) for x in input("Enter move in format 0-0 ").split("-")
                    ]
            test.make_move(move)
            whose_move = change_move(whose_move)
        print(test.gamestate)
        test.print_board()
        stopper = input("press Enter to play again or type stop")


if __name__ == "__main__":
    console_play_minmax()
