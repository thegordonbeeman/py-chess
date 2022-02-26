import pygame as pg
from .board import Board


class App:

    def __init__(self):

        # ---------- SCREEN & CONST ---------
        self.screen = pg.display.set_mode((1000, 1000), pg.SCALED)

        pg.display.set_caption("Py-Chess")  # title of the window
        pg.display.set_icon(pg.image.load("res/21.png").convert_alpha())  # icon of the window

        self.running = True
        self.clock = pg.time.Clock()

        # --------- BOARD -------------------
        self.board = Board(self.screen)

    def _quit(self):
        self.running = False
        pg.quit()
        raise SystemExit

    def run(self):
        self.screen.fill((49, 46, 43))
        self.board.update()
        pg.display.update()

        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.board.handle_clicks(event.pos)
                        self.screen.fill((49, 46, 43))
                        self.board.update()
                        pg.display.update()
