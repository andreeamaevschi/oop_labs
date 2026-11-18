import sys
import os
import math
import random
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    TRACE = 1
    INFO = 2
    WARN = 3
    ERROR = 4


class Formatter:
    random_messages = {
        LogLevel.TRACE: ["Checking the next step", "Still working", "Looking closer"],
        LogLevel.INFO: ["Operation completed", "Everything looks good", "Here is your result"],
        LogLevel.WARN: ["Be careful", "This looks strange", "Something is not right"],
        LogLevel.ERROR: ["Something went wrong", "This did not work", "Please check the input"],
    }

    def __init__(self, format="[%t] [%l] %n: %m"):
        self.__format = format

    def format(self, level, name, message):
        line = self.__format
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

    def __init__(self, name, formatter=None, sink=None):
        self.__name = name
        if formatter == None:
            formatter = Formatter()
        if sink == None:
            sink = ConsoleSink()
        self.__formatter = formatter
        self.__sink = sink

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
    f1 = Formatter()
    f2 = Formatter("[%l] %m")
    f3 = Formatter("%n: %m")
    f4 = Formatter("%l - %n - %m")
    f5 = Formatter('[%l] %r: %m')
    print(f1.format(LogLevel.INFO, "Parentheses", "Valid input"))
    print(f2.format(LogLevel.ERROR, "Parentheses", "Invalid input"))
    print(f3.format(LogLevel.INFO, "Parentheses", "Valid input"))
    print(f4.format(LogLevel.INFO, "Parentheses", "Valid input"))
    print(f5.format(LogLevel.INFO, "Parentheses", "Valid input"))
    print(f3.format(LogLevel.INFO, "Test", "Ratio is 100%n"))


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

    shared = Formatter("[%t] [%l] %n: %m")
    console = ConsoleSink()
    parser = Logger("Parser", shared, console)
    manager = Logger("Manager", shared, console)
    special = Logger("Special", Formatter("%l >> %m"), console)
    parser.info("I use the shared formatter")
    manager.info("Me too")
    special.info("I have my own formatter")


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


class Display:
    def __init__(self, model, width, height, ppi):
        self.model = model
        self.width = width
        self.height = height
        self.ppi = ppi

    def getDiagonal(self):
        return math.sqrt(self.width * self.width + self.height * self.height) / self.ppi

    def compareSize(self, other):
        d1 = round(self.getDiagonal(), 1)
        d2 = round(other.getDiagonal(), 1)
        if d1 > d2:
            print(f'{self.model} ({d1}") is bigger than {other.model} ({d2}")')
            return 1
        elif d1 < d2:
            print(f'{self.model} ({d1}") is smaller than {other.model} ({d2}")')
            return -1
        else:
            print(f'{self.model} ({d1}") has the same size as {other.model} ({d2}")')
            return 0

    def compareSharpness(self, other):
        if self.ppi > other.ppi:
            print(f"{self.model} ({self.ppi} ppi) is sharper than {other.model} ({other.ppi} ppi)")
            return 1
        elif self.ppi < other.ppi:
            print(f"{self.model} ({self.ppi} ppi) is less sharp than {other.model} ({other.ppi} ppi)")
            return -1
        else:
            print(f"{self.model} and {other.model} are the same sharpness ({self.ppi} ppi)")
            return 0

    def compareWithMonitor(self, other):
        size = self.compareSize(other)
        sharp = self.compareSharpness(other)
        if size == 1 and sharp == 1:
            print(f"Verdict: {self.model} is better, it is bigger and sharper")
        elif size == -1 and sharp == -1:
            print(f"Verdict: {other.model} is better, it is bigger and sharper")
        elif size == 0 and sharp == 0:
            print("Verdict: they are the same")
        elif size + sharp > 0:
            print(f"Verdict: {self.model} is a bit better")
        elif size + sharp < 0:
            print(f"Verdict: {other.model} is a bit better")
        else:
            print("Verdict: each one is better at something, it depends what you need")


def testDisplays():
    print("Display tests")
    d1 = Display("Samsung-Odyssey-G5", 2560, 1440, 93.0)
    d2 = Display("LG-27GP850", 2560, 1440, 108.8)
    d3 = Display("Dell-U2723QE", 3840, 2160, 163.0)
    d1.compareSize(d2)
    d2.compareSharpness(d3)
    d1.compareWithMonitor(d3)
    d2.compareWithMonitor(d3)


