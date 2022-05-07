import pygame
import pygame_menu
from src.background import Background
from src.bot import Bot
from src.player import Player
from src.singleton import Singleton
from time import sleep


class BattleshipsCOMP:

    def __init__(self):
        self.menu()

    def fleet_sunk(self, player):
        for row in player.field.field:
            for element in row:
                if element == "U":
                    return False
        return True

    def to_top(self):
        """Записывать время жизни в top.txt"""
        with open('top.txt', 'a') as f:
            f.write(Singleton.user_name + ":" + str(Singleton.user_points) + "\n")
            f.close()

    def victory_message(self):
        self.to_top()
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

    def check_profile(self):
        if Singleton.user_name.get_value() == "":
            Singleton.user_name = "Joe Biden"
        else:
            Singleton.user_name = Singleton.user_name.get_value()
        print(f"profile: {Singleton.user_name}")

    def print_top(self):
        array = []
        profiles = []
        back_ground = Background('asserts/game_bg.jpg', [0, 0])
        Singleton.screen.blit(back_ground.image, back_ground.rect)
        try:
            with open('top.txt', 'r') as f:
                for lines in f:
                    if lines != "\n":
                        profiles += [lines.split(":")[0]]
                        array += [lines.split(":")[1]]
                array = [*map(int, array)]
                arrays = [(b, a) for b, a in sorted(zip(array, profiles))]
                array, profiles = zip(*arrays)
                my_font = pygame.font.SysFont('Comic Sans MS', 45)
                start = [0, 20]
                step = 40
                count = 1
                for top_elem, profile in zip(array[::-1], profiles[::-1]):
                    text = f"{count} : {profile}-{top_elem} points"
                    text_surface = my_font.render(text, False, (255, 0, 0))
                    Singleton.screen.blit(text_surface, (
                        Singleton.screen.get_rect().width / 2 - text_surface.get_width() / 2, start[1]))
                    start[1] += step
                    count += 1
        except Exception:
            start = [0, 0]
            my_font = pygame.font.SysFont('Comic Sans MS', 45)
            text = "Top is empty"
            text_surface = my_font.render(text, False, (255, 0, 0))
            Singleton.screen.blit(text_surface, start)
        pygame.display.update()
        sleep(5)

    def step_bot(self):
        pygame.init()
        self.check_profile()
        block_size = Singleton.block_size
        left_margin = Singleton.left_margin
        upper_margin = Singleton.upper_margin
        screen = Singleton.screen
        font_size = int(block_size / 1.5)
        font = pygame.font.SysFont('notosans', font_size)
        pygame.display.set_caption("Морской бой")
        back_ground = Background('asserts/game_bg.jpg', [0, 0])
        Singleton.screen.blit(back_ground.image, back_ground.rect)
        pygame.display.update()
        self.draw_grid(font)
        self.sign_grids()
        pygame.display.update()
        c = Bot()
        c.set_compu_fleet()
        p = Player()
        p.set_fleet(Singleton.regime.get_value()[1])
        pygame.display.update()
        font_40 = pygame.font.Font(None, 40)
        score_str = font_40.render('Scores', True, (0, 0, 0))
        _str = score_str.get_width()
        screen.blit(score_str, (left_margin + 26 * block_size - _str //
                            2, upper_margin - 2 * font_size))
        game_over = False
        param = False
        while not game_over:            
            shrift = font_40.render(str(Singleton.user_points), True, (78, 140, 0))
            score = shrift.get_width()
            pygame.draw.rect(screen, (255, 255, 255), (left_margin + 26 * block_size - score //
                              2, upper_margin - font_size, 35, font_size))
            screen.blit(shrift, (left_margin + 26 * block_size - score //
                              2, upper_margin - font_size))

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
        self.menu()

    def menu(self):
        back_ground = Background('asserts/bg_pic.jpg', [0, 0])
        font = pygame_menu.font.FONT_FRANCHISE
        mytheme = pygame_menu.Theme(background_color=(40, 41, 35), title_font_shadow=True, widget_padding=25,
                                    selection_color=(255, 255, 255), widget_font_color=(255, 255, 0), widget_font=font)
        mytheme.set_background_color_opacity(0.6)
        menu = pygame_menu.Menu('', 1240, 650, theme=mytheme)
        Singleton.user_name = menu.add.text_input('NAME :')
        Singleton.regime = menu.add.selector('REGIME : ', [('Fog of War', False), ('Simple', True)])
        menu.add.button('PLAY', self.step_bot)
        menu.add.button('TOP', self.print_top)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        while True:
            Singleton.screen.blit(back_ground.image, back_ground.rect)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if menu.is_enabled():
                menu.update(events)
                menu.draw(Singleton.screen)

            pygame.display.update()

    def draw_grid(self, font):
        screen = Singleton.screen
        black = Singleton.black
        left_margin = Singleton.left_margin
        upper_margin = Singleton.upper_margin
        block_size = Singleton.block_size
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for i in range(11):
            pygame.draw.line(screen, black, (left_margin, upper_margin + i * block_size),
                             (left_margin + 10 * block_size, upper_margin + i * block_size), 1)
            pygame.draw.line(screen, black, (left_margin + i * block_size, upper_margin),
                             (left_margin + i * block_size, upper_margin + 10 * block_size), 1)

            pygame.draw.line(screen, black, (left_margin + 15 * block_size, upper_margin + i * block_size),
                             (left_margin + 25 * block_size, upper_margin + i * block_size), 1)
            pygame.draw.line(screen, black, (left_margin + i * block_size + 15 * block_size, upper_margin),
                             (left_margin + i * block_size + 15 * block_size, upper_margin + 10 * block_size), 1)
            if i < 10:
                num_ver = font.render(str(i + 1), True, black)
                letters_hor = font.render(letters[i], True, black)

                num_ver_widght = num_ver.get_width()
                num_ver_height = num_ver.get_height()
                letters_hor_wight = letters_hor.get_width()
                screen.blit(num_ver, (left_margin - (block_size // 2 + num_ver_widght // 2),
                                      upper_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
                screen.blit(num_ver, (left_margin + 15 * block_size - (block_size // 2 + num_ver_widght // 2),
                                      upper_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
                screen.blit(letters_hor, (left_margin + i * block_size + (block_size // 2 - letters_hor_wight // 2),
                                          upper_margin + 10 * block_size))
                screen.blit(letters_hor, (
                    left_margin + 15 * block_size + i * block_size + (block_size // 2 - letters_hor_wight // 2),
                    upper_margin + 10 * block_size))

    def sign_grids(self):
        screen = Singleton.screen
        black = Singleton.black
        left_margin = Singleton.left_margin
        upper_margin = Singleton.upper_margin
        block_size = Singleton.block_size
        font_size = int(block_size / 1.5)
        font = pygame.font.SysFont('notosans', font_size)
        player1 = font.render("Gerald", True, black)
        player2 = font.render(Singleton.user_name, True, black)
        sign1_width = player1.get_width()
        sign2_width = player2.get_width()
        screen.blit(player1,
                    (left_margin + 5 * block_size - sign1_width // 2, upper_margin - block_size // 2 - font_size))
        screen.blit(player2,
                    (left_margin + 20 * block_size - sign2_width // 2, upper_margin - block_size // 2 - font_size))
