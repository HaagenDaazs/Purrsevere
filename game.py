import random
import sys
from argparse import ArgumentParser
from deck_selection import deck_selection
from make_deck import make_deck
from game_menu import game_menu

class Player:
    """
    Primary author: Hagan Yeoh.
    
    Represents a player in the game, with health, attack, and defense 
    multipliers, used for calculating combat outcomes and stat changes.

    Attributes:
        name (str): The name of the player (default: "Player").
        health (int): The player's current health points (default: 100).
        attack_multiplier (float): Modifier applied to outgoing damage 
            (default: 1.0).
        defense_multiplier (float): Modifier applied to incoming damage 
            (default: 1.0).
        fearCount (int): Tracks whether the cat should react defensively 
            (default: 1).
    """
    
    def __init__(self, name="Player", health=100):
        """
        Primary author: Hagan Yeoh
        
        Initializes a Player object with a name, health, and default stat 
        multipliers.

        Args:
            name (str, optional): The player's name.
            health (int, optional): The player's starting health.
        """
        self.name = name
        self.health = health
        self.attack_multiplier = 1.0
        self.defense_multiplier = 1.0
        self.fearCount = 1

    def change_stat(self, stat, multiplier):
        """
        Primary author: Hagan Yeoh
        
        Changes the player's attack or defense stat by multiplying it with a 
        given factor.

        Args:
            stat (str): Either "attack" or "defense".
            multiplier (float): The value to multiply the selected stat by.

        Raises:
            ValueError: If an invalid stat name is provided.
        """    
        if stat == 'attack':
            self.attack_multiplier *= multiplier
        elif stat == 'defense':
            self.defense_multiplier *= multiplier
        else:
            raise ValueError("Invalid stat; choose 'attack' or 'defense'")

    def is_defeated(self):
        """
        Primary author: Hagan Yeoh
        
        Checks if the player's health is zero or below.

        Returns:
            bool: True if player is defeated, False otherwise.
        """
        if self.health <= 0:
            return True
        else:
            return False

    def __str__(self):
        """
        Primary author: Hagan Yeoh
        
        Returns a string representation of the player's current stats.

        Returns:
            str: A readable summary of health and stat multipliers.
        """
        return (
            f"{self.name}: HP = {self.health}, Attack Multiplier = "
            + f"{round(self.attack_multiplier, 2)}, " +
            f"Defense Multiplier = {round(self.defense_multiplier, 2)}"
        )


def turn_history(user, card, effect, turn, health, landed):
    """author: Dhawal
    technique: with statement
    
    Logs the turn history and effects to a file

    Args:
        user (Player object): the current user playing
        card (card object): the current card
        effect (int): the effect of the card
        turn (int): The current turn number
        health (int): the health of the targeted player
            
    Side effects:
        writing to turn_history.txt
    """
    try:
        with open("turn_history.txt", "a", encoding="utf-8") as file:
            file.write(f"Turn {turn}\n")
            if landed == True:
               file.write(f"{user} used {card} with effect {effect}\n")
            else:
                file.write(f"{user} used {card} but missed\n")
            file.write("")
            if health == 0:
                file.write("_____ end of game ____\n")
    except:
        print("Error writing to log file")


