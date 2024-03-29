from cards import *


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 60
        self.attack_power = 0
        self.coins = 0
        self.deck = get_player_deck(name)
        self.cards_to_draw = 5
        self.cards_in_front_of_me = []
        self.to_sacrifice = []
        self.army = []
        self.opponent_card_mod = 0
        self.opponent = None
        self.next_bought_card_on_hand = 0
        self.next_bought_action_on_top = 0
        self.next_bought_card_on_top = 0
        self.cards_to_sacrifice = 0
        self.sacrifice_bonus = 0
        self.heroes_to_reactivate = 0
        self.heroes_to_block = 0
        self.heroes_to_resurect = 0
        self.cards_to_resurect = 0
        self.cards_to_discard = 0

    def turn(self):
        pass
        #DRAW 5 CARDS
        #USE CARDS
        #BUY IN SHOP
        #ATTACK
        #RESET

    def reset(self):
        self.coins = 0
        self.attack_power = 0
        self.cards_to_draw = 5
        self.cards_in_front_of_me = []
        self.to_sacrifice = []
        self.opponent_card_mod = 0
        self.next_bought_card_on_hand = 0
        self.next_bought_action_on_top = 0
        self.next_bought_card_on_top = 0
        self.cards_to_sacrifice = 0
        self.heroes_to_reactivate = 0
        self.heroes_to_block = 0
        self.heroes_to_resurect = 0
        self.cards_to_resurect = 0
        self.cards_to_discard = 0


    def __str__(self):
        return f"Player {self.name}: health({self.health}) coins({self.coins}) attack power({self.attack_power})"

    def auto_sacrfice(self):
        temp_deck = self.deck.discarded + self.cards_in_front_of_me
        if len(temp_deck) < 1:
            return False
        if len(temp_deck + self.deck.cards) < 5:
            return False
        temp_deck.sort(key= lambda card: card.value)
        chosen = temp_deck[0]
        if chosen in self.deck.discarded:
            self.deck.discarded.remove(chosen)
        else:
            self.cards_in_front_of_me.remove(chosen)
        self.cards_to_draw -= 1
        return chosen.name

if __name__ == "__main__":
    p = Player("Olo")
    p.deck.add(Action("Opodatkowanie1","Akcja",[gen_add_gold(2),gen_add_health(6)],1, "yellow"))
    p.deck.add(Action("Opodatkowanie2","Akcja",[gen_add_gold(2),gen_add_health(6)],1, "yellow"))
    p.deck.add(Action("Słowo Mocy", "Akcja - Czar", [draw_card, draw_card], 6, "yellow"))
    p.deck.add(Hero("Uliczny Bandyta", "Człowiek Łotr", [get_coins_or_attack(1, 2)], 4, 3, alliance="blue"))
    p.deck.add(Action("Mroczna Nagroda", "Akcja", [gen_add_gold(3),can_sacrifice()],5,"red",actions_if_alliance=[gen_attack(6)]))
    p.deck.shuffle()
    p.turn()
    p.turn()
    p.turn()
    p.turn()