import pygame
import sys
from ball import Ball
from random import randint

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)

pygame.mixer.music.load('sounds/bird.wav')  # фоновая музыка
pygame.mixer.music.play(-1)

s_catch = pygame.mixer.Sound('sounds/catch.wav')  # звук ловли шариков

BLACK = (0, 0, 0)
W, H = 950, 450

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Balls in basket")
pygame.display.set_icon(pygame.image.load("basket-icon.png"))

FPS = 60
clock = pygame.time.Clock()

""" Создадим счетчик очков """
score = pygame.image.load('images/score_fon.png').convert_alpha()
score.set_alpha(150)
f = pygame.font.Font('fonts/praetorianexpandital.ttf', 24)

""" Создаем тележку
    Импортируем картинку / указываем начальные координаты / скорость """

telega = pygame.image.load('images/telega.png').convert_alpha()
t_rect = telega.get_rect(centerx=W//2, bottom=H-15)
t_speed = 10

""" Создадим коллекцию словарей
    содержит: путь к файлу и число очков за каждый шарик"""
balls_data = ({'path': 'ball_bear.png', 'score': 100},
              {'path': 'ball_fox.png', 'score': 150},
              {'path': 'ball_panda.png', 'score': 200})
balls_surf = [pygame.image.load('images/' + data['path']).convert_alpha() for data in balls_data]


def createball(group):
    """ Создаем шарики
        рандомный шарик / в рандомном месте по оси Х / с рандомной скоростью"""
    indx = randint(0, len(balls_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)
    return Ball(x, speed, balls_surf[indx], balls_data[indx]['score'], group)


game_score = 0  # защитанные очки


def collideballs():
    """ Отслеживаем ловлю шаров
     будем использовать pygame.Rect.collidepoint(x, y) для контроля столкновения
     проверяем пересекается ли top прямоугольника плоскости t_rect
     c ball.rect.center (центром) нашего шарика"""
    global game_score
    for ball in balls:
        # пересекает ли центр шара наш прямоугольник t_rect
        if t_rect.collidepoint(ball.rect.center):
            s_catch.play()
            game_score += ball.score  # добавляем очки к нашим защитанным
            ball.kill()  # а сам шарик при столкновении удаляем,
                         # иначе он дальше полетит


balls = pygame.sprite.Group()

bg = pygame.image.load('images/fon_sprite.jpg').convert()

createball(balls)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(1)

        elif event.type == pygame.USEREVENT:
            createball(balls)


    """ Движение тележки """
    keys = pygame.key.get_pressed()  # запоминаем кортеж нажатых клавиш
    if keys[pygame.K_LEFT]:
        t_rect.x -= t_speed
        if t_rect.x < 0:
            t_rect.x = 0
    elif keys[pygame.K_RIGHT]:
        t_rect.x += t_speed
        if t_rect.x > W - t_rect.width:
            t_rect.x = W - t_rect.width

    collideballs()

    sc.blit(bg, (-30, 0))

    balls.draw(sc)
    sc.blit(telega, t_rect)

    """ Отображаем очки """
    sc.blit(score, (0, 0))
    sc_text = f.render(str(game_score), True, (255, 0, 75))
    sc.blit(sc_text, (20, 10))

    pygame.display.update()

    clock.tick(FPS)

    balls.update(H)