def resolve_attack(card_accuracy, damage_range, user_multiplier=1.0, 
                   defender_multiplier=1.0):
    """
    Primary author: Hagan Yeoh, Skill demonstrated: Optional Parameters
    
    Resolves whether an attack hits and calculates the damage dealt based on 
    accuracy,
    damage range, and the respective stat multipliers of the attacker and 
    defender.

    This function includes optional parameters for user and defender multipliers
    to allow flexible scaling of damage logic without requiring additional 
    arguments in simple cases.

    Args:
        card_accuracy (float): A float between 0 and 1 representing base 
        accuracy.
        damage_range (range or tuple): Range or tuple indicating possible damage 
        values.
        user_multiplier (float, optional): Attacker's attack multiplier 
        (default is 1.0).
        defender_multiplier (float, optional): Defender's defense multiplier 
        (default is 1.0).

    Returns:
        tuple: A tuple (bool, int) indicating whether the attack landed and how 
        much damage it caused.
    """
    card_accuracy *= 100
    rng = random.random() * 100
    if rng >= card_accuracy:
        return False, 0

    if isinstance(damage_range, range):
        damage = random.randint(damage_range.start, damage_range[-1])
    elif isinstance(damage_range, tuple) and len(damage_range) == 2:
        damage = random.randint(damage_range[0], damage_range[1])
    else:
        raise ValueError("damage_range must be a range or a tuple of length 2")

    damage = int(damage * user_multiplier / defender_multiplier)
    return True, damage


def apply_card_effect(card, user, target, turn):
    """
    Primary author: Hagan Yeoh, Skill demonstrated: Sequence Unpacking
    
    Applies the effects of a given card from one player to another. 
    Handles attacks, stat buffs, and debuffs, and prints the outcomes of 
    those actions.

    This function uses sequence unpacking to retrieve the result of an attack 
    operation, increasing code clarity and separating logic cleanly into 
    reusable parts.

    Args:
        card (Card): The card object being used by the user.
        user (Player): The Player using the card.
        target (Player): The opponent receiving the effect.

    Side effects:
        Modifies player stats or health in place.
        Prints the result of the card usage.
    """
    landed = True
    accuracy = card.accuracy * 100
    rng = random.random() * 100
    if rng >= accuracy:
        landed = False
        
    if card.type == 'attack':
        hit, dmg = resolve_attack(
            card.accuracy,
            card.magnitude,
            user.attack_multiplier,
            target.defense_multiplier
        )
        if hit:
            target.health -= dmg
            if target.health <= 0:
                target.health = 0
            print(f"{card.description}. Hits for {dmg} damage! "
                + f"{target.name} has {target.health} health left.")
        else:
            print(f"{user.name}'s {card.name} missed!")
            
        turn_history(user.name, card.name, dmg, turn, \
            target.health, landed)
    
    else:    
        if card.type == 'attack buff' and landed:
            user.change_stat('attack', card.magnitude)
            print(f"{card.description}. {user.name}'s attack buffed by "
                f"{card.magnitude}")
        elif card.type == 'attack debuff' and landed:
            target.change_stat('attack', 1.0 * (1 - card.magnitude))
            print(f"{card.description}. {target.name}'s attack debuffed by "
                f"{card.magnitude}")
        elif card.type == 'defense buff' and landed:
            user.change_stat('defense', card.magnitude)
            print(f"{card.description}. {user.name}'s defense buffed by "
                f"{card.magnitude}")
        elif card.type == 'defense debuff' and landed:
            target.change_stat('defense', 1.0 * (1 - card.magnitude))
            print(f"{card.description}. {target.name}'s defense debuffed by "
                f"{card.magnitude}")
        elif not landed:
            print(f"{user.name}'s {card.name} missed!")
        else:
            print(f"Unknown card type: {card.type}")
        
        turn_history(user.name, card.name, card.magnitude, turn, \
            target.health, landed)


