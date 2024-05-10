def get_board_value(my_pawns, other_pawns, game_info):
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
