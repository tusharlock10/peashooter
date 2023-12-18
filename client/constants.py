from enum import Enum

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


class NetworkEvents(Enum):
    CONNECT = {"type": "connect", "value": None}
    DISCONNECT = {"type": "disconnect", "value": None}
    SHIP_ID = {"type": "ship_id", "value": None}
    NEW_SHIP = {"type": "new_ship", "value": None}
    REMOVE_SHIP = {"type": "remove_ship", "value": None}
    CHANGE_POSITION = {"type": "change_position", "value": None}
    CREATE_BULLET = {"type": "create_bullet", "value": None}


class MaterialColors(Enum):
    RED = (244, 67, 54)
    BLUE = (33, 150, 243)
    GREEN = (139, 195, 74)
    YELLOW = (255, 235, 59)
    ORANGE = (255, 152, 0)


ID_COLOR_MAP = {
    0: MaterialColors.RED.value,
    1: MaterialColors.BLUE.value,
    2: MaterialColors.GREEN.value,
    3: MaterialColors.YELLOW.value,
    4: MaterialColors.ORANGE.value,
}