def computer_card_draw(owner_hp, cat_hp, cat_deck, owner_deck, cat):
    """Author: Connor Hall
    Techniques: list comprehensions, key function with max()
    
    Determines which card the computer (cat) draws. Prioritizes defense
    (if computer can be defeated in one turn), then attack (if owner can be
    defeated in one turn), then either attack or a powerup
    
    Args: 
        owner_hp (int): health points of the owner (player)
        cat_hp (int): health points of the cat (computer)
        cat_deck (list): list of cat's card objects
        owner_deck (list): list of owner's card objects
        cat (Player object): Player object representation of the cat
                        
    Side effects:
        None
        
    Returns:
        card object
    """
    cat_attacks = [card for card in cat_deck if card.type == 'attack']
    cat_powerups = [card for card in cat_deck if card.type[-4:] == 'buff']
    owner_attacks = [card for card in owner_deck if card.type == 'attack']
    
    # raise defense when owner is close to defeating the cat
    cat_defense = [card for card in cat_powerups if card.type == 'defense buff']
    if cat.fearCount == 1:
        if len(cat_defense) > 0:
            for attack in owner_attacks:
                if max(attack.magnitude) * 2 >= cat_hp:
                    cat_defense.sort(key=lambda c: c.magnitude, reverse=True)
                    cat.fearCount += 1
                    print("Cat is afraid! He enrages and shows his meow-scles!")
                    return cat_defense[0]
            
    #draw attack card if can defeat owner 
    #chooses strongest possible attack for increased chance of winning 
    cat_attacks.sort(key=lambda c: max(c.magnitude), reverse=True)
    if max(cat_attacks[0].magnitude) >= owner_hp:
        return cat_attacks[0]
        
    #choose between attack and powerup, greater chance of attack
    if random.random() < 0.7 or len(cat_powerups) == 0:
        return random.choice(cat_attacks)
    else:
        return random.choice(cat_powerups)


def parse_args(arglist):
    """Author: Dhawal Patel
    Techniques: ArgumentParser
    
    parses command line arguments
    
    Optional arguments:
        -d, --difficulty: specify the difficulty of the battle
        -l, --length: specify the lenght of the game
    
    Args:
        arglist (list of str): arguments from the command line
        
    Returns:
        namespace: the parsed arguments as a namespace
    """
    parser = ArgumentParser()
    parser.add_argument("-d", "--difficulty", type=str, default="easy",
        choices=["easy", "hard"], 
        help="difficulty of the game, options are 'easy' and 'hard'")
    parser.add_argument("-l", "--length", type=str, default="short",
        choices=["short", "long"],
        help="length of the game, options are 'short' and 'long'")
    
    return parser.parse_args(arglist)


if __name__ == "__main__":
    '''
    runs the game
    
    ASCII art found at https://www.asciiart.eu/animals/cats
    '''
    
    args = parse_args(sys.argv[1:])
    
    print('\nWelcome to Purrsevere!\n')

    print(r'''_._     _,-'""`-._
(,-.`._,'(       |\`-/|
    `-.-' \ )-`( , o o)
          `-    \`_`"'-''')
    
    print('\nStart by choosing a deck:')
    
    # make 3 player decks and 3 cat decks
    player_decks = list()
    while len(player_decks) < 3:
        player_decks.append(make_deck('player_cards.txt', 6, 15))

    cat_decks = list()
    while len(cat_decks) < 3:
        cat_decks.append(make_deck('cat_cards.txt', 6, 15))
    
    player_deck, cat_deck = deck_selection(player_decks, cat_decks)
    player_deck = player_decks[player_deck]
    
    if args.length == "short":
        player_hp = 100
        cat_hp = 100
    else:
        player_hp = 500
        cat_hp = 500
    if args.difficulty == "hard":
        cat_hp += 100
        
    player = Player("Player", player_hp)
    cat = Player("Cat", cat_hp)
    count = 1
    
    while not cat.is_defeated():
        print(f"_____________________________________________________________\n"
              + f"\nTurn {count}\n")
        card = game_menu(player_deck, player, cat)
        apply_card_effect(card, player, cat, count) 
        if cat.is_defeated():
            print("You win!\n")
            print(r'''      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)''')
            break
        computerTurn = computer_card_draw(player.health, cat.health, 
                                          cat_deck, player_deck, cat)
        apply_card_effect(computerTurn, cat, player, count)
        if player.is_defeated():
            print("Cat wins!\n")
            print(r'''    |\__/,|   (`\\
  _.|o o  |_   ) )
-(((---(((--------''')
            break
        
        count += 1