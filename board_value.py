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
    location_values = [0] * game_info.board_size * 3  # create extra space to prevent index errors of moves past board_size
    location_values[0:game_info.board_size + 5] = list(range(1, game_info.board_size + 4))
    location_values[game_info.board_size:game_info.board_size + 3] = [game_info.board_size * (1 + n / 4) for n
                                                                      in range(1, 5)]

    board_value = 0
    for pawn in my_pawns:
        if not pawn.home:
            board_value += location_values[pawn.position]
        else:
            pass

    return int(board_value)
