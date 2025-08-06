from input_validation import validate_input 

def game_menu(deck, owner, cat):
    ''' author: Jadon
    technique: f-strings
    
    prints game options, enables user to select card for each turn
    
    Args:
        deck (list): list of card objects
        owner (Player object): Player object representation of owner
        cat (Player object): Player object representation of cat
        
    Side effects:
        prints to stdout
        
    Returns:
        Card object
    '''

    option = validate_input("Menu:\
        \nOption 1: select card\
        \nOption 2: show your deck\
        \nOption 3: show stats\
        \nSelect option: ", int, [1, 2, 3])
    
    while option != 1:
        if option == 2:
            print()
            counter = 1
            for card in deck:
                print(f'{counter}: {card}')
                counter += 1
            print()
        elif option == 3:
            print(f"\n{owner}\n{cat}\n")
        option = int(input("Select option: "))
        
    selection = validate_input(f"Select card 1-{len(deck)}: ", int, 
                                    [deck.index(card) + 1 for card in deck]) - 1 
    print()
    
    return deck[selection]
    
   
        