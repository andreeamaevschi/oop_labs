from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    TRACE = 1
    INFO = 2
    WARN = 3
    ERROR = 4


class Logger:
    level = LogLevel.INFO
    format = "[%t] [%l] %n: %m"

    def __init__(self, name):
        self.__name = name

    @classmethod
    def set_level(cls, new_level):
        cls.level = new_level

    @classmethod
    def set_format(cls, new_format):
        cls.format = new_format

    def log(self, msg_level, message):
        if msg_level.value < Logger.level.value:
            return
        text = Logger.format
        text = text.replace("%t", datetime.now().strftime("%H:%M:%S"))
        text = text.replace("%l", msg_level.name)
        text = text.replace("%n", self.__name)
        text = text.replace("%m", message)
        print(text)


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

    print("Logger formats")
    test = Logger("Parentheses")
    Logger.set_format("[%l] %m")
    test.log(LogLevel.ERROR, "Invalid input")
    Logger.set_format("%n: %m")
    test.log(LogLevel.ERROR, "Valid input")
    Logger.set_format("[%t] %m")
    test.log(LogLevel.ERROR, "Valid input")
    Logger.set_format("%l - %n - %m")
    test.log(LogLevel.ERROR, "Valid input")
    Logger.set_format("[%t] [%l] %n: %m")


test_logger()
