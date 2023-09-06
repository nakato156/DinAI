import pygame
import random 
from pathlib import Path
from decision_gen import Gen
from decision_bin import Clasif

pygame.init()

path_assets = Path('./assets')
img_player = path_assets / 'player.png'
img_rose = path_assets / 'rose.png'

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
VELOCIDAD = 16
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Juego para entrenamiento de IA")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(img_player).convert()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = 330 - self.rect.height
        self.jump = 10
        self.y = self.jump
           
class Obstaculos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(img_rose).convert()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH,SCREEN_WIDTH+600)
        self.rect.y = 330 - self.rect.height
        self.speed = VELOCIDAD
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.left < -self.rect.height-5:
            pos_x = random.randrange(SCREEN_WIDTH,SCREEN_WIDTH+(random.randrange(1,600)))
            self.rect.x = pos_x + abs(self.rect.x*random.randrange(pos_x//10))
               
all_sprites = pygame.sprite.Group()
obstaculos_sprite = pygame.sprite.Group()

player = Player()

all_sprites.add(player)

for i in range(4):
    obj = Obstaculos()
    all_sprites.add(obj)
    obstaculos_sprite.add(obj)

def main(nowPlayer=None, mode=None, algorithm="clasifier"):
    score = 0
    isJump = False
    run = True
    if not mode or mode!="normal":
        alg_clasify = algorithm =="clasifier"
        if not alg_clasify:
            now_player = nowPlayer if nowPlayer else Gen(VELOCIDAD)
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event == pygame.QUIT:
                run = False
        
        for obj in obstaculos_sprite:
            salto = 0
            # #obteniendo distancia
            obstaculo = obj.rect
            if mode != "normal":
                dist = obstaculo.x- (player.rect.x+player.rect.width)
                if alg_clasify: #utiliza algoritmo de clasificacion
                    salto = Clasif.play(dist)
                elif not alg_clasify: #utiliza algoritmo genetico
                    salto = now_player.play(dist)
                if salto:
                    isJump = True

            #score
            if obstaculo.x in range(player.rect.x-24,player.rect.x):
                score +=1
                print(f"your score: {score}")
        
        # saltos
        keystate = pygame.key.get_pressed()
        if mode and keystate[pygame.K_UP]:
            isJump=True
        if isJump:
            if player.jump >= -10:
                player.rect.y -= (player.jump*abs(player.jump))*0.5
                player.jump -=2
            else:
                player.jump = 10
                isJump = False
            if player.rect.y > 330:
                player.rect.y = 330-player.rect.height

        all_sprites.update()

        # colisiones
        over = pygame.sprite.spritecollide(player,obstaculos_sprite,False)
        if over:
            #el jueno no termina si se utiliza algun algoritmo
            if not mode and alg_clasify:
                score = 0 
                continue
            elif not mode and not alg_clasify: #si el algoritmo es genetico
                run = False #detenemos el ciclo
            return score 

        SCREEN.fill((255,255,255))

        all_sprites.draw(SCREEN)
        pygame.display.flip()
    pygame.quit()

def run_genetico():
    bef_score = None
    generations:list[Gen] = []

    player = Gen(VELOCIDAD)
    generations.append(player)
    generacion = 0

    while True:
        score = main(nowPlayer=player,algorithm="genetic")

        print("-----Actual----")
        print(f"player_gen: {player}")
        print(f"score / fitness: {score}")
        print("------------------")

        bef_score = score if generacion == 0 else bef_score #juego anterior
        player.score = score #juego actual

        if  player.score <= bef_score and generacion > 2:# fit_player < 10: #si el actual es peor que el anterior
            print("----------retrocediendo......")
            print(generations)
            player = generations[-2].mutar()
            bef_score = generations[-3].score
        else:
            if len(generations) < 2: 
                player = Gen(VELOCIDAD)
            else:    
                print("generando hijo")
                player = player.hijo(generations[-2])
            bef_score = score
        generacion +=1
        generations.append(player)

        print("-------status the player------")
        print(f"generacion: {generacion}")
        print(f"fitnes: {player.score}  player: {player}")

def runner(mode=None, alg="clasifier"):
    if not mode and alg == "genetic":
        run_genetico()
    elif mode == "normal" or alg == "clasifier":
        main(mode=mode, algorithm=alg)
    else: 
        print("intoduzca un algoritmo valido")

runner(alg="genetic")