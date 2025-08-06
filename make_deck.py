import re
import random

# info on cards: 
# - attack, defense, buff, debuff
# - all have accuracy and strength points
# 
# damage cards' magnitude comes in tuples with min/max
# defense cards' magnitude is just one number
# buff and debuff cards' magnitude come in %

# card class
class Card:
    """
    Primary author: Benjamin Weber

    Card object that holds all needed values for any given card
    
    Attributes:
        name (str): name of the card
        description (str): description of the card, used during battle
        magnitude (float or tuple of ints): strength of effect of card, tuple 
            listing attack range if attack card, multiplier otherwise
        power_level (int): number representing the strength of the card, used in
            the deck creation algorithm
        accuracy (float): accuracy of card as a percent
    """
    def __init__(self, name, description, type_, magnitude, power_level, 
                 accuracy):
        """
        Author: Benjamin Weber

        creates a Card object
        
        Args:
            name (str): name of the card
            description (str): description of the card, used during battle
            magnitude (float or tuple of ints): strength of effect of card, tuple 
                listing attack range if attack card, multiplier otherwise
            power_level (int): number representing the strength of the card, 
                used in the deck creation algorithm
            accuracy (float): accuracy of card as a percent
        """
        self.name = name
        self.description = description
        self.type = type_
        self.magnitude = magnitude
        self.power_level = power_level
        self.accuracy = accuracy

    def __repr__(self):
        """
        Primary author: Benjamin Weber

        creates a Card formal representation of Card objects, used in testing
        """
        return (
            f'Card Name: {self.name}, Description: {self.description}, '
            f'Type: {self.type}, Magnitude: {self.magnitude}, '
            f'Power Level: {self.power_level}, Accuracy: {self.accuracy}'
        )
    
    def __str__(self):
        """
        Author: Benjamin Weber
        Techniques: magic method

        creates a Card representation of Card objects,
        used when displaying decks
        """
        match self.type:
            case 'attack':
                return (f'{self.name}: does '
                + f'{self.magnitude[0]} to {self.magnitude[1]} damage with '
                + f'{int(self.accuracy*100)}% accuracy')
            case 'defense':
                return (f'{self.name}: adds '
                + f'{self.magnitude} defense with '
                + f'{int(self.accuracy*100)}% accuracy')
            case 'attack buff':
                return (f'{self.name}: add a '
                + f'{int((self.magnitude-1)*100)}% buff to your attack with '
                + f'{int(self.accuracy*100)}% accuracy')
            case 'attack debuff':
                return (f'{self.name}: add a '
                + f"{int(self.magnitude*100)}% debuff to your cats' attack "
                + f'with {int(self.accuracy*100)}% accuracy')
            case 'defense buff':
                return (f'{self.name}: add a '
                + f'{int((self.magnitude-1)*100)}% buff to your defense with '
                + f'{int(self.accuracy*100)}% accuracy')
            case 'defense debuff':
                return (f'{self.name}: add a '
                + f"{int(self.magnitude*100)}% debuff to your cats' defense "
                + f'with {int(self.accuracy*100)}% accuracy')

# deck function
def make_deck(path, max_count, max_power):
    """
    Author: Benjamin Weber
    Technique: regular expressions
    
    Creates multiple decks at the beginning of the game that the user can choose 
    from. Chooses cards with assigned strength points. The sum of these values 
    shoud not go higher than a specified max power level. Every deck should have 
    at least one attack and one buff/debuff card.
    
    Args:
        path (str): path to text file of cards to pull from
        max_count (int): maximum amount of cards that can be in a deck
        max_power (int): maximum total 'power' values of cards 
    """
    deck = list()
    power = 0
    attacks = list()
    buffs = list()

    # read in all the player cards and organize them by type
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            card = re.search('(?P<name>[^;]+);(?P<description>[^;]+);'
                              +'(?P<type>[^;]+);(?P<magnitude>[^;]+);'
                              +'(?P<power_level>[^;]+);(?P<accuracy>[^\n]+)',
                            line)
            
            match card.group('type'):
                case 'attack':
                    
                    mag = card.group('magnitude').split(',')
                    mag = (int(mag[0]),int(mag[1]))
                                        
                    attacks.append(Card(card.group('name'),
                                        card.group('description'),
                                        card.group('type'),
                                        mag,
                                        float(card.group('power_level')),
                                        float(card.group('accuracy')),))
                case 'attack buff' | 'attack debuff' | 'defense buff' | \
                    'defense debuff':
                    buffs.append(Card(card.group('name'),
                                        card.group('description'),
                                        card.group('type'),
                                        float(card.group('magnitude')),
                                        float(card.group('power_level')),
                                        float(card.group('accuracy')),))

    # add one random attack and remove from list
    current_card = attacks.pop(random.randint(0, len(attacks) - 1))
    power += current_card.power_level
    deck.append(current_card)
    
    # add one random buff/debuff and remove from list
    current_card = buffs.pop(random.randint(0, len(buffs) - 1))
    power += current_card.power_level
    deck.append(current_card)
    
    # put together the card lists
    remaining_cards = attacks + buffs

    # sort by power level, highest to lowest
    remaining_cards.sort(key=lambda s: s.power_level, reverse=True)
    
    # add cards until at max power or max card count
    while max_count > len(deck) and remaining_cards:
        
        # remove all cards too strong to fit in the deck
        while remaining_cards and remaining_cards[0].power_level > \
            (max_power - power):
            remaining_cards.pop(0)

        if not remaining_cards:
            break
        
        # select card, if last card in the deck add the strongest remaining card
        if max_count == len(deck) + 1:
            
            strongest_cards = [remaining_cards.pop(0)]
            for card in remaining_cards:
                if card.power_level == strongest_cards[0].power_level:
                    strongest_cards.append(card)
            
            current_card = strongest_cards.pop(random.randint(0, \
                len(strongest_cards) - 1))
            power += current_card.power_level
            deck.append(current_card)
        else:
            current_card = remaining_cards.pop(random.randint(0, \
                len(remaining_cards) - 1))
            power += current_card.power_level
            deck.append(current_card)
        
    return deck

# for testing
if __name__ == "__main__":

    # make 5 decks with max 6 cards and max power level of 15
    decks = list()
    while len(decks) < 5:
        decks.append(make_deck('player_cards.txt', 6, 15))
        
    # print out the decks
    for deck in decks:
        print(f'Deck {decks.index(deck) + 1}:')
        lvl = 0
        for card in deck:
            print(f'\t{card}')
            lvl += card.power_level
            
        print(f'\tTotal deck power level: {lvl}\n')