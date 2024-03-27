import time

import pygame
import sys
import random
from cards import *
from players import *
from buttons import *
from timer import *
from texts import *

GREEN = (36, 107, 33)

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


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1300
        self.screen_height = 786
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Hero Realms")
        self.clock = pygame.time.Clock()
        self.bcg_color = (36,107,33)
        self.player = Player("Player 1")
        self.opponent = Player("Gary")
        self.active_cards = []
        self.drawable_cards = []
        self.shop_deck = get_shop_deck()
        self.shop_to_buy = self.shop_deck.draw(5)
        self.shop_visible = True
        self.army_visible = False
        self.scrolling_speed = 0

        self.buttons = []
        self.set_buttons()
        self.base_y=0
        self.opponent_y = -1 * self.screen_height * 2 // 3
        self.opponent.opponent = self.player
        self.player.opponent = self.opponent

        self.cards_up=[]
        self.cards_down = []
        self.turn = "Intro"
        self.timers = []

        self.goal_y_set = False
        self.goal_y = 0

        self.opp_stats_vertical = True
        self.if_opponent_first_turn = True

        self.attack_points = []

        self.opponent_dialog = ""
        self.opponent_army_visible = False

        image = pygame.image.load(f"opponent_pics/{str(random.randint(1, 20))}.png")
        image = pygame.transform.scale(image, (200, 250))
        self.opponent.image = image


    def restart(self):
        self.player = Player("Player 1")
        self.opponent = Player("Gary")
        self.active_cards = []
        self.drawable_cards = []
        self.shop_deck = get_shop_deck()
        self.shop_to_buy = self.shop_deck.draw(5)
        self.shop_visible = True
        self.army_visible = False
        self.scrolling_speed = 0
        self.bcg_color = (36, 107, 33)

        self.buttons = []
        self.set_buttons()
        self.base_y = 0
        self.opponent_y = -1 * self.screen_height * 2 // 3
        self.opponent.opponent = self.player
        self.player.opponent = self.opponent

        self.cards_up = []
        self.cards_down = []
        self.update_card_views()

        self.timers = []
        self.opponent_dialog = ""
        self.opponent_army_visible = False
        self.if_opponent_first_turn = True

        image = pygame.image.load(f"opponent_pics/{str(random.randint(1, 12))}.png")
        image = pygame.transform.scale(image, (200, 250))
        self.opponent.image = image

        self.who_starts()
        self.attack_points = []


    def set_buttons(self):
        def func():
            if self.shop_visible:
                self.shop_visible = False
            else:
                self.shop_visible = True
        self.button_shop = Button(self.screen, "Shop:", 160, 10, function=func)
        self.buttons.append(self.button_shop)
        def func2():
            if self.army_visible:
                self.army_visible = False
            else:
                self.army_visible = True
        self.button_army = Button(self.screen, "Your Heroes:", 30, 320, function=func2)
        self.buttons.append(self.button_army)


    def run(self, if_ommit_info = False):
        if not if_ommit_info:
            self.intro()
        else:
            self.turn = "Player"
        self.update_card_views()
        while True:


            for t in self.timers:
                t.update()

            if self.scrolling_speed != 0:
                self.base_y += self.scrolling_speed
                for view in self.drawable_cards + self.buttons:
                    view.y += self.scrolling_speed
                    view.update_rect()

            if self.goal_y_set:
                if abs(self.base_y - self.goal_y) >= 5:
                    self.scrolling_speed = 10 if self.base_y < self.goal_y else -10
                else:
                    self.scrolling_speed = 0
                    self.goal_y_set = False


            for event in pygame.event.get():
                self.handle_events(event)
            self.draw()
            self.move_cards()

            pygame.display.flip()
            self.clock.tick(60)


    def intro(self):
        i = 0
        bcg_i = 250
        pad = 30
        text="Hero Realms"
        text2 = "Fan-Made Python Version"
        text3 = "by Alex Michalec"
        temp=""
        temp2 = ""
        counter2 = 0
        counter = 0
        while True:
            i = min(i+1, 250)
            self.screen.fill((i,i,i))
            if i==250:
                font = pygame.font.SysFont('Arial', 100)
                name_text = font.render("Hero Realms", True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 -60))
                bcg_rect = pygame.rect.Rect(name_rect.left - pad ,name_rect.top -pad ,name_rect.width + 2*pad,name_rect.height + 2*pad)
                pygame.draw.rect(self.screen,(250,bcg_i,bcg_i),bcg_rect)
                self.screen.blit(name_text, name_rect)
                bcg_i = max(0, bcg_i-1)
            if bcg_i == 0:
                if counter//10 < len(text2) and counter%10 == 0:
                    temp = temp + text2[counter//10]
                counter += 1
                font = pygame.font.SysFont('Arial', 30)
                name_text = font.render(temp, True, (0, 0, 0))
                name_rect = name_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))
                self.screen.blit(name_text, name_rect)
            if counter//10 > len(text2):
                if counter2//10 < len(text3) and counter2%10 == 0:
                    temp2 = temp2 + text3[counter2//10]
                counter2 += 1
                font = pygame.font.SysFont('Arial', 20)
                name_text = font.render(temp2, True, (0, 0, 0))
                name_rect = name_text.get_rect(center=(self.screen_width -100, self.screen_height -40))
                self.screen.blit(name_text, name_rect)

            if counter2 //10 > len(text2):
                break

            for event in pygame.event.get():
                self.handle_events(event)
            pygame.display.update()

        while i>0:
            i = max(i-2, 0)
            self.screen.fill((i, i, i))

            font = pygame.font.SysFont('Arial', 100)
            name_text = font.render("Hero Realms", True, (i, i, i))
            name_rect = name_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
            bcg_rect = pygame.rect.Rect(name_rect.left - pad, name_rect.top - pad, name_rect.width + 2 * pad,
                                        name_rect.height + 2 * pad)
            pygame.draw.rect(self.screen, (i, bcg_i, bcg_i), bcg_rect)
            self.screen.blit(name_text, name_rect)

            font = pygame.font.SysFont('Arial', 30)
            name_text = font.render(temp, True, (0, 0, 0))
            name_rect = name_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))
            self.screen.blit(name_text, name_rect)

            font = pygame.font.SysFont('Arial', 20)
            name_text = font.render(temp2, True, (0, 0, 0))
            name_rect = name_text.get_rect(center=(self.screen_width - 100, self.screen_height - 40))
            self.screen.blit(name_text, name_rect)

            for event in pygame.event.get():
                self.handle_events(event)
            pygame.display.update()
        self.who_starts()

    def who_starts(self):
        i = 0
        x = random.choice(("Player", "Opponent"))
        if x == "Player":
            message = "This time you start"
            self.player.cards_to_draw = 4
        else:
            message = "This time your opponent starts"
            self.opponent.cards_to_draw = 4


        temp = ""
        while i//20 < len(message):

            if i % 20 == 0:
                temp = temp + message[i//20]
            i += 1
            font = pygame.font.SysFont('Arial', 50)
            name_text = font.render(temp, True, (250, 250, 250))
            name_rect = name_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.fill((0,0,0))
            self.screen.blit(name_text, name_rect)
            pygame.display.update()
            for event in pygame.event.get():
                self.handle_events(event)

        i = 255
        while i > 0:
            i -= 1
            font = pygame.font.SysFont('Arial', 50)
            name_text = font.render(temp, True, (i, i, i))
            name_rect = name_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.fill((0,0,0))
            self.screen.blit(name_text, name_rect)
            pygame.display.update()
            for event in pygame.event.get():
                self.handle_events(event)

        while i < 1000:
            for event in pygame.event.get():
                self.handle_events(event)
            self.screen.fill(((GREEN[0] * i)//1000, (GREEN[1] * i)//1000, (GREEN[2] * i)//1000))
            pygame.display.update()
            i = i+1

        self.turn = x
        if x == "Opponent":
            self.update_card_views()
            self.move_up()



    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if self.player.health <= 0 or self.opponent.health <= 0:
                self.restart()
                self.turn = "Player"

        if self.turn == "Player":
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.scrolling_speed =5
                elif event.key == pygame.K_DOWN:
                    self.scrolling_speed =-5
                if event.key == pygame.K_SPACE:
                    #self.base_y = 0
                    if self.player.cards_in_front_of_me:
                        self.player.deck.discarded.extend(self.player.cards_in_front_of_me)
                        self.player.cards_in_front_of_me = []
                        self.update_card_views()
                        self.add_attack_player()
                        self.player.reset()
                        self.move_up()
                        #self.opponent_turn()



                    else:
                        self.player.cards_in_front_of_me = self.player.deck.draw(self.player.cards_to_draw)
                        self.update_card_views()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.scrolling_speed = 0
                elif event.key == pygame.K_DOWN:
                    self.scrolling_speed = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for card in self.active_cards:
                    if not card.rect.collidepoint(mouse_x, mouse_y):
                        continue
                    if card.state == "active":
                        card.state = "used"
                        card.card.use(self.player)
                        card.card.use_with_alliance(self.player)
                        if self.player.cards_to_draw > len(self.player.cards_in_front_of_me):
                            self.player.cards_in_front_of_me.extend(
                                self.player.deck.draw(self.player.cards_to_draw - len(self.player.cards_in_front_of_me)))
                            self.update_card_views(True)
                        if card.card.type == "Hero" and card.card not in self.player.army:
                            self.player.army.append(card.card)
                            self.player.cards_in_front_of_me.remove(card.card)
                            self.player.cards_to_draw -= 1
                            self.update_card_views(if_buying=True)
                        self.update_card_views(True)
                    elif card.state == "face_down":
                        self.player.cards_in_front_of_me = self.player.deck.draw(self.player.cards_to_draw)
                        self.update_card_views()
                    elif card.state == "shop" and self.player.coins >= card.card.value:
                        self.player.coins -= card.card.value
                        self.cards_down.append(card)
                        index = self.shop_to_buy.index(card.card)
                        self.shop_to_buy.remove(card.card)
                        self.shop_to_buy.insert(index, self.shop_deck.draw(1)[0])
                        self.update_card_views(if_buying=True)
                        self.drawable_cards.extend(self.cards_down)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        button.use()
                        self.update_card_views(if_buying=True)

    def move_cards(self):
        for view in self.cards_down:
            view.y += 30
            if view.y >= self.screen_height:
                if self.player.next_bought_card_on_hand:
                    self.player.cards_in_front_of_me.append(view.card)
                    self.player.next_bought_card_on_hand -= 1
                elif self.player.next_bought_card_on_top:
                    self.player.deck.cards = [view.card] + self.player.deck.cards
                    self.player.next_bought_card_on_top -= 1
                elif self.player.next_bought_action_on_top and view.card.type == "Action":
                    self.player.deck.cards = [view.card] + self.player.deck.cards
                    self.player.next_bought_action_on_top -= 1
                else:
                    self.player.deck.add_to_discarded(view.card)
                self.update_card_views(True)
        self.cards_down = [view for view in self.cards_down if view.y < self.screen_height]
        self.drawable_cards.extend(self.cards_down)

        for view in self.cards_up:
            view.y -= 30
            if view.y <= -210:
                self.opponent.deck.add_to_discarded(view.card)
                self.update_card_views(True)
        self.cards_up = [view for view in self.cards_up if view.y > -210]
        self.drawable_cards.extend(self.cards_up)

    def draw(self):
        self.screen.fill(self.bcg_color)
        pygame.draw.rect(self.screen, "white", (10, self.base_y + self.screen_height*2//3, 150, 210), 3)
        for view in self.drawable_cards:
            view.draw()
        if not self.army_visible:
            y = 335 +self.base_y
            for i, card in enumerate(self.player.army):
                pygame.draw.rect(self.screen,"white",(250 + i*30, y, 20, 30))

        self.draw_text(f"Health: {self.player.health}", "green", self.screen_width-200, self.base_y + 360, 30 )
        self.draw_text(f"Coins: {self.player.coins}", "yellow", self.screen_width - 200, self.base_y + 390, 30)
        self.draw_text(f"Attack: {self.player.attack_power}", "red", self.screen_width - 200, self.base_y + 420, 30)

        dx = 500
        dy = 870
        if not self.opp_stats_vertical:
            self.draw_text(f"Health: {self.opponent.health}", "green", self.screen_width - 200 -dx, self.base_y + 360 -dy, 30)
            self.draw_text(f"Coins: {self.opponent.coins}", "yellow", self.screen_width - 200 -dx, self.base_y + 390 -dy , 30)
            self.draw_text(f"Attack: {self.opponent.attack_power}", "red", self.screen_width - 200 -dx, self.base_y + 420 -dy, 30)
        else:
            self.draw_text(f"Health: {self.opponent.health}", "green", self.screen_width - 400 - dx,
                           self.base_y + 430 - dy, 30)
            self.draw_text(f"Coins: {self.opponent.coins}", "yellow", self.screen_width - 200 - dx,
                           self.base_y + 430 - dy, 30)
            self.draw_text(f"Attack: {self.opponent.attack_power}", "red", self.screen_width - 0 - dx,
                           self.base_y + 430 - dy, 30)

        for button in self.buttons:
            if button == self.button_army and len(self.player.army) == 0:
                continue
            button.draw()
        #self.draw_player_cards()

        # Clickable
        for view in self.active_cards+self.buttons:
            x, y = pygame.mouse.get_pos()
            if view.rect.collidepoint(x, y):
                temp = view.color
                temp2 = view.border_color
                view.color = (max(0, temp[0]-20), max(temp[1]-20,0), max(0,temp[2]-20))
                view.border_color = (max(0, temp2[0] - 20), max(temp2[1] - 20, 0), max(0, temp2[2] - 20))
                view.draw()
                view.color = temp
                view.border_color = temp2

        if self.player.health <= 0:
            self.active_cards = []
            self.screen.fill((0,0,0))
            self.draw_text("Unfortunately, you lose :c", (240,240,240), 260, 350, 80)
            self.draw_text("Do you want to start again?", (240, 240, 240), 200, 450, 30)
            self.draw_text("Press any button to start again", (240, 240, 240), 400, 550, 20)

        if self.opponent.health <= 0:
            self.active_cards = []
            self.screen.fill((173,126,75))
            gold = (255, 207, 75)
            self.draw_text("Congratulation, you won!!! :D", gold, 260, 350, 80)
            self.draw_text("Do you want to start again?", gold, 200, 450, 30)
            self.draw_text("Press any button to start again", gold, 400, 550, 20)

        self.draw_attack()

        if self.opponent_dialog:
            self.screen.blit(self.opponent.image, (self.screen_width//2 - 100, 20))
            self.draw_text(self.opponent_dialog,(255, 255, 255),self.screen_width//2, 300, 25, True, (0,0,0))


    def draw_attack(self):
        for point in self.attack_points:
            pygame.draw.line(self.screen, (250,0,0), (point[0], point[1]), (point[0]-200, point[1]-100) if point[2] > 0 else (point[0]-200, point[1] +100),10)
            pygame.draw.line(self.screen, (250, 0, 0), (point[0], point[1]),
                             (point[0] + 200, point[1] - 100) if point[2] > 0 else (point[0] + 200, point[1] + 100), 10)
            point[1] += point[2]
            if point[2] > 0 and point[1] > self.screen_height + 100:
                self.player.health -= 1
                if self.player.health == 0:
                    self.opp_speak()
            if point[2] < 0 and point[1] < -100:
                self.opponent.health -= 1
                if self.opponent.health == 0:
                    self.timers = []
                    self.opp_speak()

        self.attack_points = [x for x in self.attack_points if (x[2]>0 and x[1] < self.screen_height + 100) or (x[2]<0 and x[1] > -100)]



    def add_attack_player(self):
        for i in range(self.player.attack_power):
            self.attack_points.append([self.screen_width//2,self.screen_height + i*50, -10])

    def add_attack_opponent(self):
        names_of_killed_heroes = ""
        heroes = self.player.army
        guardians = [hero for hero in heroes if hero.if_guardian]
        for guardian in guardians:
            if guardian.health <= self.opponent.attack_power:
                self.opponent.attack_power -= guardian.health
                self.player.deck.add_to_discarded(guardian)
                self.player.army.remove(guardian)
                if len(names_of_killed_heroes):
                    names_of_killed_heroes = names_of_killed_heroes + ", " + guardian.name
                else:
                    names_of_killed_heroes = guardian.name
        guardians = [hero for hero in heroes if hero.if_guardian]
        if len(guardians):
            self.opponent.attack_power = 0
            if names_of_killed_heroes:
                self.opponent_dialog = "I kill your: " + names_of_killed_heroes + "!"
                t = Timer(2000, self.opp_speak_gen("x", -1))
                t.activate()
                self.timers.append(t)
            return
        heroes = self.player.army
        if self.opponent.attack_power < self.player.health:
            for hero in heroes:
                if hero.health <= self.opponent.attack_power:
                    self.opponent.attack_power -= hero.health
                    self.player.deck.add_to_discarded(hero)
                    self.player.army.remove(hero)
                    if len(names_of_killed_heroes):
                        names_of_killed_heroes = names_of_killed_heroes + ", " + hero.name
                    else:
                        names_of_killed_heroes = hero.name

        if len(names_of_killed_heroes):
            if self.opponent.attack_power > 0:
                self.opponent_dialog = "I kill your: " + names_of_killed_heroes + " and attack you with " + str(self.opponent.attack_power)
            else:
                self.opponent_dialog = "I kill your: " + names_of_killed_heroes + "!"
            t = Timer(2000, self.opp_speak_gen("", -1))
            t.activate()
            self.timers.append(t)

        for i in range(self.opponent.attack_power):
            self.attack_points.append([self.screen_width//2,0 - i*50, 10])

    def draw_text(self, text, color, x, y, size=20, center = False, background = None):
        font = pygame.font.SysFont('Arial', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x,y)
        else:
            text_rect.topleft = (x, y)
        if background is not None:
            rect = pygame.rect.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
            pygame.draw.rect(self.screen,background,rect)
        self.screen.blit(text_surface, text_rect)

    def update_card_views(self, if_buying=False):

        used = []
        if if_buying:
            for card in self.drawable_cards:
                if card.state == "used":
                    used.append(card.card)
        self.drawable_cards = []
        self.active_cards = []
        card_width = 150
        card_height = 210
        deck_x = self.screen_width - card_width - 10
        deck_y = self.screen_height * 2//3 + self.base_y
        for i, card in enumerate(self.player.deck.cards[:3]):
            view = CardView(self.screen, card, deck_x + i*2, deck_y - i*3, "face_down")
            self.drawable_cards.append(view)
            if i==2 and not self.player.cards_in_front_of_me:
                self.active_cards.append(view)

        discarded_x = 10
        discarded_y = deck_y
        for i, card in enumerate(self.player.deck.discarded[:3]):
            if card.type == "Hero":
                view = HeroView(self.screen, card, discarded_x + i*2, discarded_y - i*3, "discarded")
            elif card.type == "Action":
                view = ActionView(self.screen, card, discarded_x + i*2, discarded_y - i*3, "discarded")
            else:
                view = CardView(self.screen, card, discarded_x + i*2, discarded_y - i*3, "discarded")
            self.drawable_cards.append(view)

        if self.player.cards_in_front_of_me:
            y = self.screen_height//2 +self.base_y
            for i, card in enumerate(self.player.cards_in_front_of_me):
                x = self.screen_width//2 -len(self.player.cards_in_front_of_me) * (card_width+20) //2  + i * (card_width+20)
                state = "used" if card in used else "active"
                if card.type == "Hero":
                    view = HeroView(self.screen, card, x, y, state)
                elif card.type == "Action":
                    view = ActionView(self.screen, card, x, y, state)
                else:
                    view = CardView(self.screen, card, x, y, state)
                if state == "used":
                    view.y -= 20
                self.drawable_cards.append(view)
                self.active_cards.append(view)



        #ARMY
        by = 360 + self.base_y
        for i, card in enumerate(self.player.army):
            x = 290 + i * (card_width + 20) if self.army_visible else 2000
            state = "active" if card not in used else "used"
            y = by - 20 if state == "used" else by
            view = HeroView(self.screen, card, x, y, state)
            self.active_cards.append(view)
            self.drawable_cards.append(view)

        """""
        for button in self.buttons:
            button.x = button.base_x
            button.y = button.base_y
            button.update_rect()
        """

        #OPPONENT
        #USED? FUNCTIONALITY

        #DECK FACED DOWN
        deck_x = 10
        deck_y = -1 * self.screen_height * 2 // 3 +self.base_y + 80
        for i, card in enumerate(self.opponent.deck.cards[:3]):
            view = CardView(self.screen, card, deck_x + i * 2, deck_y - i * 3, "face_down")
            self.drawable_cards.append(view)

        #DISCARDED CARDS
        discarded_x = self.screen_width - card_width -10
        discarded_y = deck_y
        for i, card in enumerate(self.opponent.deck.discarded[:3]):
            if card.type == "Hero":
                view = HeroView(self.screen, card, discarded_x + i * 2, discarded_y - i * 3, "discarded")
            elif card.type == "Action":
                view = ActionView(self.screen, card, discarded_x + i * 2, discarded_y - i * 3, "discarded")
            else:
                view = CardView(self.screen, card, discarded_x + i * 2, discarded_y - i * 3, "discarded")
            self.drawable_cards.append(view)

        #IN FRONT OF ME
        if self.opponent.cards_in_front_of_me:
            y = -1 * self.screen_height // 2  +self.base_y
            for i, card in enumerate(self.opponent.cards_in_front_of_me):
                x = self.screen_width // 2 - len(self.opponent.cards_in_front_of_me) * (card_width + 20) // 2 + i * (
                            card_width + 20)
                state = "used" if card in used else "active"
                if state == "used":
                    y += 20
                if card.type == "Hero":
                    view = HeroView(self.screen, card, x, y, state)
                elif card.type == "Action":
                    view = ActionView(self.screen, card, x, y, state)
                else:
                    view = CardView(self.screen, card, x, y, state)
                if state == "used":
                    y -= 20
                self.drawable_cards.append(view)

        #ARMY
        y = 200
        for i, card in enumerate(self.opponent.army):
            x = 140 + i * (card_width + 20)
            if not self.opponent_army_visible:
                x = self.screen_width * 2
            view = HeroView(self.screen, card, x, y, "used" if card in used else "active")
            self.drawable_cards.append(view)

            # SHOP
        y = 80 + self.base_y
        if self.shop_visible:
            for i, card in enumerate(self.shop_to_buy):
                x = self.screen_width // 2 - 6 * (card_width + 20) // 2 + i * (card_width + 20)
                if card.type == "Hero":
                    view = HeroView(self.screen, card, x, y, "shop")
                elif card.type == "Action":
                    view = ActionView(self.screen, card, x, y, "shop")
                else:
                    view = CardView(self.screen, card, x, y, "shop")
                self.active_cards.append(view)
                self.drawable_cards.append(view)
            x = self.screen_width // 2 + 2 * (card_width + 20)
            for i in range(5):
                view = CardView(self.screen, self.shop_deck.cards[0], x + 2 * i, y - 3 * i, "face_down")
                self.drawable_cards.append(view)

    def opponent_turn(self):

        points = [[self.screen_width // 2, self.screen_height + 50 * i] for i in
                  range(self.player.attack_power)]
        if len(points) > 0:
            while points[-1][1] > -200:
                for point in points:
                    point[1] -= 20
                self.draw()
                for point in points:
                    pygame.draw.line(self.screen, (200, 0, 0), point, (point[0] - 200, point[1] + 100), 10)
                    pygame.draw.line(self.screen, (200, 0, 0), point, (point[0] + 200, point[1] + 100), 10)
                pygame.display.update()
                if points[len(points)//2][1] < self.screen_height//2:
                    self.scrolling_speed = 20
                    while self.base_y <= 20 + self.screen_height * 2 // 3:
                        self.draw()
                        for point in points:
                            pygame.draw.line(self.screen, (200, 0, 0), point, (point[0] - 200, point[1] + 100), 10)
                            pygame.draw.line(self.screen, (200, 0, 0), point, (point[0] + 200, point[1] + 100), 10)
                        pygame.display.update()
                        self.base_y += self.scrolling_speed
                        for view in self.drawable_cards + self.buttons:
                            view.y += self.scrolling_speed
                            view.update_rect()

            self.opponent.health -= self.player.attack_power

        self.player.reset()
        self.scrolling_speed = 20
        while self.base_y <= 20 + self.screen_height * 2 //3:
            self.draw()
            pygame.display.update()
            self.base_y += self.scrolling_speed
            for view in self.drawable_cards + self.buttons:
                view.y += self.scrolling_speed
                view.update_rect()

        self.opponent.cards_in_front_of_me = self.opponent.deck.draw(self.opponent.cards_to_draw)
        self.update_card_views()
        self.draw()
        pygame.display.update()
        time.sleep(1)
        for card in self.opponent.cards_in_front_of_me:
            card.use(self.opponent)
            for view in self.drawable_cards:
                if view.card == card:
                    view.state = "used"
                    view.y += 20
            self.draw()
            pygame.display.update()
            time.sleep(0.5)
        time.sleep(1)

        while self.base_y > -40 + self.screen_height * 2 //3:
            self.draw()
            pygame.display.update()
            self.base_y -= self.scrolling_speed
            for view in self.drawable_cards + self.buttons:
                view.y -= self.scrolling_speed
                view.update_rect()
        #BUYING
        can_buy = [ x for x in self.shop_to_buy if x.value <= self.opponent.coins]
        while len(can_buy) > 0:
            card = random.choice(can_buy)
            temp = ""
            for view in self.drawable_cards:
                if view.card == card:
                    temp = view
            discarded = ""

            dy = (temp.y + 210)
            for i in range(20):
                temp.y -= dy//20
                self.draw()
                pygame.display.update()
            self.opponent.deck.add_to_discarded(card)
            self.opponent.coins -= card.value
            index = self.shop_to_buy.index(card)
            self.shop_to_buy.remove(card)
            self.shop_to_buy.insert(index, self.shop_deck.draw(1)[0])
            self.update_card_views(if_buying=True)
            self.draw()
            pygame.display.update()
            time.sleep(1)
            can_buy = [x for x in self.shop_to_buy if x.value <= self.opponent.coins]
        #Attack
        points = [[self.screen_width//2,-50*i] for i in range(self.opponent.attack_power)]
        if len(points) > 0:
            while points[-1][1]<self.screen_height + 100:
                for point in points:
                    point[1] += 20
                self.draw()
                for i, point in enumerate(points):
                    pygame.draw.line(self.screen,(200,0,0),point,(point[0]-200,point[1]-100),10)
                    pygame.draw.line(self.screen, (200, 0, 0), point, (point[0] + 200, point[1] - 100),10)
                if points[len(points)//2][1] > self.screen_height//2:
                    self.scrolling_speed = -20
                    while self.base_y > 0:
                        self.draw()
                        for i, point in enumerate(points):
                            pygame.draw.line(self.screen, (200, 0, 0), point, (point[0] - 200, point[1] - 100), 10)
                            pygame.draw.line(self.screen, (200, 0, 0), point, (point[0] + 200, point[1] - 100), 10)
                        pygame.display.update()
                        self.base_y += self.scrolling_speed
                        for view in self.drawable_cards + self.buttons:
                            view.y += self.scrolling_speed
                            view.update_rect()
                    self.scrolling_speed = 0

                pygame.display.update()
            self.player.health -= self.opponent.attack_power



        self.opponent.deck.discarded.extend(self.opponent.cards_in_front_of_me)
        self.opponent.cards_in_front_of_me = []
        self.update_card_views()
        self.opponent.reset()
        self.draw()
        pygame.display.update()
        time.sleep(2)

        self.scrolling_speed = -20
        while self.base_y > 0:
            self.draw()
            pygame.display.update()
            self.base_y += self.scrolling_speed
            for view in self.drawable_cards + self.buttons:
                view.y += self.scrolling_speed
                view.update_rect()
        self.scrolling_speed = 0
        self.turn = "Player"

    def move_up(self):
        self.army_visible = False
        self.shop_visible = True
        self.turn = "Opponent"
        self.goal_y = 800
        self.goal_y_set = True
        if len(self.attack_points) >= self.opponent.health:
            return
        if self.if_opponent_first_turn:
            t = Timer(3000, self.opp_speak)
        else:
            t = Timer(1000, self.opp_speak)
        t.activate()
        self.timers.append(t)


    def opp_draw(self):
        self.opponent.cards_in_front_of_me = self.opponent.deck.draw(self.opponent.cards_to_draw)
        self.update_card_views()
        t = Timer(1000,self.opp_bef_use)
        t.activate()
        self.timers.append(t)

    def opp_speak(self):
        self.bcg_color = (26, 87, 23)
        temp = random.choice(opponent_game_lines)
        if self.if_opponent_first_turn:
            self.if_opponent_first_turn = False
            temp = random.choice(opponent_opening_lines)
        if self.opponent.health <= 0:
            temp = random.choice(opponent_dead_lines)
        if self.player.health <= 0:
            temp = random.choice(opponent_victory_lines)
        for i in range(len(temp)):
            t = Timer(100*i,self.opp_speak_gen(temp,i))
            t.activate()
            self.timers.append(t)
        t = Timer(100*len(temp)+2500,self.opp_speak_gen(temp,-1))
        t.activate()
        self.timers.append(t)

        if self.opponent.health > 0 and self.player.health >0:
            t = Timer(100 * len(temp) + 1500, self.opp_draw)
            t.activate()
            self.timers.append(t)

    def opp_speak_gen(self, text, index):
        def sub_fun():
            if index == -1:
                self.opponent_dialog = ""
                self.bcg_color = (36, 107, 33)
            else:
                self.opponent_dialog = text[0:index+1]
        return sub_fun

    def opp_bef_use(self):
        self.goal_y_set = True
        self.goal_y = 450
        t = Timer(2000, self.opp_use)
        t.activate()
        self.timers.append(t)


    def opp_use(self):
        self.opp_stats_vertical = True
        used = False
        for card in self.opponent.cards_in_front_of_me:
            for view in self.drawable_cards:
                if view.card == card and view.state == "active":
                    card.use(self.opponent)
                    card.use_with_alliance(self.opponent)
                    view.state = "used"
                    if card.type == "Hero":
                        self.opponent.army.append(card)
                        self.opponent.cards_in_front_of_me.remove(card)
                        used = True
                        self.update_card_views(if_buying=True)
                        break

                    self.update_card_views(if_buying=True)
                    used = True


            if used:
                break
        if used:
            t = Timer(500,self.opp_use)
            t.activate()
            self.timers.append(t)
        else:
            t = Timer(500, self.opp_use_army)
            t.activate()
            self.timers.append(t)

    def opp_use_army(self):
        self.opponent_army_visible = True
        self.update_card_views(True)
        used = False
        for card in self.opponent.army:
            for view in self.drawable_cards:
                if view.card == card and view.state == "active":
                    self.opponent_dialog = "I use my " + card.name
                    card.use(self.opponent)
                    card.use_with_alliance(self.opponent)
                    view.state = "used"
                    self.update_card_views(if_buying=True)
                    used = True

            if used:
                break
        if used:
            t = Timer(500, self.opp_use)
            t.activate()
            self.timers.append(t)
        else:
            t = Timer(500, self.opp_buy)
            t.activate()
            self.timers.append(t)

    def opp_buy(self):
        self.opponent_dialog = ""
        self.opponent_army_visible = False
        cards_available_to_buy = [x for x in self.shop_to_buy if x.value <= self.opponent.coins]
        if len(cards_available_to_buy) != 0:
            chosen = random.choice(cards_available_to_buy)
            self.opponent.coins -= chosen.value
            view = [x for x in self.drawable_cards if x.card == chosen][0]
            self.cards_up.append(view)

            index = self.shop_to_buy.index(chosen)
            self.shop_to_buy.remove(chosen)
            self.shop_to_buy.insert(index, self.shop_deck.draw(1)[0])
            self.update_card_views(True)
            self.drawable_cards.append(view)

            t = Timer(2000,self.opp_buy)
            t.activate()
            self.timers.append(t)
        else:
            t = Timer(2000, self.move_down)
            t.activate()
            self.timers.append(t)


    def move_down(self):
        self.opponent.deck.discard(self.opponent.cards_in_front_of_me)
        self.opponent.cards_in_front_of_me = []
        self.goal_y_set = True
        self.goal_y = 0
        self.update_card_views()
        self.add_attack_opponent()
        t = Timer(1000, self.opp_reset)
        t.activate()
        self.timers.append(t)


    def opp_reset(self):
        self.turn = "Player"
        self.opponent.reset()
        self.opp_stats_vertical = True
        self.update_card_views()
        self.timers = [t for t in self.timers if t.active]





if __name__ == "__main__":
    game = Game()
    if False:
        while len(game.player.deck.cards) <12:
            x = random.choice(game.shop_deck.cards)
            if x.type == "Hero":
                game.player.deck.cards.append(x)
                game.shop_deck.cards.remove(x)
    random.shuffle(game.player.deck.cards)
    if False:
        while len(game.opponent.deck.cards) <12:
            x = random.choice(game.shop_deck.cards)
            if x.type == "Hero":
                game.opponent.deck.cards.append(x)
                game.shop_deck.cards.remove(x)
    random.shuffle(game.opponent.deck.cards)
    game.run()

