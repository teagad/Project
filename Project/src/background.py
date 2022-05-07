import pygame


class Background(pygame.sprite.Sprite):
    """Создан для фотографии на заднем фоне
        1)Имеет параметры
        image(pygame.Surface),rect(pygame.Rect)
    """

    def __init__(self, image_file, location):
        """
        аргументы При создании:
            image_file(str): Ссылка на фотку заднего фона
            location(list): Координаты куда поставить
        Параметры:
        """
        image_coords = (1240, 650)
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, image_coords)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
