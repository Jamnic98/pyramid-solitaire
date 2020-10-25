import pygame as pg
from os import path


# Class for creating card objects
class Card(pg.sprite.Sprite):

    def __init__(self, game, position, card_name, row_number):
        pg.sprite.Sprite.__init__(self)

        self.card_value_table = {"A": 1,
                                 "2": 2,
                                 "3": 3,
                                 "4": 4,
                                 "5": 5,
                                 "6": 6,
                                 "7": 7,
                                 "8": 8,
                                 "9": 9,
                                 "1": 10,
                                 "J": 11,
                                 "Q": 12,
                                 "K": 13}

        self.game = game
        self.pic = pg.image.load(path.join(game.cards_img_dir, card_name + ".png")).convert()
        self.outline_image = pg.image.load(path.join(game.outlined_cards_img_dir, card_name + ".png")).convert()
        self.card_back_image = pg.image.load(path.join(game.img_dir, "card_back.png")).convert()
        self.image = self.pic
        self.outline = False
        self.rect = self.image.get_rect(topleft=position)
        self.value = self.card_value_table[card_name[0]]
        self.row_number = row_number

        self.flag = False

        self.destination = pg.math.Vector2()

        self.destination.x = self.rect.x
        self.destination.y = self.rect.y

        self.heading = pg.math.Vector2()

        self.change = pg.math.Vector2()

        self.speed = 0

    def set_vector(self, mpos):
        self.destination.x = mpos[0]
        self.destination.y = mpos[1]
        self.heading.x = self.destination.x - self.rect.x
        self.heading.y = self.destination.y - self.rect.y

        if self.heading != (0, 0):
            self.heading = self.heading.normalize()

    def move(self, dt):

        self.change = (self.heading * self.speed * dt)
        self.rect.x += self.change.x
        self.rect.y += self.change.y

    def set_destination(self, x, y):
        self.destination.x = x
        self.destination.y = y

    def update(self, dt):

        if self in self.game.stack1:
            self.image = self.card_back_image

        else:
            if self.outline:
                self.image = self.outline_image

            else:
                self.image = self.pic

        if (self.rect.x != self.destination.x) or (self.rect.y != self.destination.y):
            self.flag = False
            self.move(dt)
            if abs(self.destination.x - self.rect.x) <= 50 and abs(self.destination.y - self.rect.y) <= 50:
                self.speed = 0
                self.rect.x = int(self.destination.x)
                self.rect.y = int(self.destination.y)
                self.flag = True

            else:
                self.speed = 3000


# Class for creating interactive buttons
class Button(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(game.img_dir, "reset_image.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, t):
        pass
