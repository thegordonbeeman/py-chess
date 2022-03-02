import pygame as pg
from functools import cache


def load_img(path: str, alpha=True) -> pg.Surface:
    return pg.image.load(path).convert_alpha() if alpha else pg.image.load(path).convert()


def smoothscale_sq(img: pg.Surface, size: int) -> pg.Surface:
    return pg.transform.smoothscale(img, (size, size))


def extend_rect(rect: pg.Rect, extension: int) -> pg.Rect:
    return pg.Rect(rect.x - extension, rect.y - extension, rect.w + extension * 2, rect.h + extension * 2)


@cache
def darker(color: tuple[int, int, int], k: int) -> tuple[int, int, int]:
    return (color[0] - k if color[0] - k >= 0 else 0,
            color[1] - k if color[1] - k >= 0 else 0,
            color[2] - k if color[2] - k >= 0 else 0)


@cache
def lighter(color: tuple[int, int, int], k: int) -> tuple[int, int, int]:
    return (color[0] + k if color[0] + k <= 255 else 255,
            color[1] + k if color[1] + k <= 255 else 255,
            color[2] + k if color[2] + k <= 255 else 255)
