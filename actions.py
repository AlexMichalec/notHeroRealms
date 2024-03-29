import random


def gen_add_gold(amount):
    def sub_fun(player):
        player.coins += amount
        print(f"Added {amount} gold.")
    return sub_fun

def gen_attack(power):
    def sub_fun(player):
        player.attack_power += power
        print(f"Attacked by {power}.")
    return sub_fun

def gen_add_health(amount):
    def sub_fun(player):
        player.health += amount
        print(f"Health increased by {amount}.")
    return sub_fun

def draw_card():
    def sub_fun(player):
        player.cards_to_draw += 1
    return sub_fun, "Draw a card."

def draw_2_cards():
    def sub_fun(player):
        player.cards_to_draw += 2
    return sub_fun, "Draw 2 cards."

def opponent_discard():
    def sub_fun(player):
        player.opponent.cards_to_draw -= 1
    return sub_fun, "Opponent discards a card."

def get_coins_or_attack(amount, power):
    def sub_fun(player):
        choice = random.choice((True,False))
        if choice:
            player.coins += amount
        else:
            player.attack_power += power
    return sub_fun, f"get {amount} coins or attack with {power}"

def get_attack_or_health(power,amount):
    def sub_fun(player):
        choice = random.choice((True,False))
        if choice:
            player.health += amount
        else:
            player.attack_power += power
    return sub_fun, f"attack with {power} or get {amount} health"


def can_sacrifice(bonus=0):
    def sub_fun(player):
        player.cards_to_sacrifice = 1
        player.sacrifice_bonus = bonus
    text = "You can sacrifice a card." if bonus == 0 else f"You can sacrifice a card, if you do it, your attack rises by {bonus}"
    return sub_fun, text

def can_sacrifice_two(bonus=0):
    def sub_fun(player):
        player.cards_to_sacrifice = 2
        player.sacrifice_bonus = bonus
    text = "You can sacrifice max 2 cards." if bonus == 0 else f"You can sacrifice max 2 cards, if you do it, your attack rises by {bonus}"
    return sub_fun, text

def reactivate_hero():
    def sub_fun(player):
        player.heroes_to_reactivate += 1
        print("Action Reactivate not ready to use for player")
    return sub_fun, "Reactivate your Hero"

def stun_hero():
    def sub_fun(player):
        player.heroes_to_block += 1
    return sub_fun, "You can block opponent's hero."


def next_bought_on_hand():
    def sub_fun(player):
        player.next_bought_card_on_hand += 1
    return sub_fun, "Put the next bought card on the Hand"

def add_attack_for_hero(power = 1 ):
    def sub_fun(player):
        player.attack_power += len(player.army) * power
    text = f"Add +{power} attack for every hero in your party."
    return sub_fun, text

def add_health_for_hero(k = 1):
    def sub_fun(player):
        player.health += len(player.army) * k
    text = f"Add +{k} health for every hero in your party."
    return sub_fun, text

def next_bought_action_on_the_top_of_deck():
    def sub_fun(player):
        player.next_bought_action_on_top += 1

    return sub_fun, "Put the next bought Action on the top of the deck"

def next_bought_card_on_the_top_of_deck():
    def sub_fun(player):
        player.next_bought_card_on_top += 1

    return sub_fun, "Put the next bought Card on the top of the deck"


def swap_a_card():
    def sub_fun(player):
        player.cards_to_discard = 1
    text = "You can draw a card, if you do, discard another one."
    return sub_fun, text

def swap_two_cards():
    def sub_fun(player):
        player.cards_to_discard = 2
    text = "You can draw max 2 cards, if you do, discard the same amount."
    return sub_fun, text

def attack_for_alliance(alliance):
    def sub_fun(player):
        player.attack_power += len([x for x in player.cards_in_front_of_me + player.army if x.alliance == alliance])-1
    text = f"+1 attack for every other {alliance} card in the game"
    return sub_fun, text

def attack_for_guardian():
    def sub_fun(player):
        player.attack_power += len([x for x in player.army if x.if_guardian == True])-1
    text = f"+1 attack for every other Guardian in your army."
    return sub_fun, text

def resurrect_hero():
    def sub_fun(player):
        player.heroes_to_resurect = 1
    text = "You can take a dead Hero and put them on ur deck top."
    return sub_fun, text

def resurrect_card():
    def sub_fun(player):
        player.cards_to_resurect = 1
    text = "You can take a discarded Card and put it on ur deck top."
    return sub_fun, text

def sample():
    def sub_fun(player):
        pass
    text = ""
    return sub_fun, text

