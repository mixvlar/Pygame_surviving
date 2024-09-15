# import pygame
import pygame
pygame.init()

from random import *
# print(pygame.display.Info())

# create a window
W = 1920
H = 1080
sc = pygame.display.set_mode((W,H),pygame.FULLSCREEN)# pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN
# название окна
pygame.display.set_caption('Battledeath')
# иконка окна
pygame.display.set_icon(pygame.image.load('skins/icon.png'))

# colors
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
FUCHSIA = (255, 0, 255)
colors = {(255, 255, 255): 'WHITE', (0, 0, 255): 'BLUE', (255, 0, 0): 'RED', (0, 255, 0): 'GREEN', (0, 0, 0): 'BLACK',
        (255, 255, 0): 'YELLOW', (128, 0, 128): 'PURPLE', (255, 165, 0): 'ORANGE', (255, 192, 203): 'PINK',
          (165, 42, 42): 'BROWN', (128, 128, 128): 'GRAY', (0, 255, 255): 'CYAN', (255, 0, 255): 'FUCHSIA'}



class Player:
    def __init__(self, x, y,speed,see,width,height,color,damage,health,amount_of_bullets):
        self.x = x
        self.y = y
        self.speed = speed
        self.see = see
        self.health = health
        self.width = width
        self.height = height
        self.color = color
        self.skin_color = color
        self.damage = damage
        self.amount_of_bullets = amount_of_bullets
        self.actual_speed = speed
        self.actual_damage = damage
        self.actual_amount_of_bullets = amount_of_bullets


    def draw_player(self):
        # pygame.draw.rect(sc, self.color, (self.x, self.y, self.width, self.height))


        player_surf = pygame.image.load(f'skins/player_{colors[self.color]}.png')
        player_surf = pygame.transform.scale(player_surf, (self.width,self.height))

        player_rect = player_surf.get_rect(topleft=(self.x,self.y))
        sc.blit(player_surf,player_rect)


    def move(self,keys):
        # +- 30 - это серые границы
        if keys[pygame.K_LEFT] and self.x - 30 > 0: self.x -= self.speed;self.see = "l"
        if keys[pygame.K_RIGHT] and self.x < W - self.width - 30: self.x += self.speed;self.see = "r"
        if keys[pygame.K_UP] and self.y > 0 + 30: self.y -= self.speed;self.see="u"
        if keys[pygame.K_DOWN] and self.y < H - self.height - 30: self.y += self.speed;self.see="d"

    def player_collide_with_obstacle(self, opponent):
        global living,defeat,start_button,exit_button
        # player.x,player.y,10,20 killer.x,killer.y,*killer.size
        if pygame.Rect(self.x,self.y,self.width,self.height).colliderect(pygame.Rect(opponent)):

            living = False
            defeat = True
            start_button = Button_start(W // 2 - 500 // 2, H // 2 - 100, 500, 200)
            exit_button = Button_exit(W // 2 - 500 // 2, H // 2 + 150, 500, 200)
            pygame.mouse.set_visible(True)

    def player_collide_with_stick_X(self,stick):
        if pygame.Rect(self.x,self.y,self.width,self.height).colliderect(pygame.Rect(stick.x,stick.y,stick.length,stick.width)) and stick.active==True:
                stick.active = False
                self.health-=1

                self.color = RED
                redding = pygame.USEREVENT + 1
                pygame.time.set_timer(redding, 500)

    def player_collide_with_stick_Y(self,stick):
        if pygame.Rect(self.x,self.y,self.width,self.height).colliderect(pygame.Rect(stick.x,stick.y,stick.width,stick.length)) and stick.active==True:
                stick.active = False
                self.health-=1

                self.color = RED
                redding = pygame.USEREVENT + 1
                pygame.time.set_timer(redding, 500)

    def player_collide_with_bomb(self,bomb):
        if pygame.Rect(self.x,self.y,self.width,self.height).colliderect(pygame.Rect(bomb.x,bomb.y,bomb.width,bomb.length)) and bomb.active==True:
                self.health-=15
                bomb.time = float("inf")




    def player_collide_with_killer(self,x,y,w,h,damage,killer):
        if pygame.Rect(self.x, self.y, self.width, self.height).colliderect(pygame.Rect(x, y, w, h)):
            self.health -= damage
            killer.health = 0

            if killer.typ == 'spiteful':
                    killer.spiteful_effect(self)

            if self.color == self.skin_color:
                self.color = RED

            redding = pygame.USEREVENT + 1
            pygame.time.set_timer(redding, 500)


    def player_health_check(self):
        return self.health>0

    def player_reset_settings(self):
        self.speed = self.actual_speed
        self.amount_of_bullets = self.actual_amount_of_bullets
        self.color = self.skin_color



class Bomb:
    def __init__(self,length,width,x,y):


        self.length = length
        self.width = width
        self.x = x
        self.y = y
        self.active = False
        self.time = 0

    def draw_bomb(self):

            bomb_surf = pygame.image.load(f'skins/bomb_skin.png')
            bomb_surf = pygame.transform.scale(bomb_surf, (self.length, self.width))

            bomb_rect = bomb_surf.get_rect(topleft=(self.x, self.y))
            sc.blit(bomb_surf, bomb_rect)



class Xlines:
    def __init__(self,speed,length,width,vector):

        self.speed = speed
        self.length = length
        self.width = width
        self.vector = vector
        self.active = True
        self.actual_speed = speed
        if self.vector == 1:
            self.x = 0
            self.y = randint(0, H)
        else:
            self.x = W
            self.y = randint(0, H)


    def move_x(self):
        if self.active == True:
            pygame.draw.rect(sc, WHITE, (self.x, self.y,self.length,self.width))
            self.x += self.speed*self.vector

            if self.vector==1:
                if self.x > W+100:
                    self.y = randint(0, H)
                    self.x = 0
            else:
                if self.x < 0:
                    self.y = randint(0, H)
                    self.x = W+100


class Ylines:
    def __init__(self,speed,length,width,vector):

        self.speed = speed
        self.length = length
        self.width = width
        self.vector = vector
        self.active = True
        self.actual_speed = speed
        if self.vector == 1:
            self.x = randint(0, W)
            self.y = 0
        else:
            self.x = randint(0,W)
            self.y = H


    def move_y(self):
        if self.active == True:
            pygame.draw.rect(sc,WHITE,(self.x,self.y,self.width,self.length))
            self.y+=self.speed*self.vector


            if self.vector==1:
                if self.y>H+100:
                    self.x = randint(0,W)
                    self.y = 0
            else:
                if self.y<0:
                    self.x = randint(0,W)
                    self.y = H+100


class Wall:
    def __init__(self,x,y,w,h,speed,rl):
        #rl = 1 from left to right
        #rl = -1 from right to left
        #rl = 2 from up to down
        #rl = -2 down left to up
        self.x = x
        self.y = y
        self.speed = speed
        self.actual_speed = speed
        self.w = w
        self.h = h
        # self.flag = True
        self.rl = rl
        self.active = 0

    def show_walls_coords(self):
        return (self.x,self.y,self.w,self.h)

    def move_wall(self):
        self.active+=1
        if self.active>100:
            if self.rl==1:
                self.x+=self.speed
            elif self.rl==-1:
                self.x-=self.speed
            elif self.rl==2:
                self.y+=self.speed
            elif self.rl==-2:
                self.y-=self.speed

    def draw_wall(self):
        if self.active<=100:
            # предупреждение о стене
            if self.rl==1:
                wall1_surf = pygame.image.load(f'skins/wall_skin.png')
                wall1_surf = pygame.transform.scale(wall1_surf, (self.w,self.h))
                wall1_rect = wall1_surf.get_rect(topleft=(0-50,0))
                sc.blit(wall1_surf, wall1_rect)
                sc.blit(wall1_surf, wall1_rect)
            if self.rl==-1:
                wall1_surf = pygame.image.load(f'skins/wall_skin.png')
                wall1_surf = pygame.transform.scale(wall1_surf, (self.w,self.h))
                wall1_rect = wall1_surf.get_rect(topleft=(W-50, 0))
                sc.blit(wall1_surf, wall1_rect)
                sc.blit(wall1_surf, wall1_rect)
            if self.rl==2:
                wall1_surf = pygame.image.load(f'skins/wall_skin.png')
                wall1_surf = pygame.transform.scale(wall1_surf, (self.w,self.h))
                wall1_rect = wall1_surf.get_rect(topleft=(0,0-30))
                sc.blit(wall1_surf, wall1_rect)
                sc.blit(wall1_surf, wall1_rect)
            if self.rl==-2:
                wall1_surf = pygame.image.load(f'skins/wall_skin.png')
                wall1_surf = pygame.transform.scale(wall1_surf, (self.w,self.h))
                wall1_rect = wall1_surf.get_rect(topleft=(0, H-50))
                sc.blit(wall1_surf, wall1_rect)
                sc.blit(wall1_surf, wall1_rect)

        # if self.flag == True:#self.x >= 0 and
        else:
            wall1_surf = pygame.image.load(f'skins/wall_skin.png')
            wall1_surf = pygame.transform.scale(wall1_surf, (self.w,self.h))
            wall1_rect = wall1_surf.get_rect(topleft=(self.x, self.y))
            sc.blit(wall1_surf, wall1_rect)


class Killer:
    def __init__(self,x,y,color,speed,size:tuple,health,typ):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.size = size
        self.first_health = health
        self.recovering = False
        self.skin_color = color
        self.actual_speed = speed
        self.typ = typ
        self.health = 0

    def define_killer_health(self):
        if self.typ == 'killer':
            self.health = randint(5,10)
        elif self.typ == 'boss':
            self.health = randint(10,20)
        elif self.typ == 'spiteful':
            self.health = randint(2,3)

    def move_killer(self,player_x,player_y):
        if self.health>0:
            if self.x < player_x and self.x < W - self.size[0] - 30:
                self.x += self.speed
            elif self.x > player_x and self.x - 30 > 0:
                self.x -= self.speed
            if self.y < player_y and self.y < H - self.size[1] - 30:
                self.y += self.speed
            elif self.y > player_y and self.y > 0 + 30:
                self.y -= self.speed

    def show_killer(self):
        if self.health>0:
            pygame.draw.rect(sc, self.color, (self.x, self.y,*self.size))

    def draw_killer(self):
        if self.health>0:
            killer_surf = pygame.image.load(f'skins/{self.typ}_skin_{colors[self.color]}.png')
            killer_surf = pygame.transform.scale(killer_surf, self.size)
            killer_rect = killer_surf.get_rect(topleft=(self.x, self.y))
            sc.blit(killer_surf, killer_rect)

    def return_home(self):
        if self.health<=0:
            self.define_killer_health()
            possible_coords = ((0,0),(0,H),(W,0),(W,H))
            self.x,self.y = choice(possible_coords)

    def get_recovery_time(self):
        if self.typ == 'killer':
            return randint(10000,15000)
        elif self.typ == 'boss':
            return randint(10000,20000)
        elif self.typ == 'spiteful':
            return randint(5000,10000)

    def killer_collide_with_bomb(self,bomb):
        if pygame.Rect(self.x,self.y,*self.size).colliderect(pygame.Rect(bomb.x,bomb.y,bomb.width,bomb.length)) and bomb.active==True:
                self.health-=15
                bomb.time = float("inf")

    def killer_health_check_zero(self):
        if self.health>0:
            if self.typ=='spiteful':
                player.player_collide_with_killer(self.x,self.y,*self.size,2,self)
            else:
                player.player_collide_with_killer(self.x,self.y,*self.size,randint(1,5)*self.health,self)
        else:
            if self.typ == 'killer':
                if self.recovering == False:
                    pygame.time.set_timer(pygame.USEREVENT+0,self.get_recovery_time())
                    self.recovering = True
                    self.color = self.skin_color
                    self.speed = self.actual_speed
            elif self.typ == 'boss':
                if self.recovering == False:
                    pygame.time.set_timer(pygame.USEREVENT+10, self.get_recovery_time())
                    self.recovering = True
                    self.color = self.skin_color
                    self.speed = self.actual_speed
            elif self.typ == 'spiteful':
                if self.recovering == False:
                    pygame.time.set_timer(pygame.USEREVENT+11, self.get_recovery_time())
                    self.recovering = True
                    self.color = self.skin_color
                    self.speed = self.actual_speed

    def killer_redding(self):
        self.color = RED
        redding = pygame.USEREVENT+2
        # восстановление killer идет от 5 до 12 секунд
        pygame.time.set_timer(redding, 500)

    def spiteful_effect(self,player):
        effects = ['stunning', 'slowing', 'damage_lowing', 'lowing_amount_of_bullets']
        effect = choice(effects)
        if effect == 'stunning':
            player.speed = 0
            ef = pygame.USEREVENT+7
            pygame.time.set_timer(ef, 1500)
        elif effect == 'slowing':
            if player.speed/4!=0:player.speed/=4
            else:player.speed = 1

            ef = pygame.USEREVENT+7
            pygame.time.set_timer(ef, 2500)
            player.color = BLUE

        elif effect == 'damage_lowing':
            if player.damage/2!=0:player.damage/=2
            else:player.damage = 0.1
            ef = pygame.USEREVENT + 7
            pygame.time.set_timer(ef, 5000)

        elif effect == 'lowing_amount_of_bullets':
            player.amount_of_bullets-=1
            ef = pygame.USEREVENT + 7
            pygame.time.set_timer(ef, 5000)


class Healing:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.flag = False

    def healing_collide_with_player(self,player):
        if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x,player.y,player.width,player.height)):
            player.health += randint(1,3)
            return True

    def draw_healing(self):
        healing_surf = pygame.image.load(f'skins/healing_skin.png')
        healing_surf = pygame.transform.scale(healing_surf, (self.w,self.h))
        healing_rect = healing_surf.get_rect(topleft=(self.x,self.y))
        sc.blit(healing_surf,healing_rect)


