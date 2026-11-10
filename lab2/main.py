import random
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
    random_messages = {
        LogLevel.TRACE: ["Checking the next step", "Still working", "Looking closer"],
        LogLevel.INFO: ["Operation completed", "Everything looks good", "Here is your result"],
        LogLevel.WARN: ["Be careful", "This looks strange", "Something is not right"],
        LogLevel.ERROR: ["Something went wrong", "This did not work", "Please check the input"],
    }

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
        text = text.replace("%r", random.choice(Logger.random_messages[msg_level]))
        text = text.replace("%m", message)
        print(text)

    def trace(self, message):
        self.log(LogLevel.TRACE, message)

    def info(self, message):
        self.log(LogLevel.INFO, message)

    def warn(self, message):
        self.log(LogLevel.WARN, message)

    def error(self, message):
        self.log(LogLevel.ERROR, message)


class ParenthesesValidator:
    def __init__(self):
        self.logger = Logger("Parentheses")

    def is_valid(self, text):
        open_count = 0
        for i in range(len(text)):
            if text[i] == "(":
                open_count += 1
                self.logger.trace(f"Opening parenthesis found at position {i}")
            elif text[i] == ")":
                if open_count == 0:
                    self.logger.warn(f"Closing parenthesis at position {i} has nothing to match")
                    self.logger.error(f"{text} is invalid because a closing parenthesis has no opening parenthesis")
                    self.logger.info("Result: false")
                    return False
                open_count -= 1
                self.logger.info(f"Matching pair found, closed at position {i}")
        if open_count > 0:
            self.logger.error(f"{text} is invalid because {open_count} opening parenthesis has no match")
            self.logger.info("Result: false")
            return False
        self.logger.info("Result: true")
        return True


def test_logger():
    print("Logger levels")
    app = Logger("App")
    db = Logger("Database")
    app.trace("This is a trace message")
    app.info("This is an info message")
    db.warn("This is a warning")
    db.error("This is an error")
    Logger.set_level(LogLevel.ERROR)
    print("Level changed to ERROR")
    app.info("This info is hidden now")
    db.error("Only errors are printed")
    Logger.set_level(LogLevel.INFO)

    print("Logger formats")
    test = Logger("Parentheses")
    Logger.set_format("[%l] %m")
    test.error("Invalid input")
    Logger.set_format("%n: %m")
    test.info("Valid input")
    Logger.set_format("[%t] %m")
    test.info("Valid input")
    Logger.set_format("%l - %n - %m")
    test.info("Valid input")
    Logger.set_format("[%l] %r: %m")
    test.info("Valid input")
    test.error("Invalid input")
    Logger.set_format("[%t] [%l] %n: %m")


def test_validator():
    print("Parentheses tests")
    Logger.set_level(LogLevel.INFO)
    validator = ParenthesesValidator()
    tests = [
        ("()", True),
        (")(()))", False),
        ("(", False),
        ("(())((()())())", True),
        ("(()", False),
        ("())", False),
        ("", True),
    ]
    for text, expected in tests:
        print(f"Input: {text}")
        result = validator.is_valid(text)
        if result == expected:
            print("PASS")
        else:
            print(f"FAIL, expected {expected}")

    print("Same input with level TRACE")
    Logger.set_level(LogLevel.TRACE)
    validator.is_valid("(()")


test_logger()
test_validator()