class DisplayManager:
    def __init__(self, name, logger):
        self.name = name
        self.assignedDisplays = []
        self.logger = logger

    def assignDisplay(self, d):
        self.assignedDisplays.append(d)
        self.logger.trace(f"{d.model} assigned to {self.name}")

    def assist(self):
        if len(self.assignedDisplays) == 0:
            self.logger.warn(f"{self.name} has no displays, nothing to compare")
            return
        if len(self.assignedDisplays) == 1:
            self.logger.warn(f"{self.name} has only {self.assignedDisplays[0].model}, nothing to compare it with")
            return
        print(f"{self.name} compares the displays:")
        i = 0
        while i < len(self.assignedDisplays) - 1:
            self.assignedDisplays[i].compareWithMonitor(self.assignedDisplays[i + 1])
            i = i + 1

    def buyDisplay(self, d):
        self.assignedDisplays.remove(d)
        self.logger.info(f"{self.name} sold {d.model}")
        if len(self.assignedDisplays) == 0:
            self.logger.warn(f"{self.name} has no displays left after this purchase")
        return d


def testManagers():
    print("Manager tests")
    Logger.set_level(LogLevel.TRACE)
    bob = DisplayManager("Bob", managerLog)
    alice = DisplayManager("Alice", managerLog)
    dell = Display("Dell-U2723QE", 3840, 2160, 163.0)
    lg = Display("LG-27GP850", 2560, 1440, 108.8)
    apple = Display("Apple-StudioDisplay", 5120, 2880, 218.0)
    bob.assignDisplay(dell)
    bob.assignDisplay(lg)
    alice.assignDisplay(apple)
    alice.assignDisplay(dell)
    bob.assist()
    bought = bob.buyDisplay(dell)
    print("Bought:", bought.model)
    print("Bob still has:")
    for d in bob.assignedDisplays:
        print("  ", d.model)
    print("Alice still has:")
    for d in alice.assignedDisplays:
        print("  ", d.model)
    Logger.set_level(LogLevel.INFO)


class CommandReader:
    def __init__(self, path, logger):
        self.path = path
        self.logger = logger

    def readLines(self):
        if os.path.exists(self.path) == False:
            self.logger.error(f"File {self.path} does not exist, stopping")
            return None
        f = open(self.path)
        lines = f.readlines()
        f.close()
        return lines


managers = []
displays = []


def findManager(name):
    for m in managers:
        if m.name == name:
            return m
    return None


def findDisplay(model):
    for d in displays:
        if d.model == model:
            return d
    return None


def parseCommand(line, number):
    words = line.split()
    if len(words) == 0 or words[0].startswith("#"):
        return
    command = words[0]
    if command == "MANAGER":
        managers.append(DisplayManager(words[1], managerLog))
        parserLog.trace(f"Manager {words[1]} created")
    elif command == "DISPLAY":
        d = Display(words[1], int(words[2]), int(words[3]), float(words[4]))
        displays.append(d)
        parserLog.trace(f'Display {d.model} created ({round(d.getDiagonal(), 1)}", {int(d.ppi)} ppi)')
    elif command == "ASSIGN":
        d = findDisplay(words[1])
        m = findManager(words[2])
        m.assignDisplay(d)
    elif command == "COMPARE":
        d1 = findDisplay(words[1])
        d2 = findDisplay(words[2])
        print(f"Compare {d1.model} with {d2.model}:")
        d1.compareWithMonitor(d2)
    elif command == "ASSIST":
        m = findManager(words[1])
        m.assist()
    elif command == "BUY":
        d = findDisplay(words[1])
        m = findManager(words[2])
        m.buyDisplay(d)
    else:
        print("Unknown command:", command)


def runShop(path):
    reader = CommandReader(path, parserLog)
    lines = reader.readLines()
    if lines == None:
        return
    number=0
    for line in lines:
        number=number+1
        parseCommand(line, number)


formatter = Formatter("[%l] %n: %m")
sink = ConsoleSink()
managerLog = Logger("Manager", formatter, sink)
parserLog = Logger("Parser", formatter, sink)

if len(sys.argv) > 1:
    runShop(sys.argv[1])
else:
    test_formatter()
    test_logger()
    test_validator()
    testDisplays()
    testManagers()