class Slowdown_time:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.flag = False

    def slowdown_time_collide_with_player(self,player):
        if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x,player.y,player.width,player.height)):
            player.health += randint(1,3)
            return True

    def draw_slowdown_time(self):
        # pygame.draw.rect(sc,ORANGE,(self.x,self.y,self.w,self.h))
        slow_down_surf = pygame.image.load(f'skins/slow_down_skin.png')
        slow_down_surf = pygame.transform.scale(slow_down_surf, (self.w,self.h))
        slow_down_rect = slow_down_surf.get_rect(topleft=(self.x,self.y))
        sc.blit(slow_down_surf,slow_down_rect)


class Damage_boost:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.flag = False

    def damage_boost_collide_with_player(self,player):
        if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(pygame.Rect(player.x,player.y,player.width,player.height)):
            return True

    def draw_damage_boost(self):
        # pygame.draw.rect(sc,FUCHSIA,(self.x,self.y,self.w,self.h))
        damage_boost_surf = pygame.image.load(f'skins/damage_boost_skin.png')
        damage_boost_surf = pygame.transform.scale(damage_boost_surf, (self.w,self.h))
        damage_boost_rect = damage_boost_surf.get_rect(topleft=(self.x,self.y))
        sc.blit(damage_boost_surf,damage_boost_rect)


