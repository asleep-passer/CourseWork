import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from view.button_view import ButtonView
from view.dialog_view import DialogView

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

dialog = DialogView(200, 200, 400, 200)
dialog.set_message("Congratulations! Level Complete!")

ok_btn = ButtonView(350, 320, 100, 40, "OK", dialog.hide)
dialog.add_button(ok_btn)

show_btn = ButtonView(300, 100, 200, 50, "Show Dialog", dialog.show)

running = True
while running:
    screen.fill((235, 245, 255))
    show_btn.draw(screen)
    dialog.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            dialog.handle_click(event.pos)
            show_btn.handle_click(event.pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()