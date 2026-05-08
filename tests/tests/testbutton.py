import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from view.button_view import ButtonView

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test ButtonView")
clock = pygame.time.Clock()

test_btn = ButtonView(300, 250, 200, 50, "Test Button")

running = True
while running:
    screen.fill((235, 245, 255))

    test_btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            test_btn.handle_click(event.pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()