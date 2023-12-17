from enum import Enum


class NetworkEvents(Enum):
    CONNECT = {"type": "connect", "value": None}
    DISCONNECT = {"type": "disconnect", "value": None}
    SHIP_ID = {"type": "ship_id", "value": None}
    NEW_SHIP = {"type": "new_ship", "value": None}
    REMOVE_SHIP = {"type": "remove_ship", "value": None}
