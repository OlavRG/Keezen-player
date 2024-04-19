def get_board_value(my_pawns, other_pawns, game_info):
    location_values = [0] * game_info.board_size * 2  # create extra space to account for illegal moves pas board_size
    location_values[0:game_info.board_size + 5] = list(range(0, game_info.board_size + 5))
    location_values[game_info.board_size:game_info.board_size + 3] = [game_info.board_size * (1 + n / 4) for n
                                                                      in range(1, 5)]

    board_value = 0
    for n in range(0, len(my_pawns)):
        board_value += location_values[my_pawns[n].position]

    board_value = int(board_value)
    return board_value
