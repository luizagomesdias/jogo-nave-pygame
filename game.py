import pygame
import random


class Recs(object):
    def __init__(self, numero_inicial):
        self.lista = []
        for x in range(numero_inicial):
            left_random = random.randrange (2, 560)
            top_random = random.randrange (-580, -10)
            width = random.randrange (10, 30)
            height = random.randrange (15, 30)
            self.lista.append(pygame.Rect(left_random, top_random, width, height))

    def mover(self):
        for retangulo in self.lista:
            retangulo.move_ip(0, 2)

    def cor(self, superficie):
        for retangulo in self.lista:
            pygame.draw.rect(superficie, (165, 214, 254), retangulo)

    def recriar(self):
        for x in range(len(self.lista)):
            if self.lista[x].top > 480:
                left_random = random.randrange (2, 560)
                top_random = random.randrange (-580, -10)
                width = random.randrange (10, 30)
                height = random.randrange (15, 30)
                self.lista[x] = (pygame.Rect(left_random, top_random, width, height))


class Player(pygame.sprite.Sprite):
    def __init__(self, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        self.rect.top, self.rect.left = (100, 200)

    def mover(self, vx, vy):
        self.rect.move_ip(vx, vy)

    def update(self, superficie):
        superficie.blit(self.imagem, self.rect)


def colisao(player, recs):
    for rec in recs.lista:
        if player.rect.colliderect(rec):
            return True
    return False


def main():
    import pygame
    pygame.init()
    tela = pygame.display.set_mode((480, 300))
    sair = False
    relogio = pygame.time.Clock()

    img_nave = pygame.image.load('imagens/nave.png') .convert_alpha()
    img_nave = pygame.transform.scale(img_nave, (50, 50))
    jogador = Player(img_nave)

    img_fundo = pygame.image.load('imagens/fundo.png') .convert_alpha()
    img_fundo = pygame.transform.scale(img_fundo, (700, 350))

    img_explosao = pygame.image.load('imagens/explosao.png') .convert_alpha()
    img_explosao = pygame.transform.scale(img_explosao, (50, 50))

    # Colocar música no jogo
    pygame.mixer.music.load("sons/game.mp3")
    # Chamar a música
    pygame.mixer.music.play(3)

    som_explosao = pygame.mixer.Sound("sons/explosao.wav")
    
    som_movimento = pygame.mixer.Sound("sons/movimento.wav")

    vx, vy = 0, 0
    velocidade = 10
    leftpress, rightpress, uppress, downpress = False, False, False, False

    texto = pygame.font.SysFont("Arial", 15, True, False)


    Ret = Recs(30)
    colidiu = False

    while sair != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True
        
            if colidiu == False:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        leftpress = True
                        vx = - velocidade

                    if event.key == pygame.K_RIGHT:
                        rightpress = True
                        vx = velocidade

                    if event.key == pygame.K_UP:
                        uppress = True
                        vy = - velocidade
                        som_movimento.play()

                    if event.key == pygame.K_DOWN:
                        downpress = True
                        vy = velocidade

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        leftpress = False
                        if rightpress: vx = velocidade
                        else: vx = 0

                    if event.key == pygame.K_RIGHT:
                        rightpress = False
                        if leftpress: vx = - velocidade
                        else: vx = 0

                    if event.key == pygame.K_UP:
                        uppress = False
                        if downpress: vy = velocidade
                        else: vy = 0

                    if event.key == pygame.K_DOWN:
                        downpress = False
                        if uppress: vy = - velocidade
                        else: vy = 0
    
        if colisao(jogador, Ret):
            colidiu = True
            jogador.imagem = img_explosao
            pygame.mixer.music.stop()
            som_explosao.play()
        
        if colidiu == False:
            Ret.mover()
            jogador.mover(vx, vy)
            tela.blit(img_fundo, (-40, -10))
            segundos = pygame.time.get_ticks()/1000
            segundos = str(segundos)
            contador = texto.render("Pontuação:{}".format (segundos), 0, (255, 255, 255))
            tela.blit(contador, (350, 10))

        relogio.tick(30)
        #Preenchimento para a tela
        #tela.fill((200, 200, 200))
        #Para colocar o fundo na tela 
        #tela.blit(img_fundo, (-40, -10))
        #Ret.mover()
        Ret.cor(tela)
        Ret.recriar()
        jogador.update(tela)
        #jogador.mover(vx, vy)

        pygame.display.update()

    pygame.quit()
main()
