# ObjectOrientedDesign/Essence.kt
from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, Tuple


class Urge(Enum):
    North = 1
    South = 2
    East = 3
    West = 4


class Robot:
    def __init__(self, room: Room):
        self.room = room

    def turn(self, urge: Urge):
        # Get a reference to the Room you've
        # been urged to go to, and see what
        # happens when we enter the Room.
        # Point robot to returned Room:
        self.room = self.room.doors.open(urge).enter(self)

    def __str__(self):
        return f"Robot {self.room.doors}"


class Item(ABC):
    def __init__(self, symbol: str):
        self.symbol = symbol

    @abstractmethod
    def interact(self, robot: Robot, room: Room) -> Room:
        pass

    def __str__(self):
        return self.symbol


class Mech(Item):
    symbol = 'R'

    def __init__(self):
        super().__init__(symbol)

    def interact(self, robot: Robot, room: Room):
        return robot.room  # Stay in original room


class Wall(Item):
    symbol = '#'

    def __init__(self):
        super().__init__(symbol)

    def interact(self, robot: Robot, room: Room):
        return robot.room  # Stay in original room


class Food(Item):
    symbol = '.'

    def __init__(self):
        super().__init__(symbol)

    def interact(self, robot: Robot, room: Room):
        print("Eat food")
        room.occupant = Empty()
        return room  # Move to new room


class Teleport(Item):
    "Jump to the room with the same target"

    def __init__(self, target: str):
        super().__init__(target)

    def interact(self, robot: Robot, room: Room):
        pass


class Empty(Item):
    "Room is there, but nothing is in it"
    symbol = ' '

    def __init__(self):
        super().__init__(symbol)

    def interact(self, robot: Robot, room: Room):
        return room  # Move to new room


class Edge(Item):
    "The unknown void outside the maze"
    symbol = '_'

    def __init__(self):
        super().__init__(symbol)

    def interact(self, robot: Robot, room: Room):
        return robot.room  # Stay in original room


class EndGame(Item):
    "The game is over"
    symbol = '!'

    def __init__(self):
        super().__init__(symbol)

    def interact(self, robot: Robot, room: Room):
        return room


class Doors:
    def __init__(self):
        self.north = Room(Edge())
        self.south = Room(Edge())
        self.east = Room(Edge())
        self.west = Room(Edge())

    def connect(self, row: int, col: int,
                grid: Dict[Tuple[int, int], Room]):
        def link(to_row: int, to_col: int):
            return grid.get((to_row, to_col), Room(Edge()))

        self.north = link(row - 1, col)
        self.south = link(row + 1, col)
        self.east = link(row, col + 1)
        self.west = link(row, col - 1)

    def open(self, urge: Urge) -> Room:
        # Pattern Match:
        return {
            Urge.North: self.north,
            Urge.South: self.south,
            Urge.East: self.east,
            Urge.West: self.west
        }.get(urge, Room(Edge()))

    def __str__(self):
        return f"[N({self.north.occupant}), " + \
               f"S({self.south.occupant}), " + \
               f"E({self.east.occupant}), " + \
               f"W({self.west.occupant})]"


class Room:
    def __init__(self, occupant: Item = Empty()):
        self.occupant = occupant
        self.doors = Doors()

    def enter(self, robot: Robot) -> Room:
        return self.occupant.interact(robot, self)

    def __str__(self):
        return f"Room({self.occupant}) {self.doors}"


class RoomBuilder:
    def __init__(self, maze: str):
        self.grid: Dict[Tuple[int, int], Room] = {}
        self.robot = Robot(Room(Edge()))  # Nowhere
        # Stage 1: Create grid
        lines = maze.split("\n")
        # lines.withIndex().forEach {(r, line) -> line.withIndex().forEach {(c, char) -> grid[Pair(r, c)] = create_room(char)
        # Stage 2: Connect the rooms
        # grid.forEach{(pair, r) -> r.doors.connect(pair.first, pair.second, grid)
        # Stage 3: Locate the robot
        # robot.room = grid.values.find  {it.occupant == Mech}  ?: robot.room

    def room(self, row: int, col: int):
        f"({row}, {col}) " + str(self.grid.get((row, col), Room(Edge())))

    def create_room(self, c: str) -> Room:
        for item in Item.__subclasses__():
            if c == item.symbol:
                return Room(item())
        return Room(Teleport(c))

    def __str__(self):
        return f"""grid.map {"${it.key} ${it.value}"}.joinToString("\n")"""


string_maze = """
a ...#... c
R ...#...
###########
a ....... b
###########
! c ..... b
""".strip()


def main():
    builder = RoomBuilder(string_maze).build()
    print(builder.room(0, 0))
    print(builder.room(1, 6))
    print(builder.room(5, 0))
    robot = builder.robot
    print(robot)
    robot.turn(Urge.East)
    robot.turn(Urge.East)
    robot.turn(Urge.South)
    print(robot)


"""
Output:
(0, 0)
Room(T)[N(_), S(R), E(), W(_)]
(1, 6)
Room(.) [N(.), S(  # ), E(.), W(#)]
    (5, 0)
Room(!) [N(  # ), S(_), E( ), W(_)]
    Robot[N(T), S(  # ), E( ), W(_)]
        Eat food
    Robot[N(.), S(  # ), E(.), W( )]
"""
