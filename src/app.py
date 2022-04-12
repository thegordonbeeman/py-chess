import pygame as pg
from .board import Board
from .utils import extend_rect, darker


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

        # --------- GAME ENDED UI -----------
        self.ended_game = False
        self.finality = "Check Mate"
        # copy of the screen
        self.bg_on_end = None
        # greying layer
        self.layer = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        self.layer.fill((0, 0, 0))
        self.layer.set_alpha(128)
        # fonts
        self.title_font = pg.font.Font("fonts/Metropolis-Bold.otf", 30)
        self.subtitle_font = pg.font.Font("fonts/Metropolis-Black.otf", 20)
        self.button_font = pg.font.Font("fonts/Metropolis-Black.otf", 25)
        # text
        self.title = None
        self.subtitle = None
        self.button = self.button_font.render("Restart", True, (255, 255, 255))
        # background
        self.background = pg.Surface((300, 300))
        # rects
        self.bg_rect = self.background.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.title_rect = self.background.get_rect(center=(self.bg_rect.x + self.bg_rect.w // 2,
                                                           self.bg_rect.y + self.bg_rect.h / 4))
        self.subtitle_rect = self.background.get_rect(center=(self.bg_rect.x + self.bg_rect.w // 2,
                                                              self.bg_rect.y + self.bg_rect.h // 2))
        self.button_rect = self.button.get_rect(center=(self.bg_rect.x + self.bg_rect.w // 2,
                                                        self.bg_rect.y + self.bg_rect.h * 3 / 4))
        self.bg_button = extend_rect(self.button_rect, 10)

    def _quit(self):
        self.running = False
        pg.quit()
        raise SystemExit

    def init_ending_ui(self):
        self.bg_on_end = self.screen.copy()
        self.title = self.title_font.render(f"{self.finality} !", True, (0, 0, 0))
        self.subtitle = self.subtitle_font.render("It's a draw." if self.finality == "Stalemate"
                                                  else f"{(self.board.turn[0]).capitalize() + self.board.turn[1:]} "
                                                       f"won by checkmate.", True, (0, 0, 0))
        self.background.fill(self.board.white)
        self.title_rect = self.title.get_rect(center=self.title_rect.center)
        self.subtitle_rect = self.subtitle.get_rect(center=self.subtitle_rect.center)

    def run(self):
        self.screen.fill((49, 46, 43))
        self.board.reset_screen()
        pg.display.update()

        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.board.ended_game:
                            self.board.handle_clicks(event.pos)
                            pg.display.update()

                        else:
                            if self.board.get_check_king(self.board.get_king(self.board.turn).index,
                                                         self.board.turn):
                                self.finality = "Checkmate"
                            else:
                                self.finality = "Stalemate"
                            self.ended_game = True
                            self.init_ending_ui()
                            if self.bg_rect.collidepoint(event.pos):
                                self.ended_game = False
                                self.screen.fill((49, 46, 43))
                                self.board = Board(self.screen)
                                self.board.update()
                                self.board.reset_screen()
                                pg.display.update()

            if self.board.ended_game:
                self.init_ending_ui()
                self.screen.blit(self.bg_on_end, (0, 0))
                self.screen.blit(self.layer, (0, 0))
                self.screen.blit(self.background, self.bg_rect)

                self.screen.blit(self.title, self.title_rect)
                self.screen.blit(self.subtitle, self.subtitle_rect)
                if self.button_rect.collidepoint(pg.mouse.get_pos()):
                    pg.draw.rect(self.screen, darker(self.board.select_color, 20), self.bg_button)
                else:
                    pg.draw.rect(self.screen, self.board.select_color, self.bg_button)
                self.screen.blit(self.button, self.button_rect)

                pg.display.update()
                self.clock.tick(60)
            else:
                self.clock.tick(30)
