import random
import pygame
from actions import *



def grayscale(color):
    # Calculate grayscale value (average of RGB components)
    gray_value = sum(color) // 3
    return (gray_value, gray_value, gray_value)

def sepia(color):
    # Sepia formula adjustments
    sepia_red = min(int(color[0] * 0.393 + color[1] * 0.769 + color[2] * 0.189), 255)
    sepia_green = min(int(color[0] * 0.349 + color[1] * 0.686 + color[2] * 0.168), 255)
    sepia_blue = min(int(color[0] * 0.272 + color[1] * 0.534 + color[2] * 0.131), 255)
    return (sepia_red, sepia_green, sepia_blue)

def get_color(color_name):
    colors = {
        "red": (252, 177, 151),
        "yellow": (252, 231, 151),
        "green": (204, 255, 204),
        "blue": (204, 229, 255),
        None: (204, 153, 102)  # Default to brown if None is given
    }
    return colors[color_name]

def get_border_color(color_name):
    colors = {
        "red": (222, 36, 27),
        "yellow": (232, 194, 56),
        "green": (102, 204, 102),
        "blue": (102, 153, 204),
        None: (153, 102, 51)  # Default to a darker brown if None is given
    }
    return colors[color_name]

class Card:
    def __init__(self, name, description, actions, value=0, alliance=None, actions_if_destroyed = (), actions_if_alliance = ()):
        self.name = name
        self.alliance = alliance
        self.type = ""
        self.value = value
        self.description = description
        self.actions = actions      #[gold, attack, health, other actions...]
        self.actions_if_destroyed = actions_if_destroyed
        self.actions_if_alliance = actions_if_alliance

    def __str__(self):
        return "Card: " + self.name

    def __repr__(self):
        return self.name

    def use(self, player):
        player.coins += self.actions[0]
        player.attack_power += self.actions[1]
        player.health += self.actions[2]
        for action in self.actions[3:]:
            action[0](player)


    def use_with_alliance(self, player):
        if len(self.actions_if_alliance) == 0:
            return

        alliance_counter = 0
        for c in player.cards_in_front_of_me + player.army:
            if c.alliance == self.alliance:
                alliance_counter += 1
        if alliance_counter <= 1:
            return

        player.coins += self.actions_if_alliance[0]
        player.attack_power += self.actions_if_alliance[1]
        player.health += self.actions_if_alliance[2]
        for action in self.actions_if_alliance[3:]:
            action[0](player)

    def destroy(self, player):
        for action in self.actions_if_destroyed:
            action(player)
            


class Hero(Card):
    def __init__(self,  name, description, actions, health, value, if_guardian = False, alliance = None, actions_if_destroyed = (), actions_if_alliance = ()):
        super().__init__( name, description, actions, value, alliance, actions_if_destroyed, actions_if_alliance )
        self.activated = True
        self.type = "Hero"
        self.health =health
        self.if_guardian = if_guardian

    def use(self, player):
        super().use(player)

    def activate(self):
        self.activated = True

class Action(Card):
    def __init__(self, name, description, actions, value, alliance = None, actions_if_destroyed = (), actions_if_alliance = ()):
        super().__init__(name, description, actions, value, alliance, actions_if_destroyed, actions_if_alliance)
        self.type = "Action"

class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.discarded = []
        self.size = 0


    def shuffle(self):
        random.shuffle(self.cards)

    def add(self, card):
        self.cards.append(card)
        self.size += 1

    def add_to_discarded(self, card):
        self.discarded.append(card)
        self.size += 1




    def discard(self, cards):
        for card in cards:
            self.discarded.append(card)
            card.state = "discarded"
        self.size = len(self.discarded) + len(self.cards)

    def draw(self, number):
        drawn = []
        for _ in range(number):
            if len(self.cards) == 0:
                self.cards = self.discarded
                self.discarded = []
                self.shuffle()
                for card in self.cards:
                    card.state = "face_down"
            if len(self.cards) == 0:
                break
            drawn.append(self.cards[0])
            self.cards.pop(0)
        return drawn

    def __str__(self):
        temp = f"Deck {self.name} ({self.size} cards)"
        temp = temp + "\n In the deck:"
        for card in self.cards:
            temp = temp + "\n" + card.name
        temp = temp + "\n Discarded:"
        for card in self.discarded:
            temp = temp + "\n" + card.name
        return temp

    def __len__(self):
        return self.size

