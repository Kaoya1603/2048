import pygame
import sqlite3
from random import choices


def youxi(n):
    yanse = {0: (255, 248, 220),
             2: (255, 160, 122),
             4: (255, 99, 71),
             8: (255, 69, 0),
             16: (220, 20, 60),
             32: (238, 130, 238),
             64: (106, 90, 205),
             128: (123, 104, 238),
             256: (135, 206, 235),
             512: (64, 224, 208),
             1024: (0, 255, 127),
             2048: (173, 255, 47),
             4096: (255, 255, 0)}

    pygame.init()
    pygame.display.set_caption('2048')
    size = width, height = n * 50 + 110, n * 50 + 220
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 240))

    pygame.mixer.music.load("yinyue/Homescapes OST - Match 3 - Track 2_1.mp3")
    click = pygame.mixer.Sound("yinyue/click.wav")
    click.set_volume(100)

    class Board:
        def __init__(self, width, height):
            self.con = sqlite3.connect('2048.db')
            self.cur = self.con.cursor()

            self.width = width
            self.height = height
            self.board = [[0] * width for _ in range(height)]
            self.left = 55
            self.top = 175
            self.cell_size = 50
            self.defen = 0
            self.gaofen = self.cur.execute('SELECT gaofen FROM fenbiao').fetchall()[0][0]

        def get_left(self):
            return self.left

        def get_top(self):
            return self.top

        def get_cell_size(self):
            return self.cell_size

        def get_defen(self):
            return self.defen

        def get_gaofen(self):
            return self.gaofen

        def clear_board(self):
            self.board = [[0] * width for _ in range(height)]

        def set_view(self, surface):
            pygame.draw.rect(screen, (255, 248, 220), (self.left, self.top, n * 50, n * 50))

            for ci in range(2):
                self.tianjia_shuzi()

            for i in range(self.height):
                for j in range(self.width):
                    pygame.draw.rect(surface, (192, 192, 192), (
                        self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size),
                                     width=3)
                    pygame.draw.rect(screen, yanse[self.board[i][j]], (
                        self.left + self.cell_size * j + 2, self.top + self.cell_size * i + 2, self.cell_size - 4,
                        self.cell_size - 4))

                    size = 4 * (len(str(self.board[i][j])) - 1)
                    font = pygame.font.Font('OpenSans-Regular.ttf', 30 - size)
                    if self.board[i][j]:
                        shuzi = font.render(str(self.board[i][j]), True, 'black', None)
                        shuzi_rect = shuzi.get_rect()
                        shuzi_rect.x, shuzi_rect.y = self.left + self.cell_size * j + (
                                self.cell_size // 2 - shuzi_rect.width // 2), \
                                                     self.top + self.cell_size * i + (
                                                             self.cell_size // 2 - shuzi_rect.height // 2)
                        screen.blit(shuzi, shuzi_rect)

        def tianjia_shuzi(self):
            x, y = choices(range(n), k=2)
            while self.board[x][y] != 0:
                x, y = choices(range(n), k=2)
            self.board[x][y] = 2

        def render(self, surface):
            pygame.draw.rect(screen, (255, 248, 220), (self.left, self.top, n * 50, n * 50))

            for i in range(self.height):
                for j in range(self.width):
                    pygame.draw.rect(surface, (192, 192, 192), (
                        self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size),
                                     width=3)
                    pygame.draw.rect(screen, yanse[self.board[i][j]], (
                        self.left + self.cell_size * j + 2, self.top + self.cell_size * i + 2, self.cell_size - 4,
                        self.cell_size - 4))

                    size = 4 * (len(str(self.board[i][j])) - 1)
                    font = pygame.font.Font('OpenSans-Regular.ttf', 30 - size)
                    if self.board[i][j]:
                        shuzi = font.render(str(self.board[i][j]), True, 'black', None)
                        shuzi_rect = shuzi.get_rect()
                        shuzi_rect.x, shuzi_rect.y = self.left + self.cell_size * j + (
                                self.cell_size // 2 - shuzi_rect.width // 2), \
                                                     self.top + self.cell_size * i + (
                                                             self.cell_size // 2 - shuzi_rect.height // 2)
                        screen.blit(shuzi, shuzi_rect)

        def move(self, direction):
            if direction == pygame.K_DOWN:
                for c in range(n):
                    column = list(self.board[x][c] for x in range(n))
                    while 0 in column:
                        column.remove(0)
                    for x in range(n - len(column)):
                        column.insert(0, 0)
                    for i in range(len(column) - 1, 0, -1):
                        if column[i] == column[i - 1] and column[i] != 0:
                            self.defen += column[i]
                            column[i] *= 2
                            column.pop(i - 1)
                            column.insert(0, 0)
                    for j in range(len(column)):
                        self.board[j][c] = column[j]
            if direction == pygame.K_UP:
                for c in range(n):
                    column = list(self.board[x][c] for x in range(n))
                    while 0 in column:
                        column.remove(0)
                    column += [0] * (n - len(column))
                    for i in range(len(column) - 1):
                        if column[i] == column[i + 1] and column[i] != 0:
                            self.defen += column[i]
                            column[i] *= 2
                            column.pop(i + 1)
                            column.append(0)
                    for j in range(len(column)):
                        self.board[j][c] = column[j]
            if direction == pygame.K_RIGHT:
                for row in self.board:
                    while 0 in row:
                        row.remove(0)
                    for i in range(n - len(row)):
                        row.insert(0, 0)
                    for i in range(len(row) - 1, 0, -1):
                        if row[i] == row[i - 1] and row[i] != 0:
                            self.defen += row[i]
                            row[i] *= 2
                            row.pop(i - 1)
                            row.insert(0, 0)
            if direction == pygame.K_LEFT:
                for row in self.board:
                    while 0 in row:
                        row.remove(0)
                    row += [0] * (n - len(row))
                    for i in range(len(row) - 1):
                        if row[i] == row[i + 1] and row[i] != 0:
                            self.defen += row[i]
                            row[i] *= 2
                            row.pop(i + 1)
                            row.append(0)
            if not self.game_over_check(screen):
                self.tianjia_shuzi()
                self.render(screen)
                self.check_best_result()

        def game_over_check(self, surface):
            game_over = True
            for i in range(n):
                column = list(self.board[x][i] for x in range(n))
                row = self.board[i]
                for j in range(n - 1):
                    if row[j] == row[j + 1] or column[j] == column[j + 1]:
                        game_over = False
            if game_over:
                self.baocun_gaofen()

                s = pygame.Surface((n * self.get_cell_size(), n * self.get_cell_size()), pygame.SRCALPHA)
                s.fill((105, 105, 105, 128))

                font = pygame.font.Font('OpenSans-Regular.ttf', 30)
                game_over_text = font.render('Игра окончена!', True, (255, 255, 255, 156), None)
                game_over_text_rect = game_over_text.get_rect()
                game_over_text_rect.x, game_over_text_rect.y = n * self.get_cell_size() // 2 - (
                        game_over_text_rect.width // 2), \
                                                               n * self.get_cell_size() // 2 - (
                                                                       game_over_text_rect.height // 2)
                s.blit(game_over_text, game_over_text_rect)

                surface.blit(s, (self.left, self.top))
            return game_over

        def check_best_result(self):
            self.gaofen = max(self.defen, self.gaofen)

        def baocun_gaofen(self):
            self.cur.execute(f'''UPDATE fenbiao SET gaofen = {self.get_gaofen()}''')
            self.con.commit()

    board = Board(n, n)
    board.set_view(screen)

    font = pygame.font.Font('OpenSans-Regular.ttf', 60)
    ming = font.render('20', True, (105, 105, 105), None)
    ming_rect = ming.get_rect()
    ming_rect.x, ming_rect.y = 20, 5
    screen.blit(ming, ming_rect)

    pai = font.render('48', True, (210, 105, 30), None)
    pai_rect = pai.get_rect()
    pai_rect.x, pai_rect.y = ming_rect.x + ming_rect.width, ming_rect.y
    screen.blit(pai, pai_rect)

    font = pygame.font.Font('OpenSans-Regular.ttf', 13)
    dangshi_jieguo_text = font.render('Текущий результат', True, (105, 105, 105), None)
    dangshi_jieguo_text_rect = dangshi_jieguo_text.get_rect()
    dangshi_jieguo_text_rect.x, dangshi_jieguo_text_rect.y = board.get_left() + n * board.get_cell_size() - dangshi_jieguo_text_rect.width, 10
    screen.blit(dangshi_jieguo_text, dangshi_jieguo_text_rect)

    gao_jieguo_text = font.render('Лучший результат', True, (105, 105, 105), None)
    gao_jieguo_text_rect = gao_jieguo_text.get_rect()
    gao_jieguo_text_rect.x, gao_jieguo_text_rect.y = board.get_left() + n * board.get_cell_size() - gao_jieguo_text_rect.width, dangshi_jieguo_text_rect.y + 52
    screen.blit(gao_jieguo_text, gao_jieguo_text_rect)

    def actual_score_board(surface):
        font = pygame.font.Font('OpenSans-Regular.ttf', 28)
        defen_text = font.render(str(board.get_defen()), True, (0, 0, 0), None)
        defen_text_rect = defen_text.get_rect()
        defen_text_rect.x, defen_text_rect.y = board.get_left() + n * board.get_cell_size() - defen_text_rect.width, \
                                               dangshi_jieguo_text_rect.y + 15

        pygame.draw.rect(surface, (255, 255, 240), (defen_text_rect.x, defen_text_rect.y + 4,
                                                    defen_text_rect.width, defen_text_rect.height))

        surface.blit(defen_text, defen_text_rect)

    def actual_bests(surface):
        font = pygame.font.Font('OpenSans-Regular.ttf', 28)
        gaofen_text = font.render(str(board.get_gaofen()), True, (0, 0, 0), None)
        gaofen_text_rect = gaofen_text.get_rect()
        gaofen_text_rect.x, gaofen_text_rect.y = board.get_left() + n * board.get_cell_size() - gaofen_text_rect.width, \
                                                 gao_jieguo_text_rect.y + 15

        pygame.draw.rect(surface, (255, 255, 240), (gaofen_text_rect.x, gaofen_text_rect.y + 4,
                                                    gaofen_text_rect.width, gaofen_text_rect.height))
        surface.blit(gaofen_text, gaofen_text_rect)

    anniu = pygame.sprite.Group()
    anniu_tupian = ['huidao_jia_biaozhi.png', 'kai_sheng_biaozhi.png', 'chongxin_biaozhi1.png']

    class Anniu(pygame.sprite.Sprite):
        def __init__(self, group, hao):
            super().__init__(group)
            self.hao = hao
            self.jieguo = False
            self.image = pygame.image.load('tupian/' + anniu_tupian[self.hao])
            self.rect = self.image.get_rect()
            self.rect.y = board.get_top() - 53
            if self.hao == 0:
                self.rect.x = board.get_left()
            elif self.hao == 1:
                self.rect.x = board.get_left() + (n - 2) * board.get_cell_size() + 10
                self.shengyin = True
                self.flPause = False
            elif self.hao == 2:
                self.rect.x = board.get_left() + (n - 1) * board.get_cell_size() + 10

        def update(self, *args):
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                if self.hao == 1:
                    if self.shengyin:
                        self.image = pygame.image.load('tupian/guan_sheng_biaozhi.png')
                        self.shengyin = False
                    else:
                        self.image = pygame.image.load('tupian/' + anniu_tupian[self.hao])
                        self.shengyin = True

                    self.flPause = not self.flPause
                    if self.flPause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                elif self.hao == 2:
                    board.clear_board()
                    board.set_view(screen)

                elif self.hao == 0:
                    board.baocun_gaofen()

    for i in range(1, 3):
        Anniu(anniu, i)

    pygame.mixer.music.play(-1)
    flPause = False

    actual_score_board(screen)
    actual_bests(screen)

    jieguo = False
    running = True
    while running:
        pygame.draw.rect(screen, (255, 255, 240),
                         (board.get_left(), board.get_top() - 53, n * board.get_cell_size(), 40))
        anniu.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.baocun_gaofen()
                running = False
            if event.type == pygame.KEYDOWN:
                board.move(event.key)

                actual_score_board(screen)
                actual_bests(screen)

                click.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                anniu.update(event)
        pygame.display.flip()
    pygame.quit()
    return jieguo
