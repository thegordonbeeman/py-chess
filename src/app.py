import pygame as pg
from board import Board


class App:

    def __init__(self):

        # ---------- SCREEN & CONST ---------
        self.screen = pg.display.set_mode((800, 800), pg.SCALED)
        self.running = True

        # --------- BOARD -------------------
        self.board = Board(self.screen)

    def _quit(self):
        self.running = False
        pg.quit()
        raise SystemExit

    def run(self):

        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.board.handle_clicks(event.pos)

            self.screen.fill((255, 255, 255))
            self.board.update()

            pg.display.update()

App=App()
App.run()