class Button_exit:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw_exit_button(self):
        btn_surf = pygame.image.load(f'skins/exit.png')
        btn_surf = pygame.transform.scale(btn_surf, (self.w,self.h))
        btn_rect = btn_surf.get_rect(topleft=(self.x,self.y))
        sc.blit(btn_surf,btn_rect)

    def click_exit_button(self,event):
        global flRunning
        if self.x <= event.pos[0] <= self.x+self.w and self.y <= event.pos[1] <= self.y+self.h:
            flRunning=False


class Button_start:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw_start_button(self):
        btn_surf = pygame.image.load(f'skins/start.png')
        btn_surf = pygame.transform.scale(btn_surf, (self.w,self.h))
        btn_rect = btn_surf.get_rect(topleft=(self.x,self.y))
        sc.blit(btn_surf,btn_rect)

    def click_start_button(self,event):
        global living,alive,player,killer,boss,spiteful,heal,slowdown,damage_boost,new_sticks,sticks_x,sticks_y,walls,pule,pule_show,bombs,new_bomb,records_update
        if self.x <= event.pos[0] <= self.x+self.w and self.y <= event.pos[1] <= self.y+self.h:
            living = True
            # print(event.pos)
            self.x+=100000
            alive = 0
            player = Player(W // 2, H // 2, 5, 'r', W // (50 * 2 * 1.25), W // (50 * 1.25), YELLOW, 1, 15, 2)
            player.player_reset_settings()
            killer = Killer(0, 0, PURPLE, 1, (W // 40, W // 40), 5, 'killer')
            killer.define_killer_health()
            killer.return_home()
            killer.x-=100
            boss = Killer(0, 0, PURPLE, 0.5, (W // 20, W // 20), 15, 'boss')
            boss.define_killer_health()
            boss.return_home()
            boss.x-=100
            spiteful = Killer(0, 0, PURPLE, 3, (W // 66, W // 66), 5, 'spiteful')
            spiteful.define_killer_health()
            spiteful.return_home()
            spiteful.x-=100
            heal = 0
            slowdown = 0
            damage_boost = 0
            new_sticks = 0
            new_bomb = 2500
            bombs = []
            sticks_x = []
            sticks_y = []
            walls = []
            pule = []
            pule_show = []
            records_update = False
            pygame.mouse.set_visible(False)


class Button_learning:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw_learning_button(self):
        btn_surf = pygame.image.load(f'skins/learning.png')
        btn_surf = pygame.transform.scale(btn_surf, (self.w,self.h))
        btn_rect = btn_surf.get_rect(topleft=(self.x,self.y))
        sc.blit(btn_surf,btn_rect)

    def click_learning_button(self,event):
        global learning_button,start_button,exit_button
        if self.x <= event.pos[0] <= self.x + self.w and self.y <= event.pos[1] <= self.y + self.h:
            sc.fill(BLACK)
            start_button = Button_start(W // 2 - 500 // 2+700, H // 2 + 50, 500, 200)
            exit_button = Button_exit(W // 2 - 500 // 2+700, H // 2 - 200 // 2 + 400, 500, 200)
            learning_button.x+=10000
            killer.x+=10
            killer.y+=10
            killer.draw_killer()
            draw_text('Name: Killer Health: 5-10 Damage: 1-50',YELLOW,50,70,10)
            killer.x-=10
            killer.y-=10
            boss.x+=10
            boss.y+=70
            boss.draw_killer()
            draw_text('Name: Boss Health: 10-20 Damage: 1-100',YELLOW,50,120,120)
            boss.x-=10
            boss.y-=70
            spiteful.x+=10
            spiteful.y+=215
            spiteful.draw_killer()
            draw_text('Name: Spiteful Health: 2-3 Damage: 2 + negative effect',YELLOW,50,50,200)
            spiteful.x-=10
            spiteful.y-=215
            pygame.draw.rect(sc, WHITE, (10, H//266+285,30,6))
            draw_text('Name: Stick Speed: 1-5 Damage: 1',YELLOW,50,50,270)
            wall1_surf = pygame.image.load(f'skins/wall_skin.png')
            wall1_surf = pygame.transform.scale(wall1_surf, (75, 50))
            wall1_rect = wall1_surf.get_rect(topleft=(10, 330))
            sc.blit(wall1_surf, wall1_rect)
            draw_text('Name: Wall Damage: infinite',YELLOW,50,90,340)

class Bullet:
    time_to_recharge = 75
    def __init__(self,x,y,w,h,vector,color,distance_gone,active,speed,distance_gone_to_disappear):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vector = vector
        self.color = color
        self.distance_gone = distance_gone
        self.active = active
        self.speed = speed
        self.distance_gone_to_disappear = distance_gone_to_disappear
        self.to_recharge = 0

    def bullet_collide_something(self,killer):
        if pygame.Rect(self.x,self.y,self.w,self.h).colliderect(pygame.Rect(killer)):
            return True

    def draw_bullet(self):
        if self.active == True:
            pygame.draw.rect(sc, self.color, (self.x, self.y, self.w, self.h))


def draw_text(msg,color,size,x=0,y=0):
    text = pygame.font.Font('freesansbold.ttf', size).render(msg, True, color)
    text_rect = text.get_rect()
    text_rect.x = x
    text_rect.y = y
    sc.blit(text, text_rect)


def update_records(new_possible_record):
    counts = [x.strip() for x in open('records.txt')]

    counts.append(f"{new_possible_record / 60:.{3}f}")
    counts = [float(x) for x in counts]
    counts.sort(reverse=True)
    counts.pop(-1)

    with open('records.txt', 'w') as f:
        for i in range(len(counts)): f.write(f'{counts[i]}\n')


# создание игрока
player = Player(W // 2, H // 2, 5, 'r',W//(50*2*1.25),W//(50*1.25),YELLOW,1,15,2)

sticks_x = []
bombs = []
# первое и последующие появления новой бомбы
new_bomb = 2500
sticks_y = []
new_sticks = 0
alive = 0
living = False
defeat = False
# items
heal = 0
slowdown = 0
damage_boost = 0
start_button = Button_start(W//2-500//2,H//2-300,500,200)
learning_button = Button_learning(W//2-500//2,H//2-50,500,200)
exit_button = Button_exit(W//2-500//2,H//2-200//2+300,500,200)
# выстрелы
pule = []
# переворачиваем экран, чтобы было видно нарисованное на обратной стороне
pygame.display.update() # вместо update() можно использовать flip(), но первый более гибкий
# выполняем все события
flRunning = True
# Если установить одну и ту же задержку на разных устройствах, будет нечестно, так как время обработки событий у всех
# разное, поэтому создадим штуку, которая сама определяет задержку
clock = pygame.time.Clock()
FPS = 60
# цвет заднего фона
bg_ground = BLACK
walls = []
# создаем киллера
killer = Killer(0,0,PURPLE,1,(W//40,W//40),5,'killer')
boss = Killer(0,0,PURPLE,0.5,(W//20,W//20),15,'boss')
spiteful = Killer(0,0,PURPLE,3,(W//66,W//66),5,'spiteful')
spiteful.define_killer_health()
killer.define_killer_health()
boss.define_killer_health()
# невидимая мышь
pygame.mouse.set_visible(True)
records_update = False



while flRunning:
    # print('Working!')
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exit
            # pygame.quit()
            # flRunning = False
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_button.click_start_button(event)
            learning_button.click_learning_button(event)
            exit_button.click_exit_button(event)

        if living == True:
            if event.type == pygame.USEREVENT and killer.health<=0:
                killer.health = 0
                killer.return_home()
                killer.recovering = False

            elif event.type == pygame.USEREVENT+10 and boss.health<=0:
                boss.return_home()
                boss.recovering = False

            elif event.type == pygame.USEREVENT+11 and spiteful.health<=0:
                spiteful.health = 0
                spiteful.return_home()
                spiteful.recovering = False

            elif event.type == pygame.USEREVENT+1:
                if player.color == RED:
                    player.color = player.skin_color

            elif event.type == pygame.USEREVENT+2:
                killer.color = killer.skin_color
                boss.color = boss.skin_color
                spiteful.color = spiteful.skin_color

            elif event.type == pygame.USEREVENT+3:
                if heal!=0:
                    heal.flag = True

            elif event.type == pygame.USEREVENT+4:
                if killer.actual_speed>killer.speed:killer.speed*=2
                if boss.actual_speed > boss.speed: boss.speed *= 2
                if spiteful.actual_speed > spiteful.speed: spiteful.speed *= 2
                for wall in walls:
                    if wall.actual_speed>wall.speed:wall.speed*=2
                for s in sticks_x:
                    if s.actual_speed>s.speed:s.speed*=2
                for s in sticks_y:
                    if s.actual_speed>s.speed:s.speed*=2

            elif event.type == pygame.USEREVENT+5:
                if slowdown!=0:
                    slowdown.flag = True

            elif event.type == pygame.USEREVENT+7:
                player.speed = player.actual_speed
                player.color = player.skin_color
                player.damage = player.actual_damage
                player.amount_of_bullets = player.actual_amount_of_bullets


            elif event.type == pygame.USEREVENT+8:
                if damage_boost!=0:
                    damage_boost.flag = True

            elif event.type == pygame.USEREVENT + 9:
                player.damage = player.actual_damage
                player.amount_of_bullets = player.actual_amount_of_bullets


            if event.type == pygame.KEYDOWN:
                # добавление выстрела в список, первым элементом идет направление пули, игрок не может выпустить пулю, пока
                # на экране присутствует энное количество пуль
                if event.key == pygame.K_f and len([1 for x in pule if x.to_recharge<x.time_to_recharge])<player.amount_of_bullets:
                    pule.append(Bullet(player.x,player.y,5,5,player.see,GREEN,0,True,15,3000))


    if living == True:

        # управление игроком
        keys = pygame.key.get_pressed()
        player.move(keys)

        # делаем заливку
        sc.fill(bg_ground)
        # рисуем игрока
        player.draw_player()


        for bul in pule:
            # перезарядка
            bul.to_recharge+=1
            # если пуля за экраном
            if bul.distance_gone>bul.distance_gone_to_disappear:
                pule.remove(bul)

            else:
                # рисуем, исключая направление пули
                bul.draw_bullet()

            #%-tab
        # меняем координаты
            if bul.vector=="r":
                # изменяем координаты пули на ее скорость
                bul.x+=bul.speed
                bul.distance_gone+=bul.speed


            elif bul.vector=="l":
                bul.x-=bul.speed
                bul.distance_gone += bul.speed

            elif bul.vector=="u":
                bul.y-=bul.speed
                bul.distance_gone += bul.speed


            elif bul.vector=="d":
                bul.y+=bul.speed
                bul.distance_gone += bul.speed


            # damaging killer
            if bul.active == True:
                # wall shot
                if walls!=[]:
                    for wall in walls:
                        if bul.bullet_collide_something(wall.show_walls_coords()) or bul.bullet_collide_something(wall.show_walls_coords()):
                            bul.active = False

                # killer shot
                if bul.bullet_collide_something((killer.x, killer.y, *killer.size)) and killer.health>0:
                    killer.killer_redding()
                    if killer.health-player.damage>=0:killer.health -= player.damage
                    else:killer.health = 0
                    bul.active = False


                # boss shot
                if bul.bullet_collide_something((boss.x, boss.y, *boss.size)) and boss.health>0:
                    boss.killer_redding()
                    if boss.health - player.damage >= 0:boss.health -= player.damage
                    else:boss.health = 0
                    bul.active = False

                # spiteful shot
                if bul.bullet_collide_something((spiteful.x, spiteful.y, *spiteful.size)) and spiteful.health>0:
                    spiteful.killer_redding()
                    if spiteful.health - player.damage >= 0:spiteful.health -= player.damage
                    else:spiteful.health = 0
                    bul.active = False

        # коллизия с killer
        killer.killer_health_check_zero()
        # коллизия с boss
        boss.killer_health_check_zero()
        # коллизия с spiteful
        spiteful.killer_health_check_zero()

        # летящие палки
        for stick in sticks_x:
            if stick.active == True:
                stick.move_x()
                player.player_collide_with_stick_X(stick)
            else:
                sticks_x.remove(stick)

        # добавляем бомбам время
        for b in bombs:
            b.time += 1
            b.draw_bomb()

            if 100<b.time<=500:
                b.active = True
                killer.killer_collide_with_bomb(b)
                boss.killer_collide_with_bomb(b)
                spiteful.killer_collide_with_bomb(b)
                player.player_collide_with_bomb(b)

            elif b.time>500:
                bombs.remove(b)

        # падающие палки
        for stick in sticks_y:
            if stick.active == True:
                stick.move_y()
                player.player_collide_with_stick_Y(stick)
            else:
                sticks_y.remove(stick)

        # flappy wall
        # Добавляем стену, если на экране нет стен, и игрок живет больше 15 секунд
        if alive/60>15 and len(walls)+2<=2 and randint(1,250)==10:

            rl_now = []
            for wall in walls:
                rl_now += [wall.rl]


            rl = choice([1,-1,2,-2])
            if rl in [1,-1]:
                height_of_wall = randint(30,700)
                speed_of_wall = randint(2,3)

                ex2 = height_of_wall+randint(200,400) # ширина прохода между стенами

                if rl==1 and 1 not in rl_now:
                    walls+=[Wall(0-100, 0, 100, height_of_wall,speed_of_wall, rl)]
                    walls+=[Wall(0-100, ex2, 100, H,speed_of_wall, rl)]

                elif rl==-1 and -1 not in rl_now:
                    walls+=[Wall(W, 0, 100, height_of_wall,speed_of_wall, rl)]
                    walls+=[Wall(W, ex2, 100, H,speed_of_wall, rl)]

            elif rl in [2,-2]:

                width_of_wall = randint(30, W-400)
                speed_of_wall = randint(1,2)

                ex2 = randint(400, 600)  # ширина прохода между стенами

                if rl == 2 and 2 not in rl_now:
                    walls += [Wall(0, 0-75, width_of_wall, 75, speed_of_wall, rl)]
                    walls += [Wall(width_of_wall+ex2, 0-75, W, 75, speed_of_wall, rl)]

                elif rl == -2 and -2 not in rl_now:
                    walls += [Wall(0, H, width_of_wall, 75, speed_of_wall, rl)]
                    walls += [Wall(width_of_wall+ex2, H, W, 75, speed_of_wall, rl)]

        # рисуем стены
        for wall in walls:

            wall.move_wall()
            wall.draw_wall()
            player.player_collide_with_obstacle((wall.show_walls_coords()))
            # if wall.flag == False:wall = 0
            if wall.rl==1 and wall.x>W+wall.w:
                walls.remove(wall)
            elif wall.rl == -1 and wall.x+wall.w<0:
                walls.remove(wall)
            elif wall.rl == 2 and wall.y>H:
                walls.remove(wall)
            elif wall.rl == -2 and wall.y+wall.h<0:
                walls.remove(wall)


        # если игрок жив уже 30 секунд
        if alive/60>30:
            # killer
            killer.move_killer(player.x,player.y)
            # killer.show_killer()
            killer.draw_killer()

        # boss появлеется после 90 секунд
        if alive/60>90:
            # boss
            boss.move_killer(player.x,player.y)
            # boss.show_killer()
            boss.draw_killer()
        # spiteful появлеется после 150 секунд
        if alive/60>150:
            # spiteful
            spiteful.move_killer(player.x,player.y)
            # spiteful.show_killer()
            spiteful.draw_killer()


        # аптечка появлеется каждые 7-10 секунд после 40 секунд
        if alive/60>40 and heal == 0:
            heal = Healing(randint(50,950),randint(50,750),W//66,W//66)
            hh = pygame.USEREVENT+3
            pygame.time.set_timer(hh, randint(7000,10000))

        if heal!=0 and heal.flag==True:
            heal.draw_healing()
            if heal.healing_collide_with_player(player):
                heal = 0


        #  появлеется каждые 8-12 секунд после 65 секунд
        if alive/60>65 and slowdown == 0:
            slowdown = Slowdown_time(randint(50,950),randint(50,750),W//66,W//66)
            sl = pygame.USEREVENT+5
            pygame.time.set_timer(sl, randint(8000,12000))


        if slowdown!=0 and slowdown.flag==True:

            slowdown.draw_slowdown_time()

            if slowdown.slowdown_time_collide_with_player(player):

                sl_end = pygame.USEREVENT+4
                pygame.time.set_timer(sl_end, 3000)

                # скорость всех существ уменьшается вдвое
                killer.speed/=2
                boss.speed/=2
                spiteful.speed/=2
                for wall in walls:
                    wall.speed/=2

                for s in sticks_x:s.speed/=2
                for s in sticks_y:s.speed/=2
                slowdown = 0

        # damage_boost появлеется каждые 5-15 секунд после 100 секунд
        if alive/60>100 and damage_boost == 0:
            damage_boost = Damage_boost(randint(50,950),randint(50,750),W//66,W//66)
            sl = pygame.USEREVENT+8
            pygame.time.set_timer(sl, randint(5000,15000))


        if damage_boost!=0 and damage_boost.flag==True:

            damage_boost.draw_damage_boost()

            if damage_boost.damage_boost_collide_with_player(player):
                sl_end = pygame.USEREVENT+9
                pygame.time.set_timer(sl_end, 5000)
                player.damage *= 1.5
                player.amount_of_bullets+=1
                damage_boost = 0


        if alive>new_bomb:
            bombs+=[Bomb(25,25,randint(50,W-30),randint(50,H-30))]
            new_bomb = alive + 60 * 5

        if alive>new_sticks:
            xch = choice([-1,1])
            ych = choice([-1,1])
            if xch == 1:sticks_x+=[Xlines(randint(1,5),W//66,H//266,xch)]
            else:sticks_x += [Xlines(randint(1,5), W//66,H//266, xch)]
            if ych == 1:sticks_y+=[Ylines(randint(1,5),W//66,H//266,ych)]
            else:sticks_y+=[Ylines(randint(1,5),W//66,H//266,ych)]

            # каждые 5 секунд появляются летящая и падающая палки
            new_sticks = alive + 60*5



        # границы
        pygame.draw.rect(sc,GRAY,(0,0,W,H),30)



        # сколько выстрелов сделал игрок
        draw_text(f"Health: {'%.2f'%player.health}    Damage: {player.damage}    Bullets: {player.amount_of_bullets-len([1 for x in pule if x.to_recharge<x.time_to_recharge])}\
            Speed: {'%.2f'%player.speed}",YELLOW,25,10,3)
        draw_text(f"Killer's health: {killer.health}    Boss health: {boss.health}    Spiteful health: {spiteful.health}",YELLOW,25,10,H-28)

        # сколько времени игрок жив
        draw_text(f"Alive: {alive/60:.{3}f}",YELLOW,25,H,5)
        alive+=1



        if not(player.player_health_check()):
            living = False
            pygame.mouse.set_visible(True)
            defeat = True
            start_button = Button_start(W // 2 - 500 // 2, H // 2 - 100, 500, 200)
            exit_button = Button_exit(W // 2 - 500 // 2, H // 2 + 150, 500, 200)

    elif defeat == False:
        start_button.draw_start_button()
        learning_button.draw_learning_button()
        exit_button.draw_exit_button()


    else:
        sc.fill(bg_ground)
        if records_update == False:
            update_records(alive)
            records_update = True

        counts = [x.strip() for x in open('records.txt')]
        for i in range(len(counts)):draw_text(f"{i+1}) {counts[i]}",YELLOW,50,10,5+i*50)

        draw_text(f"GAME OVER!",YELLOW,100,W//2-300,200)
        draw_text(f"Alive: {alive / 60:.{3}f}",YELLOW,100,W//2-300,300)
        start_button.draw_start_button()
        exit_button.draw_exit_button()

    pygame.display.update()

    # Наш цикл прокручивается слишком быстро, нам этого не надо, поэтому нужно установить задержку
    # pygame.time.delay(20) # задержка на 20 миллисекунд
    clock.tick(FPS) # 60 итераций за секунду