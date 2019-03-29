# pacman-game
# A distributed greedy approach with two different Evaluation

This code uses an new algorithm for scoring the best value in pacman, it uses pacman libraray and the algorith resides in pacmanAgents

Original Idea: First locate the power capsules consume them, consume the white ghosts and then every remaining pellet. Distance to be calculated by Euclidean distance formula.

Unlike the greedy approach that takes one single greedy step at a time, this algorithm first takes a BFS step and generates all the possible child node in all directions and then switches on to a greedy algo for the child nodes in all directions. The greedy algorithm uses a step Evaluation function and the results of all the child Nodes is combined with using the game evaluation function. Both the step Evaluation and the game evaluation is a weighted combination of score gained and distance from Goal.
For getting the best evaluation I tried to different weights for distance and score for both game and step evaluation.
 
Drawbacks: Pacman does get confused around the corner sometimes, when distance algoritm of two adjacent blocks gives two different goals.
Future Work: Determine if the pacman is moving between a limited number of positions in a to and fro motion and change the weights of the game Evaluation dynamically.
 
