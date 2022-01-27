import pygame as pg


def pos_to_index(pos: str):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
    return [numbers.index(pos[1]), letters.index(pos[0])]


def load_img(path: str, alpha=True) -> pg.Surface:
    return pg.image.load(path).convert_alpha() if alpha else pg.image.load(path).convert()


def smoothscale_sq(img: pg.Surface, size: int) -> pg.Surface:
    return pg.transform.smoothscale(img, (size, size))
