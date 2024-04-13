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

        self.cards_to_choose = []
        self.reason_to_choose = "default"
        self.choose_index = 0

        self.buttons = []
        self.set_buttons()

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

        self.cards_to_choose = []
        self.reason_to_choose = "default"
        self.choose_index = 0


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

        def func_left():
            self.choose_index -= 1
        self.button_choose_index_left = Button(self.screen, "<-",100, 500, function= func_left)
        self.button_choose_index_left.state = "hidden"
        self.buttons.append(self.button_choose_index_left)

        def func_right():
            self.choose_index += 1
        self.button_choose_index_right = Button(self.screen, "->",1100, 500, function= func_right)
        self.button_choose_index_right.state = "hidden"
        self.buttons.append(self.button_choose_index_right)

        self.button_choose_action = Button(self.screen, "No, thanks", self.screen_width//2 - 60, self.screen_height - 100)
        self.button_choose_action.state = "hidden"
        self.buttons.append(self.button_choose_action)



    def run(self, if_ommit_info = False):
        if not if_ommit_info:
            self.intro()
        else:
            self.who_starts()
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
                if abs(self.base_y - self.goal_y) >= 10:
                    self.scrolling_speed = 10 if self.base_y < self.goal_y else -10
                else:
                    self.scrolling_speed = 0
                    self.goal_y_set = False


            for event in pygame.event.get():
                self.handle_events(event)
            self.draw()
            self.move_cards()
            if self.cards_to_choose:
                self.draw_cards_to_choose(self.cards_to_choose)

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

        self.random_fade_in()

        self.turn = x
        if x == "Opponent":
            self.update_card_views()
            self.move_up()


    def random_fade_in(self):
        self.update_card_views()
        x = random.randint(1,5)
        if x == 1:
            for i in range(100):
                self.draw()
                pygame.draw.rect(self.screen, "black",
                                 (-i * self.screen_width / 200, 0, self.screen_width // 2, self.screen_height))
                pygame.draw.rect(self.screen, "black",
                                 ((100 + i) * self.screen_width / 200, 0, self.screen_width // 2, self.screen_height))
                pygame.display.update()
        elif x == 2:
            for i in range(100):
                self.draw()
                pygame.draw.rect(self.screen, "black",
                                 (0, -i*self.screen_height//200, self.screen_width, self.screen_height//2))
                pygame.draw.rect(self.screen, "black",
                                 (0, (100+i)*self.screen_height//200, self.screen_width, self.screen_height//2))
                pygame.display.update()
        elif x == 3:
            for i in range(100):
                self.draw()
                for x in range(10):
                    for y in range(10):
                        if 10*x + y >= i:
                            pygame.draw.rect(self.screen, "black", (x*self.screen_width//10, y*self.screen_height//10, 5+self.screen_width//10, 5+self.screen_height//10))
                pygame.display.update()
        elif x==4:
            for i in range(100):
                self.draw()
                for x in range(10):
                    for y in range(10):
                        if 10*y + x >= i:
                            pygame.draw.rect(self.screen, "black", (x*self.screen_width//10, y*self.screen_height//10, 5+ self.screen_width//10, 5+self.screen_height//10))
                pygame.display.update()
        elif x==5:
            for i in range(100):
                self.draw()
                pygame.draw.circle(self.screen,"black",(self.screen_width//2, self.screen_height//2),self.screen_width*(100-i)//100)
                pygame.display.update()



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
                        if self.can_i_kill_someone():
                            self.cards_to_choose = self.opponent.army
                        else:
                            self.add_attack_player()
                            self.player.reset()
                            self.move_up()
                        #self.opponent_turn()



                    else:
                        if self.cards_to_choose:
                            return
                        self.player.cards_in_front_of_me = self.player.deck.draw(self.player.cards_to_draw)
                        self.update_card_views()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.scrolling_speed = 0
                elif event.key == pygame.K_DOWN:
                    self.scrolling_speed = 0
                elif event.key == pygame.K_f:
                    temp = (self.screen_width, self.screen_height)
                    self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    self.screen_width = self.screen.get_width()
                    self.screen_height = self.screen.get_height()
                    if temp == (self.screen_width, self.screen_height):
                        self.screen = pygame.display.set_mode((1300, 786))
                        self.screen_width = self.screen.get_width()
                        self.screen_height = self.screen.get_height()
                    self.update_card_views(True)
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
                        if self.player.cards_to_sacrifice:
                            self.cards_to_choose = self.player.deck.discarded + self.player.cards_in_front_of_me
                            self.reason_to_choose = "sacrifice"
                        if self.player.cards_to_discard > 0:
                            for _ in range(self.player.cards_to_discard):
                                self.player.cards_in_front_of_me.append(self.player.deck.draw(1)[0])
                            self.cards_to_choose = self.player.cards_in_front_of_me
                            self.reason_to_choose = "discard"

                        if self.player.heroes_to_block > 0:
                            self.cards_to_choose = self.player.opponent.army
                            if len(self.cards_to_choose) > 0:
                                self.reason_to_choose = "block"
                            else:
                                self.player.heroes_to_block = 0

                        if self.player.cards_to_resurect > 0:
                            self.cards_to_choose = self.player.deck.discarded
                            if len(self.cards_to_choose) > 0:
                                self.reason_to_choose = "resurect"
                            else:
                                self.player.cards_to_resurect = 0

                        if self.player.heroes_to_resurect > 0:
                            self.cards_to_choose = [card for card in self.player.deck.discarded if card.type == "Hero"]
                            if len(self.cards_to_choose) > 0:
                                self.reason_to_choose = "resurect"
                            else:
                                self.player.heroes_to_resurect = 0




                        if self.player.heroes_to_reactivate:
                            temp = []
                            for hero in self.player.army:
                                for view in self.drawable_cards:
                                    if view.card == hero and view.state == "used":
                                        temp.append(hero)
                            if temp:
                                self.cards_to_choose = temp
                                self.reason_to_choose = "reactivate"
                            else:
                                self.player.heroes_to_reactivate = 0
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
                    elif card.state == "to_kill":
                        if not card.card.if_guardian and len([hero for hero in self.opponent.army if hero.if_guardian]):
                            self.timers = []
                            self.opponent_dialog = "You have to kill my Guardians first!"
                            t = Timer(2000, self.opp_speak_gen("",-1))
                            t.activate()
                            self.timers.append(t)
                        elif card.card.health > self.player.attack_power:
                            self.timers = []
                            self.opponent_dialog = "You don't have enough power to kill my Hero!"
                            t = Timer(2000, self.opp_speak_gen("", -1))
                            t.activate()
                            self.timers.append(t)
                        else:
                            self.player.attack_power -= card.card.health
                            self.opponent.deck.add_to_discarded(card.card)
                            self.opponent.army.remove(card.card)
                            self.timers = []
                            self.opponent_dialog = "You killed my " + card.card.name
                            t = Timer(2000, self.opp_speak_gen("", -1))
                            t.activate()
                            self.timers.append(t)
                            if not self.can_i_kill_someone():
                                self.hide_chose_window()
                                self.add_attack_player()
                                self.player.reset()
                                self.update_card_views()
                                self.timers = []
                                self.move_up()
                    elif card.state == "to_sacrifice":
                        self.player.attack_power += self.player.sacrifice_bonus
                        if card.card in self.player.cards_in_front_of_me:
                            self.player.cards_in_front_of_me.remove(card.card)
                        else:
                            self.player.deck.discarded.remove(card.card)
                        self.timers = []
                        self.opponent_dialog = "You sacrificed your " + card.card.name
                        if self.player.sacrifice_bonus > 0:
                            self.opponent_dialog = self.opponent_dialog + " and got " + str(self.player.sacrifice_bonus) + " attack points!"
                        t = Timer(2000, self.opp_speak_gen("", -1))
                        t.activate()
                        self.timers.append(t)
                        self.player.cards_to_sacrifice -= 1
                        self.player.cards_to_draw -= 1
                        if self.player.cards_to_sacrifice == 0:
                            self.hide_chose_window()
                            self.player.sacrifice_bonus = 0
                        else:
                            self.cards_to_choose.remove(card.card)
                            self.update_card_views(True)
                    elif card.state == "to_reactivate":
                        for view in self.drawable_cards:
                            if view.card == card.card:
                                view.state = "active"
                        self.timers = []
                        self.opponent_dialog = "You reactivated your " + card.card.name
                        t = Timer(2000, self.opp_speak_gen("", -1))
                        t.activate()
                        self.timers.append(t)
                        self.player.heroes_to_reactivate = 0
                        self.hide_chose_window()
                    elif card.state == "to_discard":
                        self.player.cards_in_front_of_me.remove(card.card)
                        self.player.deck.discard([card.card])
                        self.player.cards_to_discard -= 1
                        if self.player.cards_to_discard == 0:
                            self.hide_chose_window()
                        else:
                            self.update_card_views(True)
                    elif card.state == "to_resurect":
                        self.player.deck.cards = [card.card] + self.player.deck.cards
                        self.player.deck.discarded.remove(card.card)
                        self.player.cards_to_resurect = 0
                        self.player.heroes_to_resurect = 0
                        self.hide_chose_window()
                    elif card.state == "to_block":
                        for view in self.drawable_cards:
                            if view.card == card.card:
                                view.state = "used"
                        self.player.heroes_to_block = 0
                        self.hide_chose_window()




                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_x, mouse_y) and button.state!="hidden":
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
                if self.opponent.next_bought_card_on_hand:
                    self.opponent.cards_in_front_of_me.append(view.card)
                    self.opponent.next_bought_card_on_hand -= 1
                elif self.opponent.next_bought_card_on_top:
                    self.opponent.deck.cards = [view.card] + self.opponent.deck.cards
                    self.opponent.next_bought_card_on_top -= 1
                elif self.opponent.next_bought_action_on_top and view.card.type == "Action":
                    self.opponent.deck.cards = [view.card] + self.opponent.deck.cards
                    self.opponent.next_bought_action_on_top -= 1
                else:
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
            if button.state == "active":
                button.draw()
        #self.draw_player_cards()

        # Clickable
        for view in self.active_cards+self.buttons:
            x, y = pygame.mouse.get_pos()
            if view.rect.collidepoint(x, y) and view.state!="hidden" and view.state!="used":
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
        if len([hero for hero in self.opponent.army if hero.if_guardian]) > 0:
            return
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
                if not self.army_visible and not self.cards_to_choose:
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
                    self.opp_special_use()
                    view.state = "used"
                    if card.type == "Hero":
                        self.opponent.cards_to_draw -= 1
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

    def opp_special_use(self):
        #DRAW A CARD
        while self.opponent.cards_to_draw > len(self.opponent.cards_in_front_of_me):
            self.opponent.cards_in_front_of_me.append(self.opponent.deck.draw(1)[0])
        # SACRIFICES
        while self.opponent.cards_to_sacrifice > 0:
            self.opponent.cards_to_sacrifice -= 1
            name = self.opponent.auto_sacrfice()
            if name:
                self.opponent_dialog = "I sacrifice my " + name
                if self.opponent.sacrifice_bonus > 0:
                    self.opponent_dialog = self.opponent_dialog + f" and i get {str(self.opponent.sacrifice_bonus)} attack points"
                    self.opponent.attack_power += self.opponent.sacrifice_bonus
            if self.opponent.cards_to_sacrifice == 0:
                self.opponent.sacrifice_bonus = 0

        # HERO REACTIVATIONS
        if self.opponent.heroes_to_reactivate > 0:
            temp = []
            for hero in self.opponent.army:
                for view in self.drawable_cards:
                    if view.card == hero and view.state == "used":
                        temp.append(view)
            if len(temp) > 0:
                ch = random.choice(temp)
                ch.state = "active"
                self.opponent_dialog = "I reactivate my " + ch.card.name
            self.opponent.heroes_to_reactivate = 0
        
        # STUN A HERO
        if len(self.player.army) >0 and self.opponent.heroes_to_block > 0 :
            hero = random.choice(self.player.army)
            for view in self.drawable_cards:
                if view.card == hero:
                    view.state = "used"
                    self.opponent_dialog = "I blocked your " + hero.name
                    self.opponent.heroes_to_block = 0
                    break

        #RESURECT A CARD
        if self.opponent.cards_to_resurect and self.opponent.deck.discarded:
            temp = self.opponent.deck.discarded
            temp.sort(key=lambda card: card.value,reverse=True)
            chosen = temp[0]
            self.opponent.deck.discarded.remove(chosen)
            self.opponent.deck.cards = [chosen] + self.opponent.deck.cards
            self.opponent.cards_to_resurect = 0

        # RESURECT A HERO
        if self.opponent.heroes_to_resurect and self.opponent.deck.discarded:
            temp = [card for card in self.opponent.deck.discarded if card.type=="Hero"]
            temp.sort(key=lambda card: card.value, reverse=True)
            if temp:
                chosen = temp[0]
                self.opponent.deck.discarded.remove(chosen)
                self.opponent.deck.cards = [chosen] + self.opponent.deck.cards
            self.opponent.heroes_to_resurect = 0

        # SWAP A CARD OR TWO
        while self.opponent.cards_to_discard > 0:
            temp = [card for card in self.opponent.cards_in_front_of_me]
            temp.sort(key=lambda card:card.value, reverse=True)
            chosen = temp[0]
            self.opponent.cards_in_front_of_me.remove(chosen)
            self.opponent.deck.discard([chosen])
            self.opponent.cards_to_discard -= 1


 

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
                    self.opp_special_use()
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
            temp = False
            for card in self.opponent.cards_in_front_of_me:
                for view in self.drawable_cards:
                    if view.card == card and view.state == "active":
                        temp = True
            if not temp:
                t = Timer(2000, self.move_down)
                t.activate()
                self.timers.append(t)
            else:
                self.opponent.cards_to_draw = len(self.opponent.cards_in_front_of_me)
                t = Timer(2000, self.opp_use)
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

    def draw_cards_to_choose(self, cards, mode="default"):
        self.update_card_views(True)
        button_left_hidden = False

        if self.reason_to_choose == "sacrifice":
            text1 ="Do you want to sacrifice any card?"
            text2 ="Cards to sacrifice:"
            def nope_func():
                self.hide_chose_window()
                self.player.cards_to_sacrifice = 0
                self.player.sacrifice_bonus = 0

            action = "to_sacrifice"

        elif self.reason_to_choose == "reactivate":

            text1 = "Do you want to reactivate a hero?"
            text2 = "Heroes available to reactivate:"
            def nope_func():
                self.hide_chose_window()
                self.player.heroes_to_reactivate = 0

            action = "to_reactivate"

        elif self.reason_to_choose == "discard":
            button_left_hidden = True
            ctd = self.player.cards_to_discard
            text1 = "You have to discard a card." if ctd == 1 else "You have to discard " + str(ctd) + " cards."
            text2 = "Choose a card:"
            action = "to_discard"
            while self.choose_index+5 < len(self.cards_to_choose):
                self.choose_index += 1

        elif self.reason_to_choose == "resurect":
            text1 = "You can take a card from the discarded pile and put it the top of your deck"
            text2 = "Choose a card:"
            action = "to_resurect"
            def nope_func():
                self.hide_chose_window()
                self.player.heroes_to_resurect = 0
                self.player.cards_to_resurect = 0

        elif self.reason_to_choose == "block":
            text1 = "You can block a hero of your opponent"
            text2 = "Opponents's party:"
            action = "to_block"
            def nope_func():
                self.hide_chose_window()
                self.player.heroes_to_block = 0


        else:
            text1 = "Do you want to attack any enemy's heroes first?"
            text2 = "Opponent's Party:"
            def nope_func():
                self.hide_chose_window()
                self.add_attack_player()
                self.player.reset()
                self.move_up()

            action = "to_kill"
        #DRAWING

        x = self.screen_width//2 - min(5,len(cards)) * 170//2
        y = self.screen_height//2
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 20 + 170 * min(5, len(cards)), 40 + 230))
        self.draw_text(text1, (250, 250, 250), self.screen_width//2, y - 50, size=30,
                       background="black", center=True)
        self.draw_text(text2, (250, 250, 250), self.screen_width//2, y + 10, background="black", center=True)

        for i, card in enumerate(cards[self.choose_index:self.choose_index + 5]):
            if card.type == "Hero":
                v = HeroView(self.screen, card, x + 20 + i * 170, y + 40, action)
            elif card.type == "Action":
                v = ActionView(self.screen, card, x + 20 + i * 170, y + 40, action)
            else:
                v = CardView(self.screen, card, x + 20 + i * 170, y + 40, action)
            v.draw()
            self.active_cards.append(v)

        if not button_left_hidden:
            self.button_choose_action.state = "active"
            self.button_choose_action.function = nope_func
        if self.choose_index>0:
            self.button_choose_index_left.state = "active"
        else:
            self.button_choose_index_left.state = "hidden"
        if len(cards) > self.choose_index + 5:
            self.button_choose_index_right.state = "active"
        else:
            self.button_choose_index_right.state = "hidden"

    def hide_chose_window(self):
        self.button_choose_action.state = "hidden"
        self.button_choose_index_left.state = "hidden"
        self.button_choose_index_right.state = "hidden"
        self.cards_to_choose = []
        self.reason_to_choose = "default"
        self.choose_index = 0
        self.update_card_views(True)


    def can_i_kill_someone(self):
        if not self.opponent.army:
            return False
        if not [hero for hero in self.opponent.army if hero.health <= self.player.attack_power]:
            return False
        guardians = [hero for hero in self.opponent.army if hero.if_guardian]
        if len(guardians) > 0 and len([hero for hero in guardians if hero.health < self.player.attack_power]) == 0:
            return False
        return True





if __name__ == "__main__":
    game = Game()
    if 0:
        while len(game.player.deck.cards) <20:
            x = random.choice(game.shop_deck.cards)
            if x.type == "Hero":
                game.player.deck.cards.append(x)
                game.shop_deck.cards.remove(x)
    random.shuffle(game.player.deck.cards)
    if 0:
        while len(game.opponent.deck.cards) <20:
            x = random.choice(game.shop_deck.cards)
            game.opponent.deck.cards.append(x)
            game.shop_deck.cards.remove(x)

  #  game.player.attack_power = random.randint(10,20)
    random.shuffle(game.opponent.deck.cards)
    """
    for _ in range(20):
        game.player.deck.add(Action("Dotyk Śmierci", "", [0,2,0, can_sacrifice()], 1, "red",
                    actions_if_alliance=[0,2,0]))
    for _ in range(3):
        game.player.deck.discarded.append(Card("Moneta", "+1 złoto", [1,0,0]))
    random.shuffle(game.player.deck.cards)
    """
    """
    for _ in range(9):
        game.player.deck.add(Action("Zwołanie Wojsk", "", [3, 0, 5, reactivate_hero()], 4, "yellow",
                        actions_if_alliance=[0, 0, 0]))
        game.player.deck.add(random.choice([x for x in game.shop_deck.cards if x.type == "Hero"]))
    """
    """""
    for _ in range(3):
        game.player.deck.add(Action("Dar Elfów", "", [2, 0, 0, swap_a_card()], 2, "green",
                        actions_if_alliance=[0, 4, 0]))
        game.player.deck.add(Action("Szał", "Ork", [0, 6, 0, swap_two_cards()], 6, "green"))
        game.player.deck.add(Action("Bomba Ogniowa", "", [0, 8, 0, stun_hero(), draw_card()], 8, "blue",
                    actions_if_destroyed=[0, 5, 0]))
        game.player.deck.add(Action("Niszczenie i Grabież", "", [0, 6, 0, resurrect_card()], 6, "blue",
                    actions_if_alliance=[0, 0, 6]))
        game.player.deck.add(Hero("Varrick", "Nekromanta", [0, 0, 0, resurrect_hero()], 3, 5, alliance="red", actions_if_alliance=[0,0,0,draw_card()]))
    game.opponent.coins = 20
    random.shuffle(game.player.deck.cards)
"""

    game.run()


