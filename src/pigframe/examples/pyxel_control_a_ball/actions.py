from dataclasses import dataclass
from pigframe import ActionMap
import pyxel

@dataclass
class Actions(ActionMap):
    up: tuple = pyxel.btn, pyxel.KEY_UP, pyxel.KEY_W
    down: tuple = pyxel.btn, pyxel.KEY_DOWN, pyxel.KEY_S
    left: tuple = pyxel.btn, pyxel.KEY_LEFT, pyxel.KEY_A
    right: tuple = pyxel.btn, pyxel.KEY_RIGHT, pyxel.KEY_D
    enter: tuple = pyxel.btn, pyxel.KEY_RETURN, pyxel.KEY_RETURN2
    click: tuple = pyxel.btn, pyxel.MOUSE_BUTTON_LEFT
    click_p: tuple = pyxel.btnp, pyxel.MOUSE_BUTTON_LEFT
    enter_p: tuple = pyxel.btnp, pyxel.KEY_RETURN, pyxel.KEY_RETURN2
    enter_r: tuple = pyxel.btnr, pyxel.KEY_RETURN, pyxel.KEY_RETURN2
    backspace: tuple = pyxel.btn, pyxel.KEY_BACKSPACE, pyxel.KEY_KP_BACKSPACE
    backspace_p: tuple = pyxel.btnp, pyxel.KEY_BACKSPACE, pyxel.KEY_KP_BACKSPACE
    click_r: tuple = pyxel.btnr, pyxel.MOUSE_BUTTON_LEFT
    escape: tuple = pyxel.btn, pyxel.KEY_ESCAPE
    space: tuple = pyxel.btn, pyxel.KEY_SPACE
    space_p: tuple = pyxel.btnp, pyxel.KEY_SPACE
    c_p: tuple = pyxel.btnp, pyxel.KEY_C
    