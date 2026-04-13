import pygame
import models
import config

pygame.init()
mainScreen=pygame.display.set_mode(config.screenSize)
isRunning=True
clock = pygame.time.Clock()
dt=0
player_pos = pygame.Vector2(mainScreen.get_width() / 2, mainScreen.get_height() / 2)
while isRunning:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            isRunning=False
            break
    mainScreen.fill("purple")

    pygame.draw.circle(mainScreen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()

