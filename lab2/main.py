import random
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    TRACE = 1
    INFO = 2
    WARN = 3
    ERROR = 4


class Formatter:
    format_string = "[%t] [%l] %n: %m"
    random_messages = {
        LogLevel.TRACE: ["Checking the next step", "Still working", "Looking closer"],
        LogLevel.INFO: ["Operation completed", "Everything looks good", "Here is your result"],
        LogLevel.WARN: ["Be careful", "This looks strange", "Something is not right"],
        LogLevel.ERROR: ["Something went wrong", "This did not work", "Please check the input"],
    }

    @classmethod
    def set_format(cls, new_format):
        cls.format_string = new_format

    def format(self, level, name, message):
        line = Formatter.format_string
        line = line.replace("%t", datetime.now().strftime("%H:%M:%S"))
        line = line.replace("%l", level.name)
        line = line.replace("%n", name)
        line = line.replace("%r", random.choice(Formatter.random_messages[level]))
        line = line.replace("%m", message)
        return line


class ConsoleSink:
    def write(self, line):
        print(line)


class Logger:
    level = LogLevel.INFO

    def __init__(self, name):
        self.__name = name
        self.__formatter = Formatter()
        self.__sink = ConsoleSink()

    @classmethod
    def set_level(cls, new_level):
        cls.level = new_level

    def log(self, msg_level, message):
        if msg_level.value < Logger.level.value:
            return
        line = self.__formatter.format(msg_level, self.__name, message)
        self.__sink.write(line)

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


def test_formatter():
    print("Formatter tests")
    f = Formatter()
    print(f.format(LogLevel.INFO, "Parentheses", "Valid input"))
    Formatter.set_format("[%l] %m")
    print(f.format(LogLevel.ERROR, "Parentheses", "Invalid input"))
    Formatter.set_format("%n: %m")
    print(f.format(LogLevel.INFO, "Parentheses", "Valid input"))
    Formatter.set_format("%l - %n - %m")
    print(f.format(LogLevel.INFO, "Parentheses", "Valid input"))
    Formatter.set_format("[%l] %r: %m")
    print(f.format(LogLevel.INFO, "Parentheses", "Valid input"))
    Formatter.set_format("%n: %m")
    print(f.format(LogLevel.INFO, "Test", "Ratio is 100%n"))
    Formatter.set_format("[%t] [%l] %n: %m")


def test_logger():
    print("Logger tests")
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


test_formatter()
test_logger()
test_validator()
