import pygame
from network import ClientNetwork
from keezen_bot import keezen_bot


def open_display():
    width = 500
    height = 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Client")


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main(server_IP):
    n = ClientNetwork(server_IP)
    all_pawns_of_current_player_are_in_finish = False
    while not all_pawns_of_current_player_are_in_finish:
        board_state = n.get_board_state()
        card_play = keezen_bot(board_state)
        n.send(card_play)
        all_pawns_of_current_player_are_in_finish = n.receive()

    bla = 1
"""
    run = True
    n = Network()
    startPos = n.getPos()
    p = Player(startPos[0],startPos[1],100,100,(0,255,0))
    p2 = Player(0,0,100,100,(255,0,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = n.send((p.x, p.y))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2)
"""

server_IP = "192.168.1.109"
main(server_IP)
