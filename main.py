from random import shuffle
import string

ALPHABET = list(string.ascii_uppercase)

def letter_to_index(letter: str, base=ALPHABET) -> int:
    return base.index(letter)

def index_to_letter(index: int, base=ALPHABET) -> str:
    return base[index]
    
def decrypt(cipher: str, base: str, clue: str) -> str:
    decrypted_letters = [
        base[letter_to_index(letter, cipher)] for letter in clue
    ]
    
    return ''.join(decrypted_letters)

def build_cipher_solution(clue: str, solution: str, first_letter: str = ' ', last_letter: str =' ', base=ALPHABET, existing_cipher=None) -> list:
    indexes_of_solution = [letter_to_index(letter, base) for letter in solution]
    if existing_cipher:
        cipher = existing_cipher
    else:
        cipher = [first_letter] + [' ' for i in range(1, 25)] + [last_letter]
    for (letter_index, alphabetical_index) in enumerate(indexes_of_solution):
        cipher[alphabetical_index] = clue[letter_index]

    existing_cipher = None
    return cipher

def create_cipher(clue: str, solution: str, first_letter: str = ' ', last_letter: str = ' ', base=ALPHABET, existing_cipher=None) -> str:
    if len(set(clue)) != len(clue):
        raise ValueError(f'Clue {clue} contains duplicate letters')
    if len(set(solution)) != len(solution):
        raise ValueError(f'Solution {solution} contains duplicate letters')

    cipher_solution = build_cipher_solution(clue, solution, first_letter, last_letter, base, existing_cipher)

    unused_indexes = [i for i in range(len(cipher_solution)) if cipher_solution[i] == ' ']
    shuffle(unused_indexes)

    unused_letters = [a for a in base if a not in [*clue, first_letter, last_letter]]

    for index in range(len(unused_indexes)):
        cipher_solution[unused_indexes[index]] = unused_letters[index]
        
    existing_cipher = None
    if len(set(cipher_solution)) != 26:
        print('Duplicates in cipher solution: ', sorted(cipher_solution))
    return ''.join(cipher_solution)

words = [
    'HATRED',
    'MYTHOS',
    'CIPHER',
    'CRYPTS',
    'THROES',
    'ORACLE',
    'FATHOM',
    'JINXED',
    'EMBARK',
    'PHAROS',
    'WIZARD',
    'BANISH',
    'VORTEX',
    'SPIGOT',
    'KNIGHT',
    'ASPECT',
    'BRIGHT',
    'CHISEL',
    'EMBODY',
    'THUMBS',
    'VAULTS',
    'DUPING',
    'DRIVEL',
    'SPRAWL',
    'UNVEIL',
    'ROYALS',
    'BURDEN',
    'SPHINX',
    'WRAITH',
    'BOTANY',
    'FABLED',
    'ENIGMA',
    'SHROUD',
    'GHOSTY',
    'LUCENT',
    'CHARMS',
    'MARVEL',
    'MYSTIC',
    'MOCKER',
    'CURATE',
    'PLACID',
    'TONGUE',
    'DREAMT',
    'SACRED',
    'DRIVEL',
    'MANGLE',
    'RAMBLE',
    'CAVERN',
    'COBALT',
    'SHIVER',
    'PSYCHE',
    'DEVILS',
    'SALUTE',
    'SOLACE',
    'VIRTUE',
    'VANISH',
    'VORTEX',
    'VANITY',
    'SERAPH',
    'SMITHY',
    'PLAGUE',
    'SHRINK',
    'GOBLIN',
    'GOVERN',
    'RECKON',
    'ADRIFT',
    'STRIDE',
    'BURNED',
]


final_word_pairs = [
    ('ETHICS', 'GOLDEN'),
    ('DUKING', 'SILVER'),
    ('DRAGON', 'MORTAL'),
]

clues = []
solutions = []

