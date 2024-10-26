import pygame
from menu_button import MenuButton
from backgammon.bots.stupid_bot import StupidBot
from backgammon.bots.smart_bot import SmartBot
from backgammon.constants import HOTSEAT_BUTTON_PATH, STUPID_BOT_BUTTON_PATH, SMART_BOT_BUTTON_PATH


def run_menu(screen):
    background_image = pygame.image.load("assets/images/menu.png")
    background_image = pygame.transform.scale(background_image, screen.get_size())
    hotseat_button = MenuButton(0, HOTSEAT_BUTTON_PATH)
    stupid_bot_button = MenuButton(1, STUPID_BOT_BUTTON_PATH)
    smart_bot_button = MenuButton(2, SMART_BOT_BUTTON_PATH)

    while True:
        screen.blit(background_image, (0, 0))
        hotseat_button.draw(screen)
        stupid_bot_button.draw(screen)
        smart_bot_button.draw(screen)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if hotseat_button.is_pressed(mouse_pos):
                    return
                elif stupid_bot_button.is_pressed(mouse_pos):
                    return StupidBot()
                elif smart_bot_button.is_pressed(mouse_pos):
                    return SmartBot()

        pygame.display.update()