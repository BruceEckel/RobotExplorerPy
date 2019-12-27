# ObjectOrientedDesign/Essence.kt
from enum import Enum
from typing import List, Dict, Tuple
from time import sleep
import platform
import os

CLEAR = "cls" if platform.system().lower() == "windows" else "clear"


class Urge(Enum):
    North = 1
    South = 2
    East = 3
    West = 4


class Item:
    """Things that can occupy a Room"""
    symbol = ''

    def interact(self, robot, room):
        pass

    def __str__(self) -> str:
        return self.symbol


class Robot(Item):
    symbol = 'R'

    def __init__(self):
        # Robot is a state machine:
        self.room = None

    def move(self, urge: Urge):
        # Get a reference to the Room you've been urged
        # to go to, and see what happens when we enter
        # that Room. Point robot to the returned Room:
        self.room = self.room.doors.open(urge).enter(self)


class Wall(Item):
    """Robot can't pass through a wall"""
    symbol = '#'

    def interact(self, robot: Robot, room):
        return robot.room  # Stay in original room


class Food(Item):
    """Robot can eat food to gain energy"""
    symbol = '.'

    def interact(self, robot: Robot, room):
        room.occupant = Empty() # Food eaten
        return room  # Move to new room


class Teleport(Item):
    """Jump to the room with the same target"""

    def __init__(self, target: str):
        self.target = target
        self.target_room = None

    def interact(self, robot: Robot, room):
        return self.target_room

    def __str__(self) -> str:
        return f"{self.target}"


class Empty(Item):
    """Room is there, but nothing is in it"""
    symbol = '_'

    def interact(self, robot: Robot, room):
        return room  # Move to new room


class Edge(Item):
    """The unknown void outside the maze.
    Robot can't go into an Edge."""
    symbol = '/'

    def interact(self, robot: Robot, room):
        return robot.room  # Stay in original room


class EndGame(Item):
    """The game is over when Robot encounters this"""
    symbol = '!'

    def interact(self, robot: Robot, room):
        print("Game over!")
        return room


def item_factory(symbol: str):
    """Create an Item from its symbol"""
    for item in Item.__subclasses__():
        if symbol == item.symbol:
            return item()
    return Teleport(symbol)


class Doors: pass


class Room:
    """Holds occupant, can be entered by Robot,
    has doors to other rooms."""

    def __init__(self, occupant: Item = Empty()):
        self.occupant = occupant
        self.doors = Doors()

    def enter(self, robot: Robot):
        return self.occupant.interact(robot, self)

    def __repr__(self):
        return f"Room({self.occupant}) {self.doors}"


class Doors:
    """How a Room connects to other Rooms"""
    edge = Room(Edge())

    def __init__(self):
        self.north = Doors.edge
        self.south = Doors.edge
        self.east = Doors.edge
        self.west = Doors.edge

    def connect(self, row: int, col: int,
                grid: Dict[Tuple[int, int], Room]) -> None:
        def link(to_row: int, to_col: int):
            return grid.get((to_row, to_col), Doors.edge)

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

    def __str__(self) -> str:
        return f"[N({self.north.occupant}), " + \
               f"S({self.south.occupant}), " + \
               f"E({self.east.occupant}), " + \
               f"W({self.west.occupant})]"


class GameBuilder:
    """Create and manage the game"""
    def __init__(self, maze: str):
        """Use the 'Builder' pattern to build the
        object in multiple stages."""
        self.grid: Dict[Tuple[int, int], Room] = {}
        self.teleports: List[Room] = []
        # Stage 1: Build the grid
        for row, line in enumerate(maze.split("\n")):
            for col, char in enumerate(line):
                occupant: Item = item_factory(char)
                if isinstance(occupant, Robot):
                    room = Room(Empty())
                    self.robot = occupant
                    self.robot.room = room
                    self.grid[(row, col)] = room
                else:
                    self.grid[(row, col)] = Room(occupant)
                if isinstance(occupant, Teleport):
                    self.teleports.append(self.grid[(row, col)])
        # Stage 2: Connect the rooms
        for (row, col), room in self.grid.items():
            room.doors.connect(row, col, self.grid)
        # Stage 3: Connect the Teleport rooms
        self.teleports.sort(key=lambda teleport: teleport.occupant.target)
        it = iter(self.teleports)
        for room1, room2 in zip(it, it):
            room1.occupant.target_room = room2
            room2.occupant.target_room = room1

    def show_room(self, row: int, col: int) -> str:
        return f"({row}, {col}) " + \
               f"{self.grid.get((row, col), Room(Edge()))}"

    def __str__(self) -> str:
        return "\n".join(
            [self.show_room(row, col)
             for (row, col) in self.grid.keys()])

    def show_maze(self) -> str:
        result = ""
        current_row = 0
        for (row, col), room in self.grid.items():
            if row != current_row:
                result += "\n"
                current_row = row
            if room == self.robot.room:
                result += f"{self.robot}"
            else:
                result += f"{room.occupant}"
        return result

    def step(self, urge: Urge = None):
        """If called without urge, just display
        the current maze."""
        if urge:
            self.robot.move(urge)
        os.system(CLEAR)
        print(self.show_maze())
        sleep(0.3)

    def run(self, solution: str):
        match = {
            "n": Urge.North,
            "s": Urge.South,
            "e": Urge.East,
            "w": Urge.West
        }
        for urge_char in ''.join(solution.split()):
            self.step(match.get(urge_char))


string_maze = """
a_...#..._c
R_...#...__
###########
a_......._b
###########
!_c_....._b
""".strip()

solution = """
eeeenwwww
eeeeeeeeee
wwwwwwww
eeennnwwwwwsseeeeeen
ww
"""

if __name__ == '__main__':
    game = GameBuilder(string_maze)
    game.run(solution)
