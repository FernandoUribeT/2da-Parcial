from cgitb import text
from re import X
from string import punctuation
import pygame
import os
import random
pygame.init()

#Global constants
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

sonido_saltar = pygame.mixer.Sound("salto.mp3")

sonido_musica = pygame.mixer.Sound("musica.mp3")

CORAZON = pygame.image.load(os.path.join("corazon.png"))
CORAZON.set_colorkey((255,255,255))

CORRER = [pygame.image.load( "correr1.png"),
pygame.image.load( "correr2.png"),
pygame.image.load( "correr3.png"),
pygame.image.load( "correr4.png"),
pygame.image.load( "correr3.png")]

POWERUP = pygame.mixer.Sound("up.mp3")
POWERDOWN = pygame.mixer.Sound("down.mp3")

AGACHAR = pygame.image.load( "agachar1.png")
PAISAJE = pygame.image.load("PAISAJE.png")
BURGUER = pygame.image.load(os.path.join("burguer.png")).convert()
BURGUER.set_colorkey((255,255,255))


SALTAR = pygame.image.load( "correr1.png")

ZANAHORIA = [pygame.image.load(os.path.join( "zanahoria.png")),
pygame.image.load(os.path.join("zanahoria.png")),
pygame.image.load(os.path.join("zanahoria.png"))]

PAPAS = [pygame.image.load(os.path.join( "papas.png")),
pygame.image.load(os.path.join("papas.png")),
pygame.image.load(os.path.join("papas.png"))]

PIZZA = pygame.image.load("pizza.png")

BG = pygame.image.load( "Track.png").convert()
x = 0
pygame.display.set_caption("Food Rush")
icono = pygame.image.load("pizza.jpg").convert()
pygame.display.set_icon(icono)
Fuente=pygame.font.SysFont("Arial",30)
aux = 1
puntuacion= 0


class harold(pygame.sprite.Sprite):
    X_POS = 50
    Y_POS = 468
    SALTAR_VEL = 8.5
    Y_POS_AGACHAR = 500
    
    def __init__(self):
        self.correr_img = CORRER
        self.saltar_img = SALTAR
        self.agachar_img = AGACHAR

        self.harold_correr = True
        self.harold_saltar = False
        self.harold_agachar = False

        self.step_index = 0
        self.SALTAR_vel = self.SALTAR_VEL
        self.image = self.correr_img[4]
        self.harold_rect = self.image.get_rect()
        
        self.harold_rect.x = self.X_POS
        self.harold_rect.y = self.Y_POS
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255,255,255))
        self.shield = 100


    def update(self, userInput):
        
        if self.harold_agachar:
            self.agachar()
        if self.harold_correr:
            self.correr()
        if self.harold_saltar:
            self.saltar()

        if self.step_index >= 25:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.harold_saltar:
            self.harold_agachar = False
            self.harold_correr = False
            self.harold_saltar = True

        elif userInput[pygame.K_DOWN] and not self.harold_saltar:
            self.harold_agachar = True
            self.harold_correr = False
            self.harold_saltar = False
            
        elif not (self.harold_saltar or userInput[pygame.K_DOWN]):
            self.harold_agachar = False
            self.harold_correr = True
            self.harold_saltar = False
            

    def agachar(self):
        self.image = self.agachar_img
        self.harold_rect = self.image.get_rect()
        self.harold_rect.x = self.X_POS
        self.harold_rect.y = self.Y_POS_AGACHAR
        self.step_index += 1  
        self.image.set_colorkey((255,255,255))   

    def correr(self):
        self.image = self.correr_img[self.step_index // 5]
        self.harold_rect = self.image.get_rect()
        self.harold_rect.x = self.X_POS
        self.harold_rect.y = self.Y_POS
        self.step_index += 1
        self.image.set_colorkey((255,255,255))
   

    def saltar(self):
        self.image = self.saltar_img
        if self.harold_saltar:
            self.harold_rect.y -= self.SALTAR_vel * 4
            self.SALTAR_vel -= 0.8
        if self.SALTAR_vel < - self.SALTAR_VEL:
            self.harold_saltar = False
            self.SALTAR_vel = self.SALTAR_VEL
            self.image.set_colorkey((255,255,255))

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.harold_rect.x, self.harold_rect.y))
        self.image.set_colorkey((255,255,255))
     
