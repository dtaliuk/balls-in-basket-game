import pygame


class Ball(pygame.sprite.Sprite):
    # У нас здесь определен конструктор, в котором есть два параметра:
    # x - местоположение шарика по координате Х
    # filename - ссылка на изображение этого шарика
    def __init__(self, x, speed, surf, score, group):
        # вызываем конструктор базового класса Sprite, чтобы
        # проинициализировать все необходимые переменные
        pygame.sprite.Sprite.__init__(self)
        # Далее добавляем два обязательных свойства:
        # .image - графическое представление спрайта (ссылка на Sprite)
        # .rect  - его размер и местоположение
        self.image = surf
        # Изменение размера изображения
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 8, self.image.get_height() // 8))
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed  # добавим переменную скорости
        self.score = score
        self.add(group)  # добавляем шар в группу

    # ~~~ Создадим метод перемещения нашего шарика ~~~~~~~~~~~~~~~~~~~~~
    # Метод update() входит в базовый класс Sprite
    # (он отвечает за обновление спрайта / изменение координат)
    # И сейчас мы его переопределяем
    def update(self, *args):
        if self.rect.y < args[0] - 20:  # args[0] - высота клиентской области
            self.rect.y += self.speed
        else:  # как только выходит за рамки клиентской области
            # self.rect.y = 0  # его координата Y становится равна 0
            # # и он заново падает сверху
            # ~~~ если мы хотим, чтобы после окончания движения шарик пропадал
            self.kill()