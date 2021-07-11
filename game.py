import pygame
import random 
from decision_bin import Clasif
import decision_gen
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Juego para entrenamiento de IA")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../img/player2.png').convert()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = 330-self.rect.height
        self.jump = 10
        self.y = self.jump
           
class Obstaculos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../img/rose.png').convert()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH,SCREEN_WIDTH+600)
        self.rect.y = 330-self.rect.height
        self.speed = 16
    
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

global bef_score
def main(nowPlayer=None,mode=None,algorithm="clasifier"):
    score = 0
    isJump = False
    run = True
    if not mode or mode!="normal":
        alg_clasify = True if algorithm =="clasifier" else False
        if not mode and not alg_clasify:
            global bef_score
            now_player = nowPlayer if nowPlayer else decision_gen.gen()
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
                    salto = 1 if dist-1<=round(now_player,2) <=dist+0.8 else 0 
                if salto==1:
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
            if player.jump>=-10:
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

def runner(mode=None,alg="clasifier"):
    if not mode and alg.lower() == "genetic":
        player = decision_gen.gen()
        generacion = 0
        generations = decision_gen.generations
        while True:
            score = main(nowPlayer=player,algorithm="genetic")

            print("-----Actual----")
            print(f"player_gen:{round(player,2)}")
            print(f"score:{score}")
            print("------------------")

            bef_score = score if generacion == 0 else bef_score #juego anterior
            fit_player = decision_gen.fitnes(score) #juego actual
            print("fitness:",fit_player)
    
            if  fit_player <= bef_score or generacion < 2:# fit_player < 10: #si el actual es peor que el anterior
                if len(generations) < 2: 
                    player = player
                    generations.append([player,score])
                    continue
                else:    
                    print("generando nuevo individuo")
                    player = decision_gen.new_gen(generations[-2],generations[-1])
                    generacion +=1
                    bef_score = score
            else:
                print("----------retrocediendo......")
                player = generations[-2][0]
                bef_score = generations[-3][1]

            print("-------status the player------")
            print(f"generacion: {generacion}")
            print(f"fitnes:{fit_player}  player:{round(player,2)}")

    elif not mode and alg=="clasifier":
        main(algorithm="clasifier")
    elif mode=="normal":
        main(mode="normal")
    else: 
        print("intoduzac un algoritmo valido")
        return

runner(alg="clasifier")