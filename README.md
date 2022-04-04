# Othello Game
Note: Magister, we generally understand these matching algorithms but we had difficulties and complications for the implementation. This due to our poor organization of time.
Still, we showed you how short a range we had. Where the MinMax algorithm has a depth of one level (yeah, this is too por ) and manages to interact with the human player guided by the implemented heuristics (explained later)


#### --- Heuristics ----

 utility_function_1
Here we take into account only the number of chips that a player has on the board. But we realized that we did not contemplate the winged game. For example, a player could choose the action whose number of chips is greater than 10 black chips, but we do not take into account the number of chips of the opposite side who might have more than 10 white chips that might have been given due to the action that we take. This action gives more opportunity for the opposing side to win the games.

 utility_function_2

With this heuristic we want to take into account both the number of black and white (opposing player) pieces. Where by performing a subtraction between the two, you could have a better utility and define which action is more convenient for you. Where the best case is represented by the positive number and the worst case by the smallest number. This lower number can become negative, that would mean that there is a greater amount of chips from the opposing player.



####--- Experiments carried out ----
Of 4 games

Application of “utility_function_1” Human Player: 4 - Machine: 0 = Plays: (27-7),(29-9),(41-18),

Application of “utility_function_2” Human Player: 4 – Machine: 0 = Plays: (55-9),(41-21),(36-16),(28-8)



####--- Conclusions ---
Due to the fact that there are two simple heuristics and, the main thing, only a one-level state expansion is carried out, satisfactory results are not obtained. In all cases the human manages to beat the program.


#### ---Installation guide---
You have to run the program "IntelligentProgram.py", and the interaction is done through the console.
