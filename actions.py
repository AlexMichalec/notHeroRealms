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
        return
        x = input("Do you want to sacrifice a card?(yes/no)").lower()
        while x not in ("yes","y","no","n"):
            x = input("type yes or no")
        if x[0] == "n":
            return

        print("Choose card to sacrifice:")
        for i, card in enumerate(player.cards_in_front_of_me+player.deck.discarded):
            print(i+1,card.name)

        x = input()
        while x not in [str(x+1) for x in range(len(player.cards_in_front_of_me+player.deck.discarded))]:
            x = input("type correct number")

        x = int(x)-1
        player.to_sacrifice.append((player.cards_in_front_of_me+player.deck.discarded)[x])
        player.attack_power += bonus
    text = "You can sacrifice a card." if bonus == 0 else f"You can sacrifice a card, if you do it, your attack rises by {bonus}"
    return sub_fun, text

def can_sacrifice_two(bonus=0):
    def sub_fun(player):
        print("Sacrifising not ready yet")
        return
    text = "You can sacrifice max 2 cards." if bonus == 0 else f"You can sacrifice max 2 cards, if you do it, your attack rises by {bonus}"
    return sub_fun, text

def reactivate_hero():
    def sub_fun(player):
        print("Action Reactivate not ready to use")
    return sub_fun, "Reactivate your Hero"

def stun_hero():
    def sub_fun(player):
        if len(player.opponent.army) >0:
            card = random.choice(player.opponent.army)
            player.opponent.army.remove(card)
            player.opponent.deck.add_to_discarded(card)
            print(f"{card.name} was stuned")
    return sub_fun, "You can stun opponent's hero."


def next_bought_on_hand():
    def sub_fun(player):
        player.next_bought_card_on_hand += 1
    return sub_fun, "Put the next bought card on the Hand"

def add_attack_for_hero(power = 1 ):
    def sub_fun(player):
        player.attack_power += len(player.army) * power
    text = f"Add +{power} attack for every hero in you army."
    return sub_fun, text

def add_health_for_hero(k = 1):
    def sub_fun(player):
        player.health += len(player.army) * k
    text = f"Add +{k} health for every hero in you army."
    return sub_fun, text

def next_bought_action_on_the_top_of_deck():
    def sub_fun(player):
        player.next_bought_action_on_top += 1

    return sub_fun, "Put the next bought Action on the top of the deck"

def next_bought_card_on_the_top_of_deck():
    def sub_fun(player):
        player.next_bought_action_on_top += 1

    return sub_fun, "Put the next bought Card on the top of the deck"


def swap_a_card():
    def sub_fun(player):
        card = random.choice(player.cards_in_front_of_me)
        player.cards_in_front_of_me.remove(card)
        player.deck.add_to_discarded(card)
        player.cards_in_front_of_me.extend(player.deck.draw(1))
    text = "You can draw a card, if you do, discard another one."
    return sub_fun, text

def swap_two_cards():
    def sub_fun(player):
        print("Work in progress")
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
        temp = [x for x in player.deck.discarded if x.type == "hero"]
        if len(temp) ==0:
            return
        card = random.choice(temp)
        player.deck.discarded.remove(card)
        player.deck = [card] + player.deck
    text = "You can take a dead Hero and put them on ur deck top."
    return sub_fun, text

def resurrect_card():
    def sub_fun(player):
        if len(player.deck.discarded) == 0:
            return
        card = random.choice(player.deck.discarded)
        player.deck.discarded.remove(card)
        player.deck = [card] + player.deck
    text = "You can take a discarded Card and put it on ur deck top."
    return sub_fun, text

def sample():
    def sub_fun(player):
        pass
    text = ""
    return sub_fun, text

