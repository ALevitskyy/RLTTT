# RLTTT
Using Reinforcement Learning to solve Tic-Tac-Toe

The code implements NxM dimensional Tic-Tac-Toe game which can be played in console. Player can play with:
1) himself
2) Against minmax agent which finds best optimal move using recursive breadth-first search algorithm
3) Pretrained agent using Q-learning algorithm with Q-function stored in memory 
4) Pretrained agent using Q-learning algorithm, where Q-function is approximated using Neural Network (DQN agent)

Check interfaces.py to see how to enter all these modes.

Check Q_agent.py for training an agent for mode 3; check DQN_agent.py for training an agent for mode 4

