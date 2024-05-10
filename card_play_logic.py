from is_card_play_legal import is_card_play_legal
import copy
from board_value import get_board_value
from card import Card


def check_for_tackled_pawn_and_move_them_home(my_pawn, my_pawns, other_pawns):
    my_other_pawns = [value for value in my_pawns if value != my_pawn]
    for target_pawn in my_other_pawns + other_pawns:
        if my_pawn.position == target_pawn.position:
            target_pawn.move_home()


def create_card_play(card, my_pawn, target_pawn, move_value, card_play_is_legal, board_value):
    return {"card": card, "primary_pawn": my_pawn,
            "secondary_pawn": target_pawn, "primary_move": move_value,
            "card_play_is_legal": card_play_is_legal,
            "board_value": board_value}


def play_any_card_on_a_pawn_and_resolve_outcome(card, my_pawn, my_other_pawns, other_pawns, game_info,
                                                card_plays_on_pawns_and_outcomes,
                                                target_pawn=None, move_1=None):
    position_1 = my_pawn.position
    if move_1:
        move_value = move_1
        move_2 = card.move_value - move_1
    else:
        move_value = card.move_value
        move_2 = None

    if target_pawn:
        position_2 = target_pawn.position
    else:
        position_2 = None

    # move pawns according to move values
    my_pawn.move_by_card(card, game_info, move_from_7=move_1, jack_other_pawn_position=position_2)
    if target_pawn:
        target_pawn.move_by_card(card, game_info, move_from_7=move_2, jack_other_pawn_position=position_1)
    else:
        pass

    # check if move is legal
    card_play_is_legal_p1 = is_card_play_legal(my_pawn, my_other_pawns, other_pawns,
                                               move_value, game_info)

    # check legality for target pawn
    if target_pawn:
        other_pawns_owned_by_target = [pawn for pawn in [my_pawn] + my_other_pawns + other_pawns if
                                       pawn.color == target_pawn.color and pawn != target_pawn]
        pawns_not_owned_by_target = [pawn for pawn in [my_pawn] + my_other_pawns + other_pawns if
                                     pawn.color != target_pawn.color]
        card_play_is_legal_p2 = is_card_play_legal(target_pawn, other_pawns_owned_by_target, pawns_not_owned_by_target,
                                                   move_2, game_info)
    else:
        card_play_is_legal_p2 = True

    card_play_is_legal = card_play_is_legal_p1 & card_play_is_legal_p2

    # If a pawn was tackled during move, move it off the board here. This must be done after card_play_is_legal, since
    # that function checks for protected pawns being illegally tackled
    check_for_tackled_pawn_and_move_them_home(my_pawn, [my_pawn] + my_other_pawns, other_pawns)
    if target_pawn:
        other_pawns_owned_by_target = [pawn for pawn in [my_pawn] + my_other_pawns + other_pawns if
                                       pawn.color == target_pawn.color and pawn != target_pawn]
        pawns_not_owned_by_target = [pawn for pawn in [my_pawn] + my_other_pawns + other_pawns if
                                     pawn.color != target_pawn.color]
        check_for_tackled_pawn_and_move_them_home(target_pawn, other_pawns_owned_by_target, pawns_not_owned_by_target)

    for pawn in [my_pawn] + my_other_pawns + other_pawns:
        pawn.reset_start_of_turn_bools_for_next_turn()

    # mark that card has been played for testing
    card.set_play_status(True)

    # get board value
    board_value = get_board_value([my_pawn] + my_other_pawns, other_pawns, game_info)
    card_plays_on_pawns_and_outcomes.append([create_card_play(card, my_pawn, target_pawn,
                                                              move_value, card_play_is_legal, board_value)])

    return card_plays_on_pawns_and_outcomes, [my_pawn] + my_other_pawns, other_pawns


def reset_to_previous_state(backup_pawns, pawns):
    for pawn_number in range(len(pawns)):
        pawns[pawn_number].__dict__.update(backup_pawns[pawn_number].__dict__)


