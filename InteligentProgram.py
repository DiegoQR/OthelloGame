from os import stat
from unittest import result
from OthelloGame import Board, Game, Player

class PlayerAI(Player):
    def __init__(self, tokenColor):
        super().__init__(tokenColor)

class State:
    def __init__(self, fatherState, game):
        self.fatherState = fatherState
        self.game = game
        self.utility = None
    
    def __gt__(self, other):
        if self.utility > other.utility:
            return True
        else:
            return False

    def __str__(self):
        return self.game.board_status()

    def utility_function_1(self, state, actualPlayer):
        actualGame = state.game
        utility = actualGame.get_player_score(actualPlayer)
        return utility
    
    def utility_function_2(self, state, actualPlayer, enemyPlayer):
        actualGame = state.game
        playerScore = actualGame.get_player_score(actualPlayer)
        enemyScore = actualGame.get_player_score(enemyPlayer)
        utility = playerScore - enemyScore
        return utility

    def expand_states(self, player):
        expandedStates = []
        actions = self.game.define_posible_actions(player)
        for action in actions:
            newGame = self.game.copy()
            newGame.do_player_turn(player, (action.posX, action.posY))
            childState = State(self, newGame)
            expandedStates.append(childState)
        return expandedStates, actions
    
    def terminal_test(self, player):
        actions = self.game.define_posible_actions(player)
        return len(actions) == 0
    
    def define_utility(self, player, enemyPlayer):
        self.utility = self.utility_function_1(self, player)
        #self.utility = self.utility_function_2(self, player, enemyPlayer)
            


class GameTree:
    def __init__(self, initialState, maxDepth):
        self.initalState = initialState
        self.maxDepth = maxDepth
        self.leafsList = list()
    
    def max_value(self, state, player, enemyPlayer):
        if(state.terminal_test(player)):
            return state.define_utility(player, enemyPlayer)
        min = -1000
        childStates, actions = state.expand_states(player)
        i = 0
        actionMin = None
        for state in childStates:
            state.define_utility(player, enemyPlayer)
            if(state.utility > min):
                min = state.utility
                actionMin = actions[i]
            i += 1
            # max = min(max, self.max_value(state, player, enemyPlayer))
        return actionMin
    
    def max_value_2(self, state, player, enemyPlayer):
        if(state.terminal_test(player)):
            return state.define_utility(player, enemyPlayer)
        min = -1000
        childStates, _ = state.expand_states(player)
        for state in childStates:
            min = max(min, self.min_value(state, player, enemyPlayer))
        return max
    
    def min_value(self, state, player, enemyPlayer):
        if(state.terminal_test(player)):
            return state.define_utility(player, enemyPlayer)
        max = 1000
        childStates, actions = state.expand_states(player)
        i = 0
        actionMax = None
        for state in childStates:
            state.define_utility(player, enemyPlayer)
            if(state.utility < max):
                max = state.utility
                actionMax = actions[i]
            i += 1
            # max = min(max, self.max_value(state, player, enemyPlayer))
        return actionMax
    
    # black = MAX, white = MIN
    def min_max_desicion(self, state, player, enemyPlayer):
        if(player.tokenColor == "white"):
            max = self.min_value(state, player, enemyPlayer)
            return max
        else:
            min = self.max_value(state, player, enemyPlayer)
            return min
    
    def expand_tree(self, player, enemyPlayer):
        return self.expand_tree_recursive(self.initalState, player, enemyPlayer, self.maxDepth)

    def expand_tree_recursive(self, state, player, enemyPlayer, limit):
        if(limit % 2 == 0):
            actualPlayer = player
            conraryPlayer = enemyPlayer
        if(limit % 2 == 1):
            actualPlayer = enemyPlayer
            conraryPlayer = player
        if(limit == 0):
            state.define_utility(actualPlayer, conraryPlayer)
            self.leafsList.append(state)
            #print(f"state: \n {state} \n limit: {limit} \n utility: {state.utility}")
            return True
        else:
            childStates, _ = state.expand_states(actualPlayer)
            for state in childStates:
                result = self.expand_tree_recursive(state, player, enemyPlayer, limit-1)
            return result

    def best_utility_state(self):
        return self.leafsList


def play_game():
    board = Board()
    board.initializate_board()
    playerOne = Player("black")
    playerTwoAI = PlayerAI("white")
    game = Game(board)
    game.initializate_default_game()
    initialState = State(None, game)
    print(initialState)
    gameTree = GameTree(initialState, 10)
    #gameTree.expand_tree(playerOne, playerTwoAI)
    playerTurn = playerOne
    charToNumb = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7
        }
    while (game.terminal_test(playerTurn) == False):
        print(f"Score Black: {game.get_player_score(playerOne)} - Score White: {game.get_player_score(playerTwoAI)}")
        actions = game.define_posible_actions(playerOne)
        print(f"Your possible actions are: {[str(cell) for cell in actions]}")
        validMovement = False
        while(validMovement == False):
            posX = input("Enter the position X: ")
            posY = input("Enter the position Y: ")
            validMovement = playerOne.do_a_movement(game, (charToNumb[posX], int(posY) - 1))
        print(game.board_status())
        state = gameTree.min_max_desicion(initialState, playerTwoAI, playerOne)
        print(state)
        playerTwoAI.do_a_movement(game, (state.posX, state.posY))
        print(game.board_status())
    print(f"Score Black: {game.get_player_score(playerOne)} - Score White: {game.get_player_score(playerTwoAI)}")

play_game()