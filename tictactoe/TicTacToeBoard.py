# ----------------------------------- #
# CLASS TicTacToeBoard                #
#                                     #
# Maintains state of game board       #
# ----------------------------------- #
class TicTacToeBoard( object ):

    SIZE = 3
    X = {0, 1, 2}
    Y = {0, 1, 2}

    def __init__( self ):
        # Create board matrix: 3x3
        self.__board = [ [ 0 for x in range( TicTacToeBoard.SIZE ) ] for x in range( TicTacToeBoard.SIZE ) ]

# ----------------------------------- #