# test the outcome of a play without playing it (like playing it in your mind)
def test_all_possible_plays(player, my_pawns, other_pawns, hand, game_info):
    backup_player = copy.deepcopy(player)
    my_backup_pawns = copy.deepcopy(my_pawns)
    other_backup_pawns = copy.deepcopy(other_pawns)
    backup_hand = copy.deepcopy(hand)
    card_plays_on_pawns_and_outcomes = []
    for card in hand:
        if not card.has_been_played:
            for my_pawn in my_pawns:
                my_other_pawns = [value for value in my_pawns if value != my_pawn]
                if card.is_splittable:
                    play_any_card_on_a_pawn_and_resolve_outcome(card, my_pawn, my_other_pawns,
                                                                other_pawns, game_info,
                                                                card_plays_on_pawns_and_outcomes,
                                                                target_pawn=None, move_1=None)
                    # reset pawns back to original position
                    reset_to_previous_state(my_backup_pawns, my_pawns)
                    reset_to_previous_state(other_backup_pawns, other_pawns)
                    card.set_play_status(False)
                    for my_other_pawn in my_other_pawns:
                        for move_1 in range(1, card.move_value):
                            play_any_card_on_a_pawn_and_resolve_outcome(card, my_pawn, my_other_pawns,
                                                                        other_pawns, game_info,
                                                                        card_plays_on_pawns_and_outcomes,
                                                                        target_pawn=my_other_pawn, move_1=move_1)
                            # reset pawns back to original position
                            reset_to_previous_state(my_backup_pawns, my_pawns)
                            reset_to_previous_state(other_backup_pawns, other_pawns)
                            card.set_play_status(False)

                elif card.rank == 'J':
                    for other_pawn in other_pawns:
                        play_any_card_on_a_pawn_and_resolve_outcome(card, my_pawn, my_other_pawns,
                                                                    other_pawns, game_info,
                                                                    card_plays_on_pawns_and_outcomes,
                                                                    target_pawn=other_pawn, move_1=None)

                        # reset pawns back to original position
                        reset_to_previous_state(my_backup_pawns, my_pawns)
                        reset_to_previous_state(other_backup_pawns, other_pawns)
                        card.set_play_status(False)

                else:
                    play_any_card_on_a_pawn_and_resolve_outcome(card, my_pawn, my_other_pawns,
                                                                other_pawns, game_info,
                                                                card_plays_on_pawns_and_outcomes,
                                                                target_pawn=None, move_1=None)

                    # reset pawns back to original position
                    reset_to_previous_state(my_backup_pawns, my_pawns)
                    reset_to_previous_state(other_backup_pawns, other_pawns)
                    card.set_play_status(False)
        else:
            pass
    return card_plays_on_pawns_and_outcomes


def test_next_round_card_plays(player, my_pawns, other_pawns, game_info, card_play):
    next_round_hand = []
    all_unique_cards = 'A23456789XJQK'
    for card in all_unique_cards:
        next_round_hand.append(Card(card))
    next_round_plays = test_all_possible_plays(player, my_pawns, other_pawns, next_round_hand, game_info)
    card_plays_up_to_next_round = []
    for next_round_play in next_round_plays:
        old_and_new_play = card_play + next_round_play
        card_plays_up_to_next_round.append(old_and_new_play)
    return card_plays_up_to_next_round


