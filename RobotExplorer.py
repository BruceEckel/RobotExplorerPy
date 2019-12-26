# ObjectOrientedDesign/Essence.kt
from enum import Enum
from typing import List, Dict, Tuple
from time import sleep
from clear_screen import clear_screen


class Urge(Enum):
    North = 1
    South = 2
    East = 3
    West = 4


class Item:
    symbol = ''

    def interact(self, robot, room):
        pass

    def __str__(self) -> str:
        return self.symbol


class Robot(Item):
    """Robot knows where it is in the maze, but
    doesn't actually 'occupy' any room, it isn't an occupant.
    So it doesn't have to manage what's in the room -- interact() does that.
    When displaying the maze, the robot overlays its position."""
    symbol = 'R'

    def __init__(self):
        # Robot is a state machine:
        self.room = None

    def move(self, urge: Urge):
        # self.room.occupant = Empty()  # Leave old room
        # Get a reference to the Room you've been urged
        # to go to, and see what happens when we enter
        # that Room. Point robot to the returned Room:
        self.room = self.room.doors.open(urge).enter(self)
        # self.room.occupant = self  # Occupy new room


class Wall(Item):
    symbol = '#'

    def interact(self, robot: Robot, room):
        return robot.room  # Stay in original room


class Food(Item):
    symbol = '.'

    def interact(self, robot: Robot, room):
        print("Eat food")
        room.occupant = Empty()
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
    """The unknown void outside the maze"""
    symbol = '/'

    def interact(self, robot: Robot, room):
        return robot.room  # Stay in original room


class EndGame(Item):
    """The game is over"""
    symbol = '!'

    def interact(self, robot: Robot, room):
        return room


def item_factory(symbol: str):
    for item in Item.__subclasses__():
        if symbol == item.symbol:
            return item()
    return Teleport(symbol)


class Doors: pass


class Room:
    """Holds occupant, can be entered by Robot"""

    def __init__(self, occupant: Item = Empty()):
        self.occupant = occupant
        self.doors = Doors()

    def enter(self, robot: Robot):
        return self.occupant.interact(robot, self)

    def __repr__(self):
        return f"Room({self.occupant}) {self.doors}"


class Doors:
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


class RoomBuilder:
    def __init__(self, maze: str):
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
            # print(f"{room1} : {room2}")

    def room(self, row: int, col: int) -> str:
        return f"({row}, {col}) " + \
               f"{self.grid.get((row, col), Room(Edge()))}"

    def rooms(self) -> str:
        return "\n".join(
            [self.room(row, col)
             for (row, col) in self.grid.keys()])

    def maze(self) -> str:
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


string_maze = """
a_...#..._c
R_...#...__
###########
a_......._b
###########
!_c_....._b
""".strip()


if __name__ == '__main__':
    builder = RoomBuilder(string_maze)
    def show():
        clear_screen()
        print(builder.maze())
        sleep(1)
    # print(builder.room(0, 0))
    # print(builder.room(1, 6))
    # print(builder.room(5, 0))
    robot = builder.robot
    # print(robot)
    show()
    robot.move(Urge.East)
    show()
    robot.move(Urge.East)
    show()
    robot.move(Urge.South)
    show()
    # print(robot)

""" Output:
(0, 0) Room(T)[N(_), S(R), E(), W(_)]
(1, 6) Room(.) [N(.), S(  # ), E(.), W(#)]
(5, 0) Room(!) [N(  # ), S(_), E( ), W(_)]
Robot[N(T), S(  # ), E( ), W(_)]
Eat food
Robot[N(.), S(  # ), E(.), W( )]
"""
