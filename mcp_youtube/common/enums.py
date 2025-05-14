from enum import Enum


class Transport(str, Enum):
    STDIO = "stdio"
    SSE = "sse"
