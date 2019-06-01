import os
import string
import random

from boggle.settings import GRID_SIZE, BASE_DIR


def load_test_board():
    test_board_dir = os.path.join(BASE_DIR, 'boggle/test_board.txt')
    with open(test_board_dir, 'r') as f:
        input_str = f.read()
        board = input_str.strip()

    return board

def get_random_board():
    board = [random.choice(string.ascii_letters) for i in range(GRID_SIZE * GRID_SIZE)]
    return ', '.join(board)

def load_game_state(board):
    game_state = []
    current_row = []
    for index, tile in enumerate(board.split(", ")):
        current_row.append(tile)
        if index % GRID_SIZE == GRID_SIZE - 1:
            game_state.append(current_row)
            current_row = []
    return game_state


def is_word_in_dictionary(word):
    dictionary_dir = os.path.join(BASE_DIR, 'boggle/dictionary.txt')
    with open(dictionary_dir, 'r') as f:
        words = set(word.strip() for word in f.readlines())

        if word.lower() in words:
            return True
    return False


def is_word_valid(game_state, word):
    for index_y, row in enumerate(game_state):
        for index_x, character in enumerate(row):
            if character == '*' or character.upper() == word[0]:
                valid = _recursive_validate_input(
                    game_state, word[1:], (index_x, index_y))
                if valid:
                    break
        if valid:
            break
    return valid


def _recursive_validate_input(game_state, remaining_characters, current_position):
    if len(remaining_characters) == 0:
        return True

    index_x, index_y = current_position

    min_adjacent_x = max(index_x - 1, 0)
    max_adjacent_x = min(index_x + 1, GRID_SIZE - 1)

    min_adjacent_y = max(index_y - 1, 0)
    max_adjacent_y = min(index_y + 1, GRID_SIZE - 1)

    first_character = remaining_characters[0]

    valid = False
    for curr_y in range(min_adjacent_y, max_adjacent_y + 1):
        for curr_x in range(min_adjacent_x, max_adjacent_x + 1):
            if curr_x == index_x and curr_y == index_y:
                continue
            current_character_to_compare = game_state[curr_y][curr_x]
            if current_character_to_compare in ("*", first_character):
                valid = _recursive_validate_input(
                    game_state, remaining_characters[1:], (curr_x, curr_y))
                if valid:
                    break
        if valid:
            break

    return valid
