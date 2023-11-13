import csv
import os
import random

import pygame

from classes.button import Button
from classes.decoration import Decoration
from classes.exit import Exit
from classes.health_bar import HealthBar
from classes.water import Water
from helpers.functions import draw_bg, draw_text
from resources import load_resources
from settings import *

prince_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prince')

if os.path.exists(prince_dir):
    os.chdir(prince_dir)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prince of Persia")

clock = pygame.time.Clock()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
resources = load_resources(BASE_DIR)


start_button = Button(260, 250, resources["start_button_image"], screen)

enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
with open(f"level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (
            x + TILE_SIZE // 2,
            y + (TILE_SIZE - self.image.get_height()),
        )

    def update(self):
        self.rect.x += screen_scroll


class World:
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    if tile < TILE_TYPES:
                        img = resources["img_list"][tile]
                        img_rect = img.get_rect()
                        img_rect.x = x * TILE_SIZE
                        img_rect.y = y * TILE_SIZE
                        tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(
                            img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:

                        player = Character(
                            "player", x * TILE_SIZE, y * TILE_SIZE, 1.65, 5
                        )
                        health_bar = HealthBar(
                            10, 10, player.health.health, player.health.health, screen
                        )
                    elif tile == 16:
                        enemy = Character(
                            "enemy", x * TILE_SIZE, y * TILE_SIZE, 1.65, 2
                        )
                        enemy_group.add(enemy)

                    elif tile == 20:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Health:
    def __init__(self, character):
        self.character = character
        self.health = 100
        self.max_health = self.health

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.character.speed = 0
            self.character.alive = False
            self.character.update_action(3)


class Character(pygame.sprite.Sprite):
    def __init__(
        self,
        char_type,
        x,
        y,
        scale,
        speed,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.health = Health(self)
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        animation_types = ["Idle", "Run", "Jump", "Death", "Attack"]
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(
                f"img/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f"img/{self.char_type}/{animation}/{i}.png"
                ).convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale),
                          int(img.get_height() * scale))
                )
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.health.check_alive()

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump == True and self.in_air == False:
            self.vel_y = -13
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(
                self.rect.x + dx, self.rect.y, self.width, self.height
            ):
                dx = 0
                if self.char_type == "enemy":
                    self.direction *= -1
                    self.move_counter = 0
            if tile[1].colliderect(
                self.rect.x, self.rect.y + dy, self.width, self.height
            ):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if self.char_type == "player":
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.char_type == "player":
            if (
                self.rect.right > SCREEN_WIDTH - SCROLL_THRESH
                and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH
            ) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            if self.vision.colliderect(player.rect):
                self.update_action(0)

            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    self.vision.center = (
                        self.rect.centerx + 75 * self.direction,
                        self.rect.centery,
                    )

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        self.rect.x += screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


world = World()
player, health_bar = world.process_data(world_data)

can_jump = True
main_menu = True
run = True
while run:
    clock.tick(FPS)

    if main_menu:
        if start_button.draw():
            main_menu = False
    if not main_menu:
        draw_bg(screen, resources)
        world.draw()
        draw_text("HP", resources["font"], WHITE, 180, 13, screen)
        health_bar.draw(player.health.health)

        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()

        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

    if (
        pygame.sprite.spritecollide(player, water_group, False)
        or not player.alive
        or player.rect.y > 800
    ):
        player.health.health = -1
        text = my_font.render("Game Over!", False, (255, 255, 255))
        text2 = my_font.render("Press ESCAPE to exit", False, (255, 255, 255))
        screen.blit(text, (300, 300))
        screen.blit(text2, (240, 330))
        can_jump = False

    if player.alive:
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        screen_scroll = player.move(moving_left, moving_right)
        bg_scroll -= screen_scroll
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                player.update_action(4)

            if event.key == pygame.K_w and player.alive and can_jump:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        for enemy in enemy_group:
            if pygame.sprite.collide_rect(player, enemy):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.update_action(4)
                    if enemy.alive:
                        enemy.health.health -= 25
                        if enemy.health.health <= 0:
                            enemy.update_action(0)
                else:
                    if enemy.alive and player.alive:
                        player.health.health -= 2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