# The final problem here is that each word pair
# cannot share any letters with the first and final positions!
# I think we need to take a list of all possible words and
# make pairs dynamically, possibly excluding the final 3 pairs
def main():
    # The 2 penultimate pairings must be consistent,
    # and preferably not include the same letters as the final pairing
    (final_clue, final_result) = final_word_pairs[-1]
    (final_first_letter_clue, final_first_letter_result) = final_word_pairs[-3]
    (final_last_letter_clue, final_last_letter_result) = final_word_pairs[-2]

    # Check to make sure we can build a valid final cipher
    for letter in final_clue:
        if letter in final_first_letter_clue:
            print(f'Cannot build cipher; final clue {final_word_pairs[-1][0]} shares letter {letter} with semi-penultimate clue {final_word_pairs[-3][0]}')
            exit(666)
    for letter in final_result:
        if letter in final_last_letter_clue:
            print(f'Cannot build cipher; final result {final_word_pairs[-1][1]} shares letter {letter} with penultimate clue {final_word_pairs[-2][0]}')
            exit(666)

    partial_first_letter_cipher = build_cipher_solution(
        final_first_letter_clue, final_first_letter_result,
    )
    
    partial_last_letter_cipher = build_cipher_solution(
        final_last_letter_clue, final_last_letter_result,
    )

    unused_indexes = [i for i in range(0, 26) if partial_first_letter_cipher[i] == ' ' and partial_last_letter_cipher[i] == ' ']
    shuffle(unused_indexes)
    for i in range(6):
        if partial_first_letter_cipher[unused_indexes[i]] != ' ':
            raise ValueError(f'Conflict at index {unused_indexes[i]} between {partial_first_letter_cipher[unused_indexes[i]]} and {final_clue[i]}')
        partial_first_letter_cipher[unused_indexes[i]] = final_clue[i]

        if partial_last_letter_cipher[unused_indexes[i]] != ' ':
            raise ValueError(f'Conflict at index {unused_indexes[i]} between {partial_last_letter_cipher[unused_indexes[i]]} and {final_result[i]}')

        partial_last_letter_cipher[unused_indexes[i]] = final_result[i]

    for i in range(len(final_clue)):
        partial_first_letter_cipher[unused_indexes[i]] = final_clue[i]
        partial_last_letter_cipher[unused_indexes[i]] = final_result[i]

    # There, now we have our last 2 ciphers that we can work backwards from.
    # We need to map every unused letter in the first one to an unused letter in the second one
    # such that the same letter doesn't map to itself.

    unused_first_cipher_letters = [a for a in ALPHABET if a not in partial_first_letter_cipher]
    shuffle(unused_first_cipher_letters)
    unused_last_cipher_letters = [a for a in ALPHABET if a not in partial_last_letter_cipher]
    shuffle(unused_last_cipher_letters)
    
    first_letter_index = 0
    last_letter_index = 0
    
    # Fill out the other letters in the first- and last-letter ciphers
    for index in range(len(unused_first_cipher_letters)):
        while partial_first_letter_cipher[first_letter_index] != ' ':
            if first_letter_index >= 25:
                break
            first_letter_index += 1
        while partial_last_letter_cipher[last_letter_index] != ' ':
            if last_letter_index >= 25:
                break
            last_letter_index += 1

        # If a letter pairs with itself, swap with another letter.
        # To determine this, we need to cross-check by swapping the indexes

        # Pretend these are our ciphers and unused letters
        # Cipher: [A, B, ' ', C]  --- Unused letters: Y, Z
        # Cipher: [Z, X, Y, ' ']  --- Unused letters: C, D
        # The empty spot in the first cipher cannot become Y, and the empty spot in the second cipher cannot become C,
        # Even though those indexes are not the same number as each other.
        # So we swap Y and Z, and C and D, and we get:
        # Cipher: [A, B, Z, C]
        # Cipher: [Z, X, Y, D]
        if unused_first_cipher_letters[index] == partial_last_letter_cipher[first_letter_index]:
            if index + 1 >= len(unused_first_cipher_letters):
                raise ValueError(f'Cannot find a suitable swap for {unused_first_cipher_letters[index]}')
            swap_index = index + 1
            unused_first_cipher_letters[index], unused_first_cipher_letters[swap_index] = unused_first_cipher_letters[swap_index], unused_first_cipher_letters[index]

        if unused_last_cipher_letters[index] == partial_first_letter_cipher[last_letter_index]:
            if index + 1 >= len(unused_last_cipher_letters):
                raise ValueError(f'Cannot find a suitable swap for {unused_last_cipher_letters[index]}')
            swap_index = index + 1
            unused_last_cipher_letters[index], unused_last_cipher_letters[swap_index] = unused_last_cipher_letters[swap_index], unused_last_cipher_letters[index]   

        partial_first_letter_cipher[first_letter_index] = unused_first_cipher_letters[index]
        partial_last_letter_cipher[last_letter_index] = unused_last_cipher_letters[index]

    first_last_letter_pairs = list(zip(partial_first_letter_cipher, partial_last_letter_cipher))

    ciphers = []
    print('Generating ciphers...')
    for (first, last) in first_last_letter_pairs:
        solution_index = 0
        solution = words[solution_index]
        while 'A' in solution or 'Z' in solution:
            solution_index += 1
            solution = words[solution_index]

        solution = words.pop(solution_index)

        clue_index = 0
        clue = words[clue_index]
        
        while any(letter for letter in clue if letter in [first, last]):
            clue_index += 1
            clue = words[clue_index]
        
        clue = words.pop(clue_index)

        cipher = create_cipher(
            clue=clue,
            solution=solution,
            first_letter=first,
            last_letter=last,
        )
        ciphers.append(cipher)
        clues.append(clue)
        solutions.append(solution)
        
        print(f'{clue} -> {solution} : {cipher}')

    ciphers.append(partial_first_letter_cipher)
    ciphers.append(partial_last_letter_cipher)

    print('First letters: ', ''.join(partial_first_letter_cipher))
    print('Last letters: ', ''.join(partial_last_letter_cipher))

    print('Testing ciphers: ')
    for index in range(len(clues)):
        decrypted_solution = decrypt(ciphers[index], ALPHABET, clues[index])
        print(f'{clues[index]} -> ', decrypted_solution)
        assert(solutions[index] == decrypted_solution)

    print('------------')
    print('Testing first letter cipher:')
    decrypted_solution = decrypt(partial_first_letter_cipher, ALPHABET, final_first_letter_clue)
    print(f'{final_first_letter_clue} -> ', decrypted_solution)
    assert(decrypted_solution == final_first_letter_result)

    print('------------')
    print('Testing last letter cipher:')
    decrypted_solution = decrypt(partial_last_letter_cipher, ALPHABET, final_last_letter_clue)
    print(f'{final_last_letter_clue} -> ', decrypted_solution)
    assert(decrypted_solution == final_last_letter_result)

    print('------------')
    print('Testing final cipher:')
    final_decoded_word = decrypt(partial_first_letter_cipher, partial_last_letter_cipher, final_clue)
    print(f'{final_clue} -> ', final_decoded_word)
    assert(final_result == final_decoded_word)
    
    print('Tests passed.')
    
if __name__ == '__main__':
    main()