class CardView():
    def __init__(self, screen, card, x, y, state, width = 150, height =210):
        self.screen = screen
        self.card = card
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x,self.y,self.width,self.height)
        self.state = state
        self.color = get_color(self.card.alliance)
        self.border_color = get_border_color(self.card.alliance)
        self.font = pygame.font.SysFont('Arial', 20)
        self.desc_font = pygame.font.SysFont('Arial', 12)

    def draw(self):
        if self.state == "face_down":
            font = pygame.font.SysFont('Arial', 24, bold=True)
            pygame.draw.rect(self.screen, (255,155,20), (self.x - 3,self.y - 3, self.width + 6, self.height + 6), border_radius=5)
            pygame.draw.rect(self.screen, (130,70,35) , (self.x,self.y, self.width, self.height), border_radius=5)

            name_text = font.render("Hero", True, "white")
            name_rect = name_text.get_rect(center=(self.x + self.width / 2,self.y + self.height / 2 - 10))
            bcg_rect = pygame.Rect(name_rect.left -5, name_rect.top - 5, name_rect.width +10, name_rect.height + 10)
            pygame.draw.rect(self.screen, "red", bcg_rect)


            name_text2 = font.render("Realms", True, "white")
            name_rect2 = name_text2.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2 + 10))
            bcg_rect2 = pygame.Rect(name_rect2.left - 5, name_rect2.top - 5, name_rect2.width + 10, name_rect2.height + 10)
            pygame.draw.rect(self.screen, "red", bcg_rect2)
            self.screen.blit(name_text, name_rect)
            self.screen.blit(name_text2, name_rect2)
        else:
            color = self.color
            br_color = self.border_color
            if_bw = False
            if self.state in ("discarded", "used"):
                color = grayscale(color)
                br_color = grayscale(br_color)
                if_bw = True
            pygame.draw.rect(self.screen, br_color, (self.x - 3,self.y - 3, self.width + 6, self.height + 6), border_radius=5)
            pygame.draw.rect(self.screen, color, (self.x,self.y, self.width, self.height), border_radius=5)



            if self.card.type == "":
                name_text = self.font.render(self.card.name, True, (0, 0, 0))
                name_rect = name_text.get_rect(center=(self.x + self.width / 2,self.y + self.height / 2 - 20))
                self.screen.blit(name_text, name_rect)
                self.draw_row_of_actions(self.card.actions, 0, 120, if_bw)

            else:
                pygame.draw.circle(self.screen, br_color, (self.x + 16, self.y + 16), 10)
                name_text = self.font.render(self.card.name, True, (0, 0, 0))
                name_rect = name_text.get_rect(center=(self.x + self.width / 2, self.y + 35))
                self.screen.blit(name_text, name_rect)

                pygame.draw.circle(self.screen, (255,155,20) if not if_bw else grayscale((255,155,20)), (self.x + self.width -16, self.y + 16), 10)
                pygame.draw.circle(self.screen, "yellow" if not if_bw else (170,170,170), (self.x + self.width - 16, self.y + 16), 7)
                value_text = self.font.render(str(self.card.value), True, (0, 0, 0))
                value_rect = value_text.get_rect(center=(self.x + self.width -16, self.y + 16))
                self.screen.blit(value_text, value_rect)

    def draw_row_of_actions(self, actions, dx= 0, dy = 100, if_bw = False):
        g = actions[0]
        a = actions[1]
        h = actions[2]
        dist = 30
        if g==0 and a== 0 and h==0:
            return
        elif g>0 and a==0 and h==0:
            self.draw_resource("g", g, self.x + self.width // 2 + dx, self.y + dy, if_bw)
        elif g==0 and a>0 and h==0:
            self.draw_resource("a", a, self.x + self.width // 2 + dx, self.y + dy, if_bw)
        elif g==0 and a==0 and h>0:
            self.draw_resource("h", h, self.x + self.width // 2 + dx, self.y + dy, if_bw)
        elif g>0 and a>0 and h==0:
            self.draw_resource("g", g, self.x + self.width // 2 + dx -dist//2, self.y + dy, if_bw)
            self.draw_resource("a", a, self.x + self.width // 2 + dx +dist//2, self.y + dy, if_bw)
        elif g>0 and a==0 and h>0:
            self.draw_resource("g", g, self.x + self.width // 2 + dx -dist//2, self.y + dy, if_bw)
            self.draw_resource("h", h, self.x + self.width // 2 + dx +dist//2, self.y + dy, if_bw)
        elif g==0 and a>0 and h>0:
            self.draw_resource("h", h, self.x + self.width // 2 + dx -dist//2, self.y + dy, if_bw)
            self.draw_resource("a", a, self.x + self.width // 2 + dx +dist//2, self.y + dy, if_bw)
        elif g>0 and a>0 and h>0:
            self.draw_resource("g", g, self.x + self.width // 2 + dx -dist, self.y + dy, if_bw)
            self.draw_resource("a", a, self.x + self.width // 2 + dx, self.y + dy, if_bw)
            self.draw_resource("h", h, self.x + self.width // 2 + dx + dist, self.y + dy, if_bw)


    def draw_resource(self,typ,amount,x,y, if_bw):
        if if_bw:
            color = (170,170,170) if typ == "g" else (85,85,85)
        else:
            color = "yellow" if typ == "g" else ("green" if typ =="h" else "red")
        pygame.draw.circle(self.screen, color, (x,y), 15)
        temp = self.font.render(str(amount), True, "black")
        rect = temp.get_rect(center=(x,y))
        self.screen.blit(temp, rect)

    def update_rect(self):
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)






class HeroView(CardView):
    def __init__(self, *args):
        super().__init__(*args)
        self.font = pygame.font.SysFont('Arial', 16)


    def draw(self):
        super().draw()
        if self.state != "face_down":
            if_bw = self.state in ("used", "discarded")
            br_color = grayscale(self.border_color) if if_bw else self.border_color

        desc_text = self.desc_font.render(self.card.description, True, (0, 0, 0))
        desc_rect = desc_text.get_rect(center=(self.x + self.width // 2, self.y + 50))
        self.screen.blit(desc_text, desc_rect)

        name_text = self.font.render("Hero", True, (0, 0, 0))
        name_rect = name_text.get_rect(center=(self.x + self.width//2, self.y + self.height - 15))
        self.screen.blit(name_text, name_rect)

        power_text = self.font.render(str(self.card.health), True, (0, 0, 0))
        power_rect = power_text.get_rect(topright=(self.x + self.width - 5, self.y + self.height - 25))
        self.screen.blit(power_text, power_rect)


        if len(self.card.actions_if_alliance) == 0:
            self.draw_row_of_actions(self.card.actions, 0, 120, if_bw)
            temp = ""
            for action in self.card.actions[3:]:
                temp = temp + action[1] + " "
            if temp != "":
                if len(temp) <= 26:
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 150))
                    self.screen.blit(text, rect)
                else:
                    temp2 = temp[26:]
                    temp = temp[:26]
                    while temp[-1] != " ":
                        temp2 = temp[-1] + temp2
                        temp = temp[:-1]
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 145))
                    self.screen.blit(text, rect)

                    text = self.desc_font.render(temp2, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 155))
                    self.screen.blit(text, rect)

        else:
            temp = ""
            for action in self.card.actions[3:]:
                temp = temp + action[1] + " "
            if temp != "":
                if len(temp) > 26:
                    temp2 = temp[26:]
                    temp= temp[:26]
                    while temp[-1] != " ":
                        temp2 = temp[-1] + temp2
                        temp = temp[:-1]
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 95))
                    self.screen.blit(text, rect)


                    text = self.desc_font.render(temp2, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 110))
                    self.screen.blit(text, rect)

                    self.draw_row_of_actions(self.card.actions, 0, 70, if_bw)
                else:
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 100))
                    self.screen.blit(text, rect)

                    self.draw_row_of_actions(self.card.actions, 0, 75, if_bw)
            else:
                self.draw_row_of_actions(self.card.actions, 0, 85, if_bw)

            #SOJUSZ
            pygame.draw.rect(self.screen, br_color, (self.x, self.y + 120, self.width, 60))
            text = self.desc_font.render("Alliance:", True, "black")
            self.screen.blit(text, (self.x + 5, self.y + 125))

            temp = ""
            for action in self.card.actions_if_alliance[3:]:
                temp = temp + action[1] + " "
            all_text_y = self.y + 155 if sum(self.card.actions_if_alliance[:3]) == 0 else self.y + 170
            if temp != "":
                if len(temp) < 26:
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, all_text_y))
                    self.screen.blit(text, rect)
                    self.draw_row_of_actions(self.card.actions_if_alliance, 0, 140, if_bw)
                else:
                    temp2 = temp[26:]
                    temp = temp[0:26]
                    while temp[-1] != " ":
                        temp2 = temp[-1] + temp2
                        temp = temp[:-1]
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, all_text_y-5))
                    self.screen.blit(text, rect)

                    text = self.desc_font.render(temp2, True, "black")
                    rect = text.get_rect(center=(self.x + 75, all_text_y+5))
                    self.screen.blit(text, rect)
                    self.draw_row_of_actions(self.card.actions_if_alliance, 0, 140, if_bw)

            else:
                self.draw_row_of_actions(self.card.actions_if_alliance, 0, 150, if_bw)

        if self.card.if_guardian:
            pygame.draw.rect(self.screen,(200,200,200),(self.x, self.y + self.height - 42, 150, 20))
            name_text = self.font.render("Guardian", True, "black")
            name_rect = name_text.get_rect(center=(self.x + self.width // 2, self.y + self.height - 32))
            self.screen.blit(name_text, name_rect)


class ActionView(CardView):
    def __init__(self, *args):
        super().__init__(*args)
        self.font = pygame.font.SysFont('Arial', 16)

    def draw(self):

        super().draw()
        if self.state == "face_down":
            return
        
        if_bw = self.state in ("used", "discarded")
        br_color = grayscale(self.border_color) if if_bw else self.border_color 
            
        name_text = self.font.render("Action Card", True, (0, 0, 0))
        name_rect = name_text.get_rect(center=(self.x + self.width//2, self.y + self.height - 15))
        self.screen.blit(name_text, name_rect)
        if len(self.card.actions_if_alliance) == 0:
            self.draw_row_of_actions(self.card.actions, 0, 120, if_bw)
            temp = ""
            for action in self.card.actions[3:]:
                temp = temp + action[1] + " "
            if temp!= "":
                if len(temp) <= 26:
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center = (self.x+75, self.y + 150))
                    self.screen.blit(text, rect)
                else:
                    temp2 = temp[26:]
                    temp = temp[:26]
                    while temp[-1] != " ":
                        temp2 = temp[-1] + temp2
                        temp = temp[:-1]
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 145))
                    self.screen.blit(text, rect)

                    text = self.desc_font.render(temp2, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 155))
                    self.screen.blit(text, rect)


        else:
            temp = ""
            for action in self.card.actions[3:]:
                temp = temp + action[1] + " "
            if temp != "":
                if len(temp) > 26:
                    temp2 = temp[26:]
                    temp= temp[:26]
                    while temp[-1] != " ":
                        temp2 = temp[-1] + temp2
                        temp = temp[:-1]
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 95))
                    self.screen.blit(text, rect)


                    text = self.desc_font.render(temp2, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 110))
                    self.screen.blit(text, rect)

                    self.draw_row_of_actions(self.card.actions, 0, 70, if_bw)
                else:
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, self.y + 100))
                    self.screen.blit(text, rect)

                    self.draw_row_of_actions(self.card.actions, 0, 75, if_bw)
            else:
                self.draw_row_of_actions(self.card.actions, 0, 85, if_bw)

            #SOJUSZ
            pygame.draw.rect(self.screen, br_color, (self.x, self.y + 120, self.width, 60))
            text = self.desc_font.render("Alliance:", True, "black")
            self.screen.blit(text, (self.x + 5, self.y + 125))

            temp = ""
            for action in self.card.actions_if_alliance[3:]:
                temp = temp + action[1] + " "
            all_text_y = self.y + 155 if sum(self.card.actions_if_alliance[:3]) == 0 else self.y + 170
            if temp != "":
                if len(temp) < 26:
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, all_text_y))
                    self.screen.blit(text, rect)
                    self.draw_row_of_actions(self.card.actions_if_alliance, 0, 140, if_bw)
                else:
                    temp2 = temp[26:]
                    temp = temp[0:26]
                    while temp[-1] != " ":
                        temp2 = temp[-1] + temp2
                        temp = temp[:-1]
                    text = self.desc_font.render(temp, True, "black")
                    rect = text.get_rect(center=(self.x + 75, all_text_y-5))
                    self.screen.blit(text, rect)

                    text = self.desc_font.render(temp2, True, "black")
                    rect = text.get_rect(center=(self.x + 75, all_text_y+5))
                    self.screen.blit(text, rect)
                    self.draw_row_of_actions(self.card.actions_if_alliance, 0, 140, if_bw)

            else:
                self.draw_row_of_actions(self.card.actions_if_alliance, 0, 150, if_bw)









