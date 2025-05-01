from enum import Enum


class WebSocketEvent(Enum):
    MESSAGE = "message"
    JOIN = "join"
    LEAVE = "leave"