from enum import Enum


class JWTType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"