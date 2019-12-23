# ObjectOrientedDesign/Essence.kt
from enum import Enum
from typing import List, Dict, Tuple

class Urge(Enum):
    North = 1
    South = 2
    East = 3
    West = 4


class Robot:
    def __init__(self, room):
        self.room = room

    def move(self, urge: Urge):
        # Get a reference to the Room you've been urged
        # to go to, and see what happens when we enter
        # that Room. Point robot to the returned Room:
        self.room = self.room.doors.open(urge).enter(self)

    def __str__(self) -> str:
        return f"Robot {self.room.doors}"


class Item:
    symbol = ''

    def interact(self, robot, room):
        pass

    def __str__(self) -> str:
        return self.symbol


class Mech(Item):
    symbol = 'R'

    def interact(self, robot: Robot, room):
        return robot.room  # Stay in original room


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
        self.robot = Robot(Room(Edge()))  # Nowhere
        self.teleports: List[Room] = []
        # Stage 1: Build the grid
        for row, line in enumerate(maze.split("\n")):
            for col, char in enumerate(line):
                room: Room = Room(item_factory(char))
                self.grid[(row, col)] = room
                # NOT type-check coding:
                if isinstance(room.occupant, Teleport):
                    self.teleports.append(room)
        # Stage 2: Connect the rooms
        for (row, col), room in self.grid.items():
            room.doors.connect(row, col, self.grid)
        # Stage 3: Connect the Teleport rooms
        self.teleports.sort(key=lambda teleport: teleport.occupant.target)
        it = iter(self.teleports)
        for room1, room2 in zip(it, it):
            room1.occupant.target_room = room2
            room2.occupant.target_room = room1
            print(f"{room1} : {room2}")
        # Stage 4: Locate the robot
        for room in self.grid.values():
            if isinstance(room.occupant, Mech):
                self.robot.room = room
                return

    def room(self, row: int, col: int) -> str:
        return f"({row}, {col}) " + \
               f"{self.grid.get((row, col), Room(Edge()))}"

    def rooms(self) -> str:
        return "\n".join(
            [self.room(row, col)
             for (row, col) in self.grid.keys()])

    def __str__(self) -> str:
        result = ""
        current_row = 0
        for (row, col), room in self.grid.items():
            if row != current_row:
                result += "\n"
                current_row = row
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
    # print(builder.rooms())
    # print(builder)
    # print(builder.room(0, 0))
    # print(builder.room(1, 6))
    # print(builder.room(5, 0))
    # robot = builder.robot
    # print(robot)
    # robot.move(Urge.East)
    # robot.move(Urge.East)
    # robot.move(Urge.South)
    # print(robot)

""" Output:
(0, 0) Room(T)[N(_), S(R), E(), W(_)]
(1, 6) Room(.) [N(.), S(  # ), E(.), W(#)]
(5, 0) Room(!) [N(  # ), S(_), E( ), W(_)]
Robot[N(T), S(  # ), E( ), W(_)]
Eat food
Robot[N(.), S(  # ), E(.), W( )]
"""
