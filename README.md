# Artificial_Intelligence_2021
PacMan Project repo for class. This repo will track the progress of the PacMan AI game throughout the Fall quarter

## Tutorial
This project is a simple python introduction to familiarize ourselves with the python language, download software for using working 
with python and establish a base programming level. The following python files were worked on: <br>
1. ``addition.py``
2. ``buyLotsOfFruit.py``
3. ``shopSmart.py``

## Project 1 - Search
This project focuses on search algorithms for the pacman to complete various mazes. I also edited the pacman agent methods to 
be able to complete different search goals around corners and "eat" dots. The two files edited are ``search.py`` and ``searchAgents.py`` 
### In ``search.py``
1. Depth First Search 
2. Breadth First Search
3. Uniform Cost Search
4. A* Search

### In ``searchAgents.py``
1. Corners Problem: Representation
2. Heuristic Corners Problem
3. Heuristic Eating All of the Dots

Suboptimal Search was optional, so I didn't complete the code, however I have left comments with code copied from 
another online source. I know it's not complete and will need to work on it in order to test the functionality.

## Project 2 - Multi-Agent Search
This project focuses on designing algorithms for the adversarial agents, Pacman and ghost, using different approaches. In the 
file ``multiAgents.py``. The following classees were worked on:<br>

1. ReflexAgent
2. MultiAgentSearch
3. MinimaxAgent
4. AlphaBetaAgent
5. ExpectimaxAgent
6. ExpectimaxAgent -> betterEvaluationFunction

## Project 3 - Reinforcement Learning
This project focuses on designing algorithms for reinforced learning for pacman through QLearning so that he can finish the game without losing. I got 100% wins during my tests.  The primary files edited were ``qlearningAgents.py`` and ``analysis.py``.
### In ``analysis.py``
1. question2
2. question3a-3e
3. question8

### In ``qlearningAgents.py``
1. QLearningAgent class </br>
  a. getQValue</br>
  b. computeValueFromQValues </br>
  c. computeActionFromQValues </br>
  d. getAction </br>
  e. update </br>
2. ApproximateQAgent</br>
  a. getQvalue</br>
  b. update</br>
  c. final</br>

