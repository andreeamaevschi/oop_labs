from enum import Enum


class LogLevel(Enum):
    TRACE = 1
    INFO = 2
    WARN = 3
    ERROR = 4


class Logger:
    level = LogLevel.INFO

    def __init__(self, name):
        self.__name = name

    @classmethod
    def set_level(cls, new_level):
        cls.level = new_level

    def log(self, msg_level, message):
        print(f"[{msg_level.name}] {self.__name}: {message}")


def test_logger():
    app = Logger("App")
    app.log(LogLevel.INFO, "This is an info message")
    app.log(LogLevel.ERROR, "This is an error")


test_logger()
