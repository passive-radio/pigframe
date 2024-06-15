from dataclasses import dataclass
from pigframe import ActionMap
import pyxel

@dataclass
class Actions(ActionMap):
    # Movement
    up: tuple = pyxel.btn, pyxel.KEY_UP, pyxel.KEY_W
    down: tuple = pyxel.btn, pyxel.KEY_DOWN, pyxel.KEY_S
    left: tuple = pyxel.btn, pyxel.KEY_LEFT, pyxel.KEY_A
    right: tuple = pyxel.btn, pyxel.KEY_RIGHT, pyxel.KEY_D
    
    # Shooting
    shoot: tuple = pyxel.btnp, pyxel.KEY_SPACE, pyxel.MOUSE_BUTTON_LEFT
    
    # Game Control
    start: tuple = pyxel.btnp, pyxel.KEY_RETURN
    restart: tuple = pyxel.btnp, pyxel.KEY_R
    pause: tuple = pyxel.btnp, pyxel.KEY_P

    # Additional Controls
    escape: tuple = pyxel.btn, pyxel.KEY_ESCAPE
    space: tuple = pyxel.btn, pyxel.KEY_SPACE
    space_p: tuple = pyxel.btnp, pyxel.KEY_SPACE
    click_p: tuple = pyxel.btnp, pyxel.MOUSE_BUTTON_LEFT