def test_all_possible_follow_up_plays(player, my_pawns, other_pawns, hand, game_info, previous_turn_legal_plays,
                                      all_dead_plays):
    all_card_plays = []
    my_backup_pawns = copy.deepcopy(my_pawns)
    other_backup_pawns = copy.deepcopy(other_pawns)
    backup_hand = copy.deepcopy(hand)
    for card_play in previous_turn_legal_plays:
        for turn in range(0,len(card_play)):
            my_other_pawns = [value for value in my_pawns if value != card_play[turn]["primary_pawn"]]
            play_any_card_on_a_pawn_and_resolve_outcome(card_play[turn]["card"],
                                                        card_play[turn]["primary_pawn"],
                                                        my_other_pawns, other_pawns, game_info,
                                                        [],
                                                        target_pawn=card_play[turn]["secondary_pawn"],
                                                        move_1=card_play[turn]["primary_move"])
        new_card_plays_from_single_previous_play = test_all_possible_plays(player, my_pawns, other_pawns, hand,
                                                                           game_info)
        # if previous turn play has no follow up, check the value of its next round
        legal_new_card_plays_from_single_previous_play = [new_card_play for new_card_play in
                                                          new_card_plays_from_single_previous_play if
                                                          new_card_play[0]["card_play_is_legal"]]
        if not legal_new_card_plays_from_single_previous_play:
            all_dead_plays_incl_illegal = test_next_round_card_plays(player, my_pawns, other_pawns, game_info, card_play)
            all_dead_plays += [play for play in all_dead_plays_incl_illegal if play[-1]["card_play_is_legal"]]
            # Putting the last pawn in finish leaves no legal new card plays. Hence we check separately for a winning move
            if all([pawn.finish for pawn in my_pawns]):
                all_dead_plays += [card_play]
        else:
            pass

        # reset test pawns and hand for following loop
        reset_to_previous_state(my_backup_pawns, my_pawns)
        reset_to_previous_state(other_backup_pawns, other_pawns)
        reset_to_previous_state(backup_hand, hand)

        # Append the previous play and new play in the same sublist
        for new_turn_card_play in new_card_plays_from_single_previous_play:
            old_and_new_play_from_single_previous_play = card_play + new_turn_card_play
            all_card_plays.append(old_and_new_play_from_single_previous_play)

    # filter all illegal plays
    all_legal_card_plays = [card_play for card_play in all_card_plays if card_play[-1]["card_play_is_legal"]]

    return all_legal_card_plays, all_dead_plays


def pick_play_with_highest_eventual_board_value(all_plays):
    highest_value = 0
    best_play = None
    for play in all_plays:
        if play[-1]["board_value"] > highest_value:
            highest_value = play[-1]["board_value"]
            best_play = play
        else:
            pass
    return best_play


def card_play_to_dict(card_play):
    # check if there is any legal play
    if not card_play:
        card_play_dict = None
        return card_play_dict
    else:
        card_play = card_play[0]
    if card_play["secondary_pawn"]:
        secondary_pawn_color = card_play["secondary_pawn"].color
        secondary_pawn_position = card_play["secondary_pawn"].position_from_own_start
    else:
        secondary_pawn_color = None
        secondary_pawn_position = None
    card_play_dict = {"card": card_play["card"].rank,
                      "primary_pawn_color": card_play["primary_pawn"].color,
                      "primary_pawn_position": card_play["primary_pawn"].position_from_own_start,
                      "secondary_pawn_color": secondary_pawn_color,
                      "secondary_pawn_position": secondary_pawn_position,
                      "primary_move": card_play["primary_move"]}
    return card_play_dict


def check_if_client_card_play_is_legal(player, my_pawns, other_pawns, hand, game_info, card_play_dict):
    # If the client returned None, it means they can play no card. Test this first
    if not card_play_dict:
        pass
    else:
        pass

    legal = False
    legal_card = False
    legal_color = False
    legal_pawn = False

    # First check if the player actually is the right color and has the card in hand
    if card_play_dict["card"] in [card.rank for card in hand]:
        legal_card = True
    if card_play_dict["primary_pawn_color"] == player.color:
        legal_color = True

    # check if the player has a pawn on the position of play
    legal_pawn = any([True for pawn in my_pawns if pawn.position_from_own_start == card_play_dict["primary_pawn_position"]])

    card = next((card for card in hand if card.rank == card_play_dict["card"]), None)
    my_pawn = next((pawn for pawn in my_pawns if pawn.position_from_own_start == card_play_dict["primary_pawn_position"]), None)
    my_other_pawns = [value for value in my_pawns if value != my_pawn]
    target_pawn = next((pawn for pawn in my_pawns + other_pawns if
                        pawn.position_from_own_start == card_play_dict["secondary_pawn_position"] and
                        pawn.color == card_play_dict["secondary_pawn_color"]
                        ), None)
    if card.is_splittable and target_pawn:
        move_1 = card_play_dict["primary_move"]
    else:
        move_1 = None

    card_play = play_any_card_on_a_pawn_and_resolve_outcome(card, my_pawn, my_other_pawns, other_pawns, game_info,
                                                            [], target_pawn, move_1)[0]
    return card_play[0][0]["card_play_is_legal"]
