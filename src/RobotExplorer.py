# ObjectOrientedDesign/Essence.kt
from enum import Enum


class Item:
    def __init__(self, symbol: Char):
        self.symbol = symbol

    def __str__(self):
        return self.symbol


class Mech(Item):
    def __init__(self):
        super().__init__('R')


class Wall(Item):
    def __init__(self):
        super().__init__('#')


class Food(Item):
    def __init__(self):
        super().__init__('.')


class Teleport(Item):
    "Jump to the room with the same target"
    def __init__(self, target: Char):
        super().__init__(target)


class Empty(Item):
    "Room is there, but nothing in it"
    def __init__(self):
        super().__init__(' ')


class Edge(Item):
    "The unknown void outside the maze"
    def __init__(self):
        super().__init__('_')


class EndGame(Item):
    "The game is over"
    def __init__(self):
        super().__init__('!')


Enum('Urge', 'North South East West')


class Robot:
    def __init__(self, room: Room):
        self.room = room

    def turn(self, urge: Urge):
        # Get a reference to the Room you've
        # been urged to go to, and see what
        # happens when we enter the Room.
        # Point robot to returned Room:
        self.room = self.room.doors.open(urge).enter(this)

    def __str__(self):
        return "Robot ${room.doors}"


class Doors:
    def __init__(self):
        self.north = Room(Edge)
        self.south = Room(Edge)
        self.east = Room(Edge)
        self.west = Room(Edge)

    def connect(self, row: Int, col: Int,
                grid: Dict[Tuple[Int, Int], Room]):
        def link(to_row: Int, to_col: Int):
            return grid.get((to_row, to_col), Room(Edge))
        self.north = link(row - 1, col)
        self.south = link(row + 1, col)
        self.east = link(row, col + 1)
        self.west = link(row, col - 1)

    def open(self, urge: Urge) -> Room :
        # Pattern Match:
        return {
            Urge.North : north,
            Urge.South : south,
            Urge.East : east,
            Urge.West : west
        }.get(urge)

    def __str__(self):
        return  "[N(${self.north.occupant}), " + \
                "S(${self.south.occupant}), " + \
                "E(${self.east.occupant}), " + \
                "W(${self.west.occupant})]"


class Room:
    def __init__(self, occupant: Item = Empty()):
        self.occupant = occupant
        self.doors = Doors()

    def enter(robot: Robot) -> Room:
        "Is type-check coding SO bad?"
        if isinstance(occupant, Empty):
          return this  # Enter new room
        if isinstance(occupant, Mech) or isinstance(occupant, Wall) or isinstance(occupant, Edge):
            # Stay in original room:
            return robot.room
        if isinstance(self.occupant, Food):
            print("Eat food")
            self.occupant = Empty
            return this
        if isinstance(self.occupant, Teleport):
            print("Jump to target room")
            return Room(Teleport)
        if isinstance(self.occupant, EndGame):
            print("End game")
            return Room(EndGame)

    def __str__(self):
        return f"Room({occupant}) {doors}"


class RoomBuilder:
    def __init__(self, maze: String):
        self.grid: Dict[Tuple[Int, Int], Room] = {}
        self.robot = Robot(edge)  # Nowhere

    def room(self, row: Int, col: Int):
        f"({row}, {col}) " + grid.get((row, col), edge)

    def build(self) -> RoomBuilder:
        # Stage 1: Create grid
        lines = maze.split("\n")
        # lines.withIndex().forEach {(r, line) -> line.withIndex().forEach {(c, char) -> grid[Pair(r, c)] = createRoom(char)
        # Stage 2: Connect the rooms
        # grid.forEach{(pair, r) -> r.doors.connect(pair.first, pair.second, grid)
        # Stage 3: Locate the robot
        # robot.room = grid.values.find  {it.occupant == Mech}  ?: robot.room
        return self

    def createRoom(self, c: Char) -> Room:
        # Item.values().forEach
        # {item ->
        # if (item.symbol == c):
        #     return Room(item)
        return Room(Teleport)


    def __str__(self):
        """grid.map {"${it.key} ${it.value}"}.joinToString("\n")"""


stringMaze = """
a ...#... c
R ...#...
###########
a ....... b
###########
! c ..... b
""".trim()


def main():
    builder = RoomBuilder(stringMaze).build()
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
