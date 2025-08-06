import random 
from input_validation import validate_input 

def deck_selection(owner_decks, cat_decks):
    ''' Author: Connor Hall
    Techniques: none
    
    prints decks to choose from, takes user input and chooses cat's deck
    
    Args:
        owner_decks (list): list of lists containing owner Card objects
        cat_decks (list): list of lists containing cat Card objects
        
    Side effects:
        prints to stdout
    
    Returns:
        2 lists of Card objects for the owner and the cat
    '''
    valid_inputs = list()
    
    for index, deck in enumerate(owner_decks): # go through each deck
        # print deck number in list
        print(f'Deck {index + 1}')
        valid_inputs.append(index + 1)
        
        for card_num, card in enumerate(deck):
            print(f'{card_num + 1}: {card}')
        print()
    
    input = validate_input("Choose your deck: ", data_type=int, \
        allowed_values=valid_inputs)
    owner_selection = int(input) - 1
    cat_selection = random.choice(cat_decks)
    return owner_selection, cat_selection