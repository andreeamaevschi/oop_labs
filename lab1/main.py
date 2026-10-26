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
        if msg_level.value < Logger.level.value:
            return
        print(f"[{msg_level.name}] {self.__name}: {message}")


def test_logger():
    print("Logger levels")
    app = Logger("App")
    db = Logger("Database")
    app.log(LogLevel.TRACE, "This is a trace message")
    app.log(LogLevel.INFO, "This is an info message")
    db.log(LogLevel.WARN, "This is a warning")
    db.log(LogLevel.ERROR, "This is an error")
    Logger.set_level(LogLevel.ERROR)
    print("Level changed to ERROR")
    app.log(LogLevel.INFO, "This info is hidden now")
    db.log(LogLevel.ERROR, "Only errors are printed")


test_logger()
