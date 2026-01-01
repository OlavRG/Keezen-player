# Following moves are in order of priority and should get progressively fewer points:
# Moving last pawn into finish
# Stepping into finish
# Move away from getting (near-certain) tackled
# Spawn new pawn on board if all pawns are in finish or home
# Aansluiten in finish
# Spawn new pawn
# Tackle opponent
# Regular move

def get_board_value(my_pawns, game_info):
    """
    :param my_pawns:
    :param game_info:
    :return:

    board values per pawn, decreasing (example: board_size = 64)

    finish [0-3] = 2 x 64 + 16, 32, 48, 64
    start [start] = 1 x 64 + 33
    board [start+1 to start-1] =  1 x 64 + 0 to 63
    home = 0
    """

    start_position = my_pawns[0].start_position
    position_values = [0] * game_info.board_size * 3  # create extra space to prevent index errors of moves past board_size
    finish_values = [0] * game_info.board_size

    # Assign values
    position_values[0:game_info.board_size-1] = [1 * game_info.board_size + ((position - start_position) % game_info.board_size) for position in range(game_info.board_size)]
    position_values[start_position] = 2 * game_info.board_size - 2 * game_info.board_size_per_player + 1

    finish_values[0:game_info.pawns_per_player-1] = [2 * game_info.board_size + n * game_info.board_size_per_player for n in range(1, game_info.pawns_per_player+1)]

    board_value = 0
    for pawn in my_pawns:
        if pawn.home:
            board_value += 0
        elif pawn.finish:
            board_value += finish_values[pawn.position]
        else:
            board_value += position_values[pawn.position]

    return int(board_value)
