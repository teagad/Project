from ctypes import alignment
import pygame
import pygame_menu
from time import sleep
from src.bot import Bot
#from src.menu import Menu
from src.background import Background
from src.player import Player
from src.singleton import Singleton




class BattleshipsCOMP:

    def __init__(self):
        self.step_bot()

    def fleet_sunk(self, player):
        for row in player.field.field:
            for element in row:
                if element == "U":
                    return False
        return True

    def victory_message(self):
        back_ground = Background('asserts/bg_pic.jpg', [0, 0])
        Singleton.screen.blit(back_ground.image, back_ground.rect)
        vic = Background('asserts/victory.png', [0, 0])
        Singleton.screen.blit(vic.image, vic.rect)
        pygame.display.update()

    def lose_message(self):
        back_ground = Background('asserts/bg_pic.jpg', [0, 0])
        self.screen.blit(back_ground.image, back_ground.rect)
        vic = Background('assers/defeat.png', [0, 0])
        Singleton.screen.blit(vic.image, vic.rect)
        pygame.display.update()
    
    ###START__________

    def step_bot(self):
        pygame.init()
        block_size = Singleton.block_size
        left_margin = Singleton.left_margin
        upper_margin = Singleton.upper_margin
        screen = Singleton.screen

        def start_the_game():
            WHITE = Singleton.WHITE
            font_size = int(block_size / 1.5)
            font = pygame.font.SysFont('notosans', font_size)
            pygame.display.set_caption("Морской бой")
            screen.fill(WHITE)
            pygame.display.update()

            self.draw_grid(font)
            self.sign_grids()
            pygame.display.update()

            c = Bot()
            c.set_compu_fleet()

            p = Player()
            p.set_fleet(Singleton.regime.get_value()[1])
            pygame.display.update()

            
            game_over = False
            param = False  # если false то игрок ходит первым. иначе первым ходит бот
            while not game_over:
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                    elif event.type == pygame.MOUSEBUTTONDOWN and not param:
                        x, y = event.pos
                        if (left_margin <= x <= left_margin + 10 * block_size) and (
                                upper_margin <= y <= upper_margin + 10 * block_size):
                            param = p.strike(c, ((x - left_margin) // block_size), ((y - upper_margin) // block_size))
                            print(param)
                        else:
                            print("Out of range")
                            param = False

                if self.fleet_sunk(c) is True:
                    game_over = True
                    self.victory_message()
                    sleep(3)
                    break
                elif param:
                    sleep(0.5)
                    param = c.compu_strike(p)
                    print("bot step")
                    if self.fleet_sunk(p) is True:
                        game_over = True
                        sleep(3)
                        self.lose_message()
                        break
                    else:
                        pygame.display.update()

        back_ground = Background('asserts/bg_pic.jpg', [0, 0])
        font = pygame_menu.font.FONT_FRANCHISE
        mytheme = pygame_menu.Theme(
            background_color=(40, 41, 35),
            title_font_shadow=True,
            widget_padding=25,
            selection_color=(255, 255, 255), 
            widget_font_color=(255, 255, 0),
            widget_font=font
            )
        mytheme.set_background_color_opacity(0.6)
        menu = pygame_menu.Menu('', 1240, 650, theme=mytheme)
        Singleton.USER_NAME = menu.add.text_input('NAME :')
        Singleton.regime = menu.add.selector('REGIME : ', [('Fog of War', False), ('Simple', True)])        
        menu.add.button('PLAY', start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        while True:
            screen.blit(back_ground.image, back_ground.rect)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if menu.is_enabled():
                menu.update(events)
                menu.draw(screen)

            pygame.display.update()
        


    def draw_grid(self, font):
        screen = Singleton.screen
        BLACK = Singleton.BLACK
        left_margin = Singleton.left_margin
        upper_margin = Singleton.upper_margin
        block_size = Singleton.block_size
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for i in range(11):
            pygame.draw.line(screen, BLACK, (left_margin, upper_margin + i * block_size),
                             (left_margin + 10 * block_size, upper_margin + i * block_size), 1)
            pygame.draw.line(screen, BLACK, (left_margin + i * block_size, upper_margin),
                             (left_margin + i * block_size, upper_margin + 10 * block_size), 1)

            pygame.draw.line(screen, BLACK, (
                left_margin + 15 * block_size, upper_margin + i * block_size),
                             (left_margin + 25 * block_size, upper_margin + i * block_size), 1)
            pygame.draw.line(screen, BLACK, (
                left_margin + i * block_size + 15 * block_size, upper_margin),
                             (left_margin + i * block_size + 15 * block_size,
                              upper_margin + 10 * block_size), 1)
            if i < 10:
                num_ver = font.render(str(i + 1), True, BLACK)
                letters_hor = font.render(letters[i], True, BLACK)

                num_ver_widght = num_ver.get_width()
                num_ver_height = num_ver.get_height()
                letters_hor_wight = letters_hor.get_width()
                screen.blit(num_ver, (left_margin - (block_size // 2 + num_ver_widght // 2),
                                      upper_margin + i * block_size + (
                                              block_size // 2 - num_ver_height // 2)))
                screen.blit(num_ver, (left_margin + 15 * block_size - (block_size // 2 + num_ver_widght // 2),
                                      upper_margin + i * block_size + (
                                              block_size // 2 - num_ver_height // 2)))
                screen.blit(letters_hor, (left_margin + i * block_size + (
                        block_size // 2 - letters_hor_wight // 2),
                                          upper_margin + 10 * block_size))
                screen.blit(letters_hor, (
                    left_margin + 15 * block_size + i * block_size + (
                            block_size // 2 - letters_hor_wight // 2),
                    upper_margin + 10 * block_size))

    def sign_grids(self):
        screen = Singleton.screen
        BLACK = Singleton.BLACK
        left_margin = Singleton.left_margin
        upper_margin = Singleton.upper_margin
        block_size = Singleton.block_size
        font_size = int(block_size / 1.5)
        font = pygame.font.SysFont('notosans', font_size)
        player1 = font.render("Gerald", True, BLACK)
        player2 = font.render(Singleton.USER_NAME.get_value(), True, BLACK)
        sign1_width = player1.get_width()
        sign2_width = player2.get_width()
        screen.blit(player1, (left_margin + 5 * block_size - sign1_width //
                              2, upper_margin - block_size // 2 - font_size))
        screen.blit(player2, (left_margin + 20 * block_size - sign2_width //
                              2, upper_margin - block_size // 2 - font_size))