def get_player_deck(name = "Player"):
    deck = Deck(f"{name}'s Deck")
    for _ in range(5):
        deck.add(Card("Moneta", "+1 złoto", [1,0,0]))
    deck.add(Card("Rubin", "+2 złoto", [2,0,0]))
    deck.add(Card("Sztylet", "+1 atak", [0,1,0]))
    deck.add(Card("Krótki Miecz", "+2 atak", [0,2,0]))
    deck.shuffle()
    return deck


# noinspection PyTypeChecker
def get_shop_deck():
    deck = Deck(f"Shop's Deck")

    deck.add(Hero("Arkus", "Imperialny Smok", [0, 5, 0, draw_card()], 6, 8, alliance="yellow",
                  if_guardian=True, actions_if_alliance=[0,0,6]))

    deck.add(Hero("Borg", "Org Najemnnik", [0,4,0], 6, 6, alliance="blue",
                  if_guardian=True))

    deck.add(Action("Bomba Ogniowa", "", [0, 8, 0, stun_hero(), draw_card()], 8, "blue",
                    actions_if_destroyed=[0, 5, 0]))

    deck.add(Hero("Broelyn", "Tkaczka Legend", [4, 0, 0], 6, 4, alliance="green",
                  if_guardian=False, actions_if_alliance=[0,0,0,opponent_discard()]))

    for _ in range(2):
        deck.add(Hero("Ciężkozbrojny", "Człowiek Wojownik", [0, 2, 0, attack_for_guardian()], 4, 3, alliance="yellow",
                      if_guardian=True))

    deck.add(Hero("Cristov Sprawiedliwy", "Człowiek Paladyn", [0, 2, 3], 5, 5, alliance="yellow",
                  if_guardian=True, actions_if_alliance=[0,0,0,draw_card()]))

    deck.add(Hero("Cron, Berserker", "Człowiek Wojownik", [0, 5, 0], 6, 6, alliance="green",
                  if_guardian=False, actions_if_alliance=[0,0,0,draw_card()]))

    for _ in range(3):
        deck.add(Action("Dar Elfów", "", [2, 0, 0, swap_a_card()], 2, "green",
                        actions_if_alliance=[0, 4, 0]))
    for _ in range(2):
        deck.add(Hero("Decymator", "Człowiek Kapłan", [1, 0, 0, add_health_for_hero()], 3, 2, alliance="yellow",
                  if_guardian=False))

    deck.add(Hero("Darian", "Mag Wojny", [0, 0, 0, get_attack_or_health(3,4)], 5, 4, alliance="yellow",
                  if_guardian=False))

    deck.add(Action("Dary Natury", "", [4, 0, 0], 4, "green",
                    actions_if_alliance=[0, 0, 0, opponent_discard()], actions_if_destroyed=[0,4,0]))

    deck.add(Action("Dominacja", "", [0, 6, 6, draw_card()], 7, "yellow",
                    actions_if_alliance=[0, 0, 0, reactivate_hero()]))

    for _ in range(3):
        deck.add(Action("Dotyk Śmierci", "", [0,2,0, can_sacrifice()], 1, "red",
                    actions_if_alliance=[0,2,0]))

    deck.add(Action("Dowodzenie", "Za mną!", [2, 4, 4], 5, "yellow",))

    deck.add(Action("Forma Wilka", "", [0, 8, 0, opponent_discard()], 5, "green",
                    actions_if_alliance=[0, 0, 0, opponent_discard()]))

    deck.add(Hero("Grak", "Sztormowy Gigant", [0, 6, 0, swap_a_card()], 7, 8, alliance="green",
                  if_guardian=True, actions_if_alliance=[0, 0, 0, swap_a_card()]))

    deck.add(Action("Groźba Śmierci", "", [0,1,0, draw_card()], 3, "blue", actions_if_alliance=[0,0,0,stun_hero()]))

    for _ in range(3):
        deck.add(Action("Iskra", "", [0, 3, 0, opponent_discard()], 1, "green",
                        actions_if_alliance=[0,2,0]))

    for _ in range(2):
        deck.add(Hero("Kapłan Kultu", "", [0, 0, 0, get_coins_or_attack(1, 1)], 4, 3, alliance="red",
                      if_guardian=False, actions_if_alliance=[0,4,0]))

    for _ in range(2):
        deck.add(Action("Klątwa Elfów", "", [0, 6, 0, opponent_discard()], 3, "green",
                        actions_if_alliance=[0,3,0]))

    deck.add(Hero("Kraka", "Arcykapłan", [0, 0, 2, draw_card()], 6, 6, alliance="yellow",
                  if_guardian=False, actions_if_alliance=[0,0,0,add_health_for_hero(2)]))

    deck.add(Hero("Krythos", "Mistrz Wampirów", [0, 3, 0, can_sacrifice(3)], 6, 7, alliance="red",
                  if_guardian=False))

    for _ in range(2):
        deck.add(Hero("Kultysta Śmierci", "", [0,2,0], 3, 2, alliance="red",
                      if_guardian=False))

    deck.add(Hero("Lys, Nieuchwytny", "Wampir", [0, 2, 0, can_sacrifice(2)], 5, 6, alliance="red",
                  if_guardian=True))

    for _ in range(3):
        deck.add(Action("Łapówka", "", [3,0,0], 3, "blue",
                    actions_if_alliance=[0,0,0,next_bought_action_on_the_top_of_deck()]))

    deck.add(Hero("Mistrz Weyan", "Człowiek Mnich", [0, 3, 0, add_attack_for_hero()], 4, 4, alliance="yellow",
                  if_guardian=True))

    deck.add(Action("Mroczna Energia", "Czar", [0, 7, 0], 4, "red",
                    actions_if_alliance=[0, 0, 0, draw_card()]))

    deck.add(Action("Mroczna Nagroda", "", [3, 0, 0, can_sacrifice()], 5, "red",
                    actions_if_alliance=[0, 6, 0]))

    deck.add(Hero("Myros", "Mag Gildii", [3, 0, 0], 3, 5, alliance="blue",
                  actions_if_alliance=[0, 4, 0], if_guardian=True))

    deck.add(Action("Niszczenie i Grabież", "", [0, 6, 0, resurrect_card()], 6, "blue",
                    actions_if_alliance=[0, 0, 6]))

    for _ in range(3):
        deck.add(Action("Opodatkowanie", "", [2,0,0], 1, "yellow",
                    actions_if_alliance=[0,0,6]))

    for _ in range(2):
        deck.add(Hero("Ork Grabieżca", "", [0,2,0], 3, 3, alliance="green",
                    actions_if_alliance=[0,0,0,draw_card()]))

    deck.add(Action("Oszustwo", "", [2,0,0, draw_card()], 5, "blue",
                    actions_if_alliance=[0,0,0,next_bought_on_hand()]))

    deck.add(Hero("Parov", "Egzekutor", [0, 3, 0], 5, 5, alliance="blue",
                  actions_if_alliance=[0, 0, 0, draw_card()]))

    deck.add(Hero("Rasmus", "Przemytnik", [2, 0, 0], 5, 4, alliance="blue",
                  if_guardian=False, actions_if_alliance=[0,0,0,next_bought_card_on_the_top_of_deck()]))

    deck.add(Hero("Rayla", "Wieszczka Końca", [0,3,0], 4, 4, alliance="red",
                  actions_if_alliance=[0,0,0,draw_card()]))

    deck.add(Hero("Rake", "Mistrz Skrytobójców", [0, 4, 0, stun_hero()], 7, 7, alliance="blue",
                  actions_if_alliance=[0, 0, 0, draw_card()]))

    deck.add(Action("Szał", "Ork", [0, 6, 0, swap_two_cards()], 6, "green"))

    deck.add(Action("Słowo Mocy", "Czar", [0, 0, 0, draw_2_cards()], 6, "yellow",
                    actions_if_alliance=[0, 0, 5], actions_if_destroyed=[0,5,0]))

    deck.add(Hero("Torgen", "Kruszący Skały", [0, 4, 0, opponent_discard()], 7, 7, alliance="green",
                  if_guardian=True))

    deck.add(Hero("Tyrannor Pożeracz", "Demon", [0, 4, 0, can_sacrifice_two()], 6, 8, alliance="red",
                  if_guardian=True, actions_if_alliance=[0,0,0,draw_card()]))

    for _ in range(2):
        deck.add(Hero("Uliczny Bandyta", "", [0, 0, 0, get_coins_or_attack(1, 2)], 4, 3, alliance="blue"))

    deck.add(Hero("Varrick", "Nekromanta", [0, 0, 0, resurrect_hero()], 3, 5, alliance="red", actions_if_alliance=[0,0,0,draw_card()]))

    for _ in range(3):
        deck.add(Action("Werbunek", "", [2,0,3, add_health_for_hero()], 2, "yellow",
                    actions_if_alliance=[1,0,0]))

    for _ in range(2):
        deck.add(Hero("Wilczy Szaman", "Człowiek Kapłan", [0, 2, 0, attack_for_alliance("green")], 4, 2, alliance="green"))

    deck.add(Hero("Wilkor", "Gigantyczny Wilk", [0, 3, 0], 5, 5, alliance="green",
                  actions_if_alliance=[4, 0, 0], if_guardian=True))

    deck.add(Action("Wyssanie Życia", "Klątwa", [0, 8, 0, can_sacrifice()], 6, "red",
                    actions_if_alliance=[0, 0, 0, draw_card()]))

    for _ in range(3):
        deck.add(Action("Wpływy", "", [3, 0, 0], 2, "red",
                    actions_if_destroyed=[0, 0, 3]))

    for _ in range(2):
        deck.add(Action("Zastraszenie", "", [0,5,0], 2, "blue",
                        actions_if_alliance=[2,0,0]))

    deck.add(Action("Zlecenie Zabójstwa", "Zabójca", [0, 7, 0], 4, "blue",
                    actions_if_alliance=[0, 0, 0, stun_hero()]))

    for _ in range(2):
        deck.add(Action("Zgnilizna", "Klątwa", [0,4,0, can_sacrifice()], 3, "red",
                    actions_if_alliance=[0,3,0]))

    deck.add(Action("Zwarte Szeregi", "", [0, 5, 0, add_attack_for_hero(2)], 3, "yellow",
                    actions_if_alliance=[0, 0, 6]))

    deck.add(Action("Zwołanie Wojsk", "", [0, 5, 5], 4, "yellow",
                    actions_if_alliance=[0, 0, 0, reactivate_hero()]))
    for _ in range(3):
        deck.add(Action("Zyski", "", [2, 0, 0], 1, "blue",
                    actions_if_alliance=[0, 4, 0]))


    deck.shuffle()
    return deck



if __name__ == "__main__":
    a = Card("Moneta", "Złota Moneta", [gen_add_gold(1)])
    b = Card("Moneta", "Złota Moneta", [gen_add_gold(1)])
    print(a==b, a is b)