class Obstaculos(pygame.sprite.Sprite):
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(100, 200)
        self.rect.y = random.randint(400, 495)
        

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            paps.empty()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class ComidaSaludable(pygame.sprite.Sprite):
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(300, 800)
        self.rect.y = random.randint(400, 495)

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            carrots.empty()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)



class Papas(Obstaculos):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = random.randint(400, 495)
        
        
class Zanahoria(ComidaSaludable):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = random.randint(400, 495)
        

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

    
def draw_health_bar(surface, x, y, porcentaje):
    BAR_LENGHT = 200
    BAR_HEIGHT = 30
    fill = (porcentaje / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, (20,200,20),fill)
    pygame.draw.rect(surface, (255,255,255), border, 2)


def main():
    global game_speed, reloj, obstaculos, comidasaludables, carrots, paps
    run = True
    clock = pygame.time.Clock()
    player = harold()
    obstaculos = []
    comidasaludables = []
    carrots = pygame.sprite.Group()
    paps = pygame.sprite.Group()
    game_speed = 14
    x = 0
    reloj = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    death_count = 0
    sonido_musica.play()
    puntuacion= 0

    def score():
        global reloj, game_speed
        reloj += 1
        if reloj % 1000 == 0:
            game_speed += 1

        text = font.render("Time: " + str(reloj), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1200, 60)
        SCREEN.blit(text, textRect)

    

    Rojo = (255,50,50)
    Verde = (50,255,50)

    fuente = pygame.font.Font(None,25)
    texto = fuente.render("",0,(200,20,20))
    barra_roja = pygame.Rect(50,60,200,30)
    barra_verde = pygame.Rect(50,60,200,30)



    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                 sonido_saltar.play()
                 SALTAR=True

        
        userInput = pygame.key.get_pressed()

        x_relativa = x % BG.get_rect().width
        SCREEN.blit(BG,(x_relativa - BG.get_rect().width,0))
        if x_relativa < SCREEN_WIDTH:
            SCREEN.blit(BG,(x_relativa,0)) 
        x -= 10
        SCREEN.blit(CORAZON, (20,20)) 
        SCREEN.blit(texto,(110,40))
        draw_text(SCREEN, str(puntuacion), 25, 800, 55 )
        draw_text(SCREEN, "Recolecta 15 zanahorias: ", 25, SCREEN_WIDTH // 2, 55 )
        draw_health_bar(SCREEN, 100, 50, player.shield)
        player.draw(SCREEN)  
        player.update(userInput)
        
        if len(paps) == 0:
            if random.randint(0, 2) == 0:
                paps.add(Papas(PAPAS))
               
        if paps:
            for pap in paps:
                pap.draw(SCREEN)
                pap.update()
                if player.harold_rect.colliderect(pap.rect):
                    player.shield -= 25
                    POWERDOWN.play()
                    pap.kill()
                    if player.shield <= 0:
                        menu(death_count == 0)
                

        if len(carrots) == 0:
            if random.randint(0, 2) == 1:
                carrots.add(Zanahoria(ZANAHORIA))
               
        if carrots:
            for carrot in carrots:
                carrot.draw(SCREEN)
                carrot.update()
                if player.harold_rect.colliderect(carrot.rect):
                    puntuacion += 1
                    POWERUP.play()
                    if puntuacion == 15:
                     menu(death_count == 0)
                    if player.shield <= 95:
                        player.shield += 10
                    carrot.kill()
                    
                    
        score()

    
        clock.tick(30)
        pygame.display.update()
    



def menu(death_count):
    global reloj
    run = True
    while run:
        SCREEN.fill((192, 248, 242))
        font = pygame.font.Font('freesansbold.ttf', 30)
        SCREEN.blit(PAISAJE, (0,0))

        if death_count == 0:
            sonido_musica.stop()
            text = font.render("Press any key to start: ", True, (0, 0, 0))
        elif death_count > 0:
            sonido_musica.stop()
            text = font.render("¡Gracias por jugar! ", True, (0, 0, 0))
            score = font.render("Time: " + str(reloj), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(BURGUER, (570, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)