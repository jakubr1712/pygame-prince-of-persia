import os
import pygame
from settings import TILE_SIZE, TILE_TYPES


def load_resources(base_dir):
    resources = {}

    resources["pine1_img"] = pygame.image.load(
        os.path.join(base_dir, "img/Background/pine1.png")
    ).convert_alpha()
    resources["pine2_img"] = pygame.image.load(
        os.path.join(base_dir, "img/Background/mountain.jpeg")
    ).convert_alpha()
    resources["mountain_img"] = pygame.image.load(
        os.path.join(base_dir, "img/Background/mountain.jpeg")
    ).convert_alpha()
    resources["sky_img"] = pygame.image.load(
        os.path.join(base_dir, "img/Background/sky_cloud.png")
    ).convert_alpha()
    resources["start_button_image"] = pygame.image.load(
        os.path.join(base_dir, "img/start_btn.png")
    ).convert_alpha()

    resources["img_list"] = []
    for x in range(TILE_TYPES):
        try:
            img = pygame.image.load(os.path.join(
                base_dir, f"img/Tile/{x}.png"))
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            resources["img_list"].append(img)
        except FileNotFoundError:
            img = pygame.image.load(os.path.join(
                base_dir, f"img/Tile/{x + 1}.png"))
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            resources["img_list"].append(img)

    resources["font"] = pygame.font.SysFont("Futura", 30)

    return resources
