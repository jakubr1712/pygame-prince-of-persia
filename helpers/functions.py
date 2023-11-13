from settings import *


def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg(screen, resources):
    screen.fill(BG)
    width = resources['sky_img'].get_width()
    for x in range(5):
        screen.blit(resources['sky_img'], ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(resources['mountain_img'], ((x * width) - bg_scroll * 0.6,
                    SCREEN_HEIGHT - resources['mountain_img'].get_height() - 300))
        screen.blit(resources['pine1_img'], ((x * width) - bg_scroll * 0.7,
                    SCREEN_HEIGHT - resources['pine1_img'].get_height() - 150))
        screen.blit(resources['pine2_img'], ((x * width) - bg_scroll * 0.8,
                    SCREEN_HEIGHT - resources['pine2_img'].get_height()))
