import pygame as pg


pg.init()


class Colors:
    BACKGROUND = pg.Color(30, 30, 30)
    NAV_BACKGROUND = pg.Color(50,50,50)

    TXT_OUT = pg.Color('lightskyblue3')
    TXT_ERR = pg.Color('firebrick1')
    TXT_IN = pg.Color('darkolivegreen1')
    CURSOR = pg.Color(230,230,230,100)

    DIR = pg.Color("#E99E3D")
    PROG = pg.Color("#BDCDDB")
    FILE = pg.Color("#FEFAE0")

    PASS_BOX = pg.Color(15, 15, 15)

    CURR_NODE = pg.Color("#EBD288")
    VISITED = pg.Color("#183078")
    VISIBLE = pg.Color("#9EAEDE")
    INVISIBLE = pg.Color("#525663")
    EDGE = pg.Color("#F1FFFA")
    # ARROW = pg.Color("#464E47")
    ARROW = EDGE


# NOTE: Must be a uniform-sized "terminal" fonts
class Fonts:
    TERMINAL = pg.font.SysFont('Consolas', 17)
    PASSWORD = pg.font.SysFont('Consolas', 54)
    PROMPT = pg.font.SysFont('Consolas', 24)
    TEXT = TERMINAL
    HINT = pg.font.SysFont('Consolas', 14)
    NODE_LABEL = pg.font.SysFont('Consolas', 18)
