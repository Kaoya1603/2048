import pygame


def menu():
    yanse = {0: (255, 248, 220),
             2: (255, 160, 122),
             4: (255, 99, 71),
             8: (255, 69, 0),
             16: (220, 20, 60),
             32: (238, 130, 238)}

    pygame.init()
    pygame.display.set_caption('2048')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 240))

    font = pygame.font.Font('OpenSans-Regular.ttf', 60)
    ming = font.render('20', True, (105, 105, 105), None)
    ming_rect = ming.get_rect()
    ming_rect.x, ming_rect.y = 20, 5
    screen.blit(ming, ming_rect)

    pai = font.render('48', True, (210, 105, 30), None)
    pai_rect = pai.get_rect()
    pai_rect.x, pai_rect.y = ming_rect.x + ming_rect.width, ming_rect.y
    screen.blit(pai, pai_rect)

    font = pygame.font.Font('OpenSans-Regular.ttf', 20)
    shuoming = font.render('выберите размер поля', True, (125, 125, 125), None)
    shuoming_rect = shuoming.get_rect()
    shuoming_rect.x, shuoming_rect.y = 200, 30
    screen.blit(shuoming, shuoming_rect)

    xiaoban = list()

    class XiaoBan:
        def __init__(self, shuzi):
            self.shuzi = shuzi
            self.board = [[0] * self.shuzi for _ in range(self.shuzi)]
            self.left = 55
            self.top = 90
            self.width = 175
            if self.shuzi == 6:
                self.left += 205
            elif self.shuzi == 7:
                self.top += 200
            elif self.shuzi == 8:
                self.left += 205
                self.top += 200
            self.cell_size = self.width // self.shuzi
            self.rect = pygame.rect.Rect(self.left, self.top, self.width, self.width)

        def render(self, surface):
            self.board[0][0] = 16
            self.board[0][1] = 8
            self.board[1][-1] = 4
            self.board[1][0] = 32
            self.board[0][-1] = 2
            self.board[-1][0] = 16
            self.board[-1][1] = 4

            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    pygame.draw.rect(surface, (192, 192, 192), (
                        self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size),
                                     width=2)
                    pygame.draw.rect(screen, yanse[self.board[i][j]], (
                        self.left + self.cell_size * j + 1, self.top + self.cell_size * i + 2, self.cell_size - 2,
                        self.cell_size - 2))

                    size = 4 * (len(str(self.board[i][j])) - 1)
                    font = pygame.font.Font('OpenSans-Regular.ttf', 18 - size)
                    if self.board[i][j]:
                        shuzi = font.render(str(self.board[i][j]), True, 'black', None)
                        shuzi_rect = shuzi.get_rect()
                        shuzi_rect.x, shuzi_rect.y = self.left + self.cell_size * j + (
                                self.cell_size // 2 - shuzi_rect.width // 2), \
                                                     self.top + self.cell_size * i + (
                                                             self.cell_size // 2 - shuzi_rect.height // 2)
                        screen.blit(shuzi, shuzi_rect)

        def xuanze(self, *args):
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                return self.shuzi

    for n in range(5, 9, 1):
        xiaoban.append(XiaoBan(n))
        xiaoban[-1].render(screen)

    n = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = list(filter(lambda x: x is not None, list(xiaoban[i].xuanze(event) for i in range(len(xiaoban)))))[
                    0]
                running = False
        pygame.display.flip()
    pygame.quit()
    return n if n else False
