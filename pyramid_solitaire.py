from sprites import *
from settings import *
import pygame as pg
import random


class Game:
    def __init__(self):
        pg.init()
        self.file_dir = path.dirname(__file__)
        self.data_dir = path.join(self.file_dir, "data")
        self.img_dir = path.join(self.data_dir, "images")
        self.cards_img_dir = path.join(self.img_dir, "cards")
        self.outlined_cards_img_dir = path.join(self.img_dir, "cards_outlined")
        self.card_back = pg.image.load(path.join(self.img_dir, "card_back.png"))
        game_icon = pg.image.load(path.join(self.img_dir, "game_icon.png"))
        pg.display.set_icon(game_icon)
        self.game_window = pg.display.set_mode(SCREEN_DIMENSIONS)
        self.font_name = pg.font.match_font(FONT_NAME)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.playing = True
        self.running = True
        self.score = 0
        self.high_score = 0
        self.card_sum = 0
        self.card_pair = []
        self.card_identifier = []
        self.deck = []
        self.array = []
        # Init groups
        self.all_sprites = pg.sprite.Group()
        self.stack1 = pg.sprite.Group()
        self.stack2 = pg.sprite.Group()
        self.pyramid = pg.sprite.Group()
        self.discard_group = pg.sprite.Group()
        self.row1 = pg.sprite.Group()
        self.row2 = pg.sprite.Group()
        self.row3 = pg.sprite.Group()
        self.row4 = pg.sprite.Group()
        self.row5 = pg.sprite.Group()
        self.row6 = pg.sprite.Group()
        self.row7 = pg.sprite.Group()
        self.row8 = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        button1 = Button(self, STACK1_X_COORD, STACK1_Y_COORD)
        self.buttons.add(button1)
        self.all_sprites.add(button1)
        self.next_row = {1: self.row2,
                         2: self.row3,
                         3: self.row4,
                         4: self.row5,
                         5: self.row6,
                         6: self.row7,
                         7: self.row8}
        self.load_data()
        self.pyramid_coord_array()

    def create_deck(self):
        # create list of unique identifier strings for each card
        self.deck.clear()
        # face values
        for a in range(2, 11):
            self.card_identifier.append(str(a))
        # A, K, Q, J
        for b in range(4):
            self.card_identifier.append(royals[b])
        
        for card in range(4):
            for d in range(13):
                self.deck.append((self.card_identifier[d] + "of" + suits[card]))

        random.shuffle(self.deck)

    def pyramid_coord_array(self):
        x_coord, y_coord = PYRAMID_X_COORD, PYRAMID_Y_COORD
        self.array.append((int(x_coord), int(y_coord)))
        
        f = 0
        row_number = 1
        while row_number < 7:
            x_coord -= (CARD_WIDTH * (f + 2) - CARD_WIDTH / 2)
            y_coord += CARD_HEIGHT / 2

            row_number += 1
            f += 1
            e = 0
            while e < row_number:
                x_coord += CARD_WIDTH
                e += 1
                self.array.append((int(x_coord), int(y_coord)))

    def load_data(self):
        with open(path.join(self.data_dir, HS_FILE), 'r') as f:
            try:
                self.high_score = int(f.read())

            except:
                self.high_score = 0

    def new(self):
        # reset game then rerun
        pg.mouse.set_cursor(*pg.cursors.arrow)
        self.score = 0
        self.card_sum = 0
        self.all_sprites.empty()
        self.stack1.empty()
        self.stack2.empty()
        self.pyramid.empty()
        self.row1.empty()
        self.row2.empty()
        self.row3.empty()
        self.row4.empty()
        self.row5.empty()
        self.row6.empty()
        self.row7.empty()
        self.create_deck()
        self.initialize_sprites()
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            dt = self.clock.tick(FPS)
            t = dt / 1000.0
            self.events()
            self.update(t)
            self.draw()

    def events(self):
        # game loop
        for event in pg.event.get():
            # exit game event
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.playing:
                    self.playing = False
                self.running = False

            # check for mouse click
            elif event.type == pg.MOUSEBUTTONDOWN:
                for card in self.all_sprites:
                    if card.rect.collidepoint(pg.mouse.get_pos()):
                        if card in self.pyramid:
                            collide = pg.sprite.spritecollide(card, self.next_row[card.row_number], False)
                            if len(collide) == 0:
                                self.process_sprite(card)
                                return

                        # top card in stack1 has been clicked
                        elif card in self.stack1:
                            top_card_in_stack1 = self.stack1.sprites()[len(self.stack1.sprites()) - 1]
                            if card == top_card_in_stack1:
                                if len(self.card_pair) != 0:
                                    self.card_pair[0].outline = False
                                    self.card_pair.clear()
                                    self.card_sum = 0
                                    return

                                else:
                                    # transfer top card of stack 1 to top of stack 2
                                    self.stack1.remove(top_card_in_stack1)
                                    self.stack2.add(top_card_in_stack1)
                                    self.move_card((150 + (len(self.stack2) - 1) * 2),
                                                   (10 + (len(self.stack2) - 1) * 2), top_card_in_stack1, 8)

                                    dt = self.clock.tick(FPS)
                                    t = dt / 1000.0
                                    self.all_sprites.update(t)
                                    self.draw()
                                    return

                        # top card in stack 2 has been clicked
                        elif card in self.stack2:
                            top_card_in_stack2 = self.stack2.sprites()[len(self.stack2.sprites()) - 1]
                            if card == top_card_in_stack2:
                                self.process_sprite(top_card_in_stack2)
                                return

                else:
                    if len(self.card_pair) > 0:
                        self.card_pair[0].outline = False
                        self.card_pair.clear()
                        self.card_sum = 0
                    # reset button pressed, empty stack 2 and reset stack 1
                    if len(self.stack1) == 0:
                        for button in self.buttons:
                            if button.rect.collidepoint(pg.mouse.get_pos()):
                                if len(self.card_pair) != 0:
                                    for card in self.card_pair:
                                        card.outline = False
                                    self.card_pair.clear()
                                    self.card_sum = 0
                                    return

                                for item in reversed(self.stack2.sprites()):
                                    n = (10 + (len(self.stack1)) * 2)
                                    item.rect.x = n
                                    item.rect.y = n
                                    item.set_destination(n, n)
                                    self.stack1.add(item)
                                    self.stack2.remove(item)
                                    dt = self.clock.tick(FPS)
                                    t = dt / 1000.0
                                    self.all_sprites.update(t)
                                    self.draw()
                                return

    def update(self, t):
        self.all_sprites.update(t)
        self.set_cursor()
        if self.is_game_over():
            self.playing = False

    def draw(self):
        # draw sprites and text to the game window
        self.game_window.fill(LIGHT_BLUE)
        if self.score > 0:
            self.game_window.blit(self.card_back, (DISCARD_X_COORD, DISCARD_Y_COORD))
        self.buttons.draw(self.game_window)
        self.pyramid.draw(self.game_window)
        self.stack1.draw(self.game_window)
        self.stack2.draw(self.game_window)
        self.discard_group.draw(self.game_window)
        self.draw_text("Score: " + str(self.score), 36, BLACK, 730, 30)
        pg.display.flip()

    def draw_text(self, text, size, colour, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game_window.blit(text_surface, text_rect)

    def initialize_sprites(self):
        # init card sprites
        pos = (STACK1_X_COORD, STACK1_Y_COORD)

        for index in (range(0, 52)):
            card = Card(self, pos, self.deck[index], 0)
            self.all_sprites.add(card)
            self.stack1.add(card)
            pos = (10 + len(self.stack1)*2, 10 + len(self.stack1)*2)

        dt = self.clock.tick(FPS)
        t = dt / 1000.0
        self.all_sprites.update(t)
        self.draw()
        pg.time.wait(170)

        for num in range(0, 28):
            c = self.stack1.sprites()[len(self.stack1) - 1]
            x, y = (self.array[num][0], self.array[num][1])
            c.set_vector((x, y))

            while c.rect.x != x and c.rect.y != y:
                dt = self.clock.tick(FPS)
                t = dt / 1000.0
                self.all_sprites.update(t)
                self.draw()

            self.stack1.remove(c)
            self.pyramid.add(c)

        for card in self.pyramid:
            if card.rect.y == PYRAMID_Y_COORD:
                self.row1.add(card)
                card.row_number = 1
            elif card.rect.y == PYRAMID_Y_COORD + HALF_CARD_HEIGHT:
                self.row2.add(card)
                card.row_number = 2
            elif card.rect.y == PYRAMID_Y_COORD + HALF_CARD_HEIGHT * 2:
                self.row3.add(card)
                card.row_number = 3
            elif card.rect.y == PYRAMID_Y_COORD + HALF_CARD_HEIGHT * 3:
                self.row4.add(card)
                card.row_number = 4
            elif card.rect.y == PYRAMID_Y_COORD + HALF_CARD_HEIGHT * 4:
                self.row5.add(card)
                card.row_number = 5
            elif card.rect.y == PYRAMID_Y_COORD + HALF_CARD_HEIGHT * 5:
                self.row6.add(card)
                card.row_number = 6
            elif card.rect.y == PYRAMID_Y_COORD + HALF_CARD_HEIGHT * 6:
                self.row7.add(card)
                card.row_number = 7

    def process_sprite(self, sprite):
        if len(self.card_pair) == 0:

            if sprite.value == 13:
                sprite.kill()
                self.all_sprites.add(sprite)
                self.stack1.add(sprite)
                self.discard_group.add(sprite)
                sprite.image = self.card_back
                sprite.set_vector((DISCARD_X_COORD, DISCARD_Y_COORD))
                sprite.flag = False
                while not sprite.flag:
                    dt = self.clock.tick(FPS)
                    t = dt / 1000.0
                    self.all_sprites.update(t)
                    self.draw()

                sprite.kill()
                self.score += 1
                return

            else:
                sprite.outline = True
                self.card_pair.append(sprite)
                self.card_sum += sprite.value
                return

        elif len(self.card_pair) == 1:
            self.card_pair.append(sprite)

            if self.card_pair[0] == self.card_pair[1]:
                sprite.outline = False
                self.card_pair.clear()
                self.card_sum = 0
                return

            else:
                self.card_sum += sprite.value

                if self.card_sum == 13:
                    for card in self.card_pair:
                        card.image = self.card_back

                    self.discard_cards(self.card_pair)
                    self.score = self.score + 2
                    self.card_sum = 0
                    self.card_pair.clear()
                    return

                else:
                    self.card_pair[0].outline = False
                    self.card_sum = 0
                    self.card_pair.clear()
                    return

    def set_cursor(self):

        for sprite in self.all_sprites:
            if sprite.rect.collidepoint(pg.mouse.get_pos()):
                if sprite in self.pyramid:
                    # card is contacting no cards in row below
                    if len(pg.sprite.spritecollide(sprite, self.next_row[sprite.row_number], False)) == 0:
                        pg.mouse.set_cursor(*pg.cursors.diamond)
                        return

                elif sprite in self.stack1:
                    top_card_in_stack1 = self.stack1.sprites()[len(self.stack1.sprites()) - 1]
                    
                    if top_card_in_stack1.rect.collidepoint(pg.mouse.get_pos()):
                        pg.mouse.set_cursor(*pg.cursors.diamond)
                        return
                    
                    else:
                        pg.mouse.set_cursor(*pg.cursors.arrow)
                        return

                elif sprite in self.stack2:
                    top_card_in_stack2 = self.stack2.sprites()[len(self.stack2.sprites()) - 1]
                    if top_card_in_stack2.rect.collidepoint(pg.mouse.get_pos()):
                        pg.mouse.set_cursor(*pg.cursors.diamond)
                        return

                    else:
                        pg.mouse.set_cursor(*pg.cursors.arrow)
                        return

        else:
            for button in self.buttons:
                if button.rect.collidepoint(pg.mouse.get_pos()) and len(self.stack1) == 0:
                    pg.mouse.set_cursor(*pg.cursors.diamond)
                    return

            pg.mouse.set_cursor(*pg.cursors.arrow)
            return

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    waiting = False
                    self.running = False

                if event.type == pg.KEYUP and event.key == pg.K_SPACE:
                    waiting = False

    def show_start_screen(self):
        self.game_window.fill(LIGHT_BLUE)
        self.draw_text("Pyramid Solitaire", 100, BLACK, SCREEN_DIMENSIONS[0] // 2, (SCREEN_DIMENSIONS[1] // 2) - 50)
        self.draw_text("Press space to start", 24, RED, SCREEN_DIMENSIONS[0] // 2, (SCREEN_DIMENSIONS[1] // 2) + 20)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        
        self.draw_text("GAME OVER", 50, RED, (SCREEN_DIMENSIONS[0] // 2) + 20, 25)
        if self.score > self.high_score:
            self.draw_text("New High Score = " + str(self.score), 25, RED, (SCREEN_DIMENSIONS[0] // 2) + 20, 60)
            self.draw_text("(press space to play again)", 20, RED, (SCREEN_DIMENSIONS[0] // 2) + 20, 80)
            with open(path.join(self.data_dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("(press space to play again)", 20, RED, (SCREEN_DIMENSIONS[0] // 2) + 20, 60)

        pg.display.flip()
        self.wait_for_key()

    def is_game_over(self):
        playable_card_values = []
        stack2_card_values = []
        playable_card_values_copy = []

        if len(self.stack1) == 0:
            # create an array of playable cards from the pyramid
            for card in self.pyramid:
                collide = pg.sprite.spritecollide(card, self.next_row[card.row_number], False)
                if len(collide) == 0:
                    if card.value == 13:
                        return False
                    playable_card_values.append(card.value)

                playable_card_values_copy = playable_card_values.copy()
            # create an array of card values from the cards in stack2
            for card in self.stack2:
                if card.value == 13:
                    return False

                else:
                    stack2_card_values.append(card.value)

            for element in playable_card_values:
                for value in playable_card_values_copy:
                    if element + value == 13:
                        return False

                for number in stack2_card_values:
                    if number + element == 13:
                        return False

            else:
                return True

        # stack1 is not empty
        else:
            return False

    def move_card(self, x, y, card, speed=35):
        starting_pos = card.rect.topleft
        while card.rect.topleft != (x, y):
            if card.rect.x != x:
                if starting_pos[0] < x:
                    if card.rect.x + speed >= x:
                        card.rect.x += 1
                        
                    elif card.rect.x + speed < x:
                        card.rect.x += speed

                elif starting_pos[0] > x:
                    if card.rect.x - speed <= x:
                        card.rect.x -= 1
                        
                    elif card.rect.x - speed > x:
                        card.rect.x -= speed

            if card.rect.y != y:
                if starting_pos[1] < y:
                    if card.rect.y + speed >= y:
                        card.rect.y += 1
                        
                    elif card.rect.y + speed < y:
                        card.rect.y += speed

                elif starting_pos[1] > y:
                    if card.rect.y - speed <= y:
                        card.rect.y -= 1
                        
                    elif card.rect.y - speed > y:
                        card.rect.y -= speed

            self.draw()
            pg.display.flip()

    def discard_cards(self, cards):
        discard_coords = (DISCARD_X_COORD, DISCARD_Y_COORD)
        card1 = cards[0]
        card2 = cards[1]
        self.stack1.add(card1)
        self.stack1.add(card2)
        card1.set_vector(discard_coords)
        card2.set_vector(discard_coords)
        card1.flag = False
        card2.flag = False

        while not card1.flag or not card2.flag:
            dt = self.clock.tick(FPS)
            t = dt / 1000.0
            self.all_sprites.update(t)
            self.draw()

        card1.kill()
        card2.kill()


# Create an instance of the game object
game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pg.quit()
