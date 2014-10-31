import numbers
# ----------------------------------- #
# CLASS TicTacToePlayer               #
#                                     #
# Maintains state of a single player  #
# Will be two instances for one game  #
# ----------------------------------- #
class TicTacToePlayer( object ):

    def __init__(self, name):
        self.__moves = list()
        self.__name = str( name )

    
