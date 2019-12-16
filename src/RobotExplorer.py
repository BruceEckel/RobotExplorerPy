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
    def __init__(self):
        super().__init__('T')


class Empty(Item):
    def __init__(self):
        super().__init__(' ')


class Edge(Item):
    def __init__(self):
        super().__init__('_')


class EndGame(Item):
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


edge = Room(Edge)


class Doors:
    def __init__(self):
        self.north = edge
        self.south = edge
        self.east = edge
        self.west = edge

    def connect(self, row: Int, col: Int,
                grid: Map[Pair[Int, Int], Room ]):
        def link(to_row: Int, to_col: Int):
            return grid.getOrDefault((to_row, to_col), edge)
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
        return "[N(${north.occupant}), " + \
               "S(${south.occupant}), " + \
               "E(${east.occupant}), " + \
               "W(${west.occupant})]"


class Room:
    def __init__(self, occupant: Item = Empty):
        self.occupant = occupant
        self.doors = Doors()

    def enter(robot: Robot) -> Room:
        when(occupant):
        Empty -> return this  # Enter new room
        # Stay in original room:
        Wall, Edge, Mech -> return robot.room
        Food -> {
            print("Eat food")
        occupant = Empty
        return this
        }
        Teleport -> {
        print("Jump to target room")
        return Room(Teleport)
        }
        EndGame -> {
        print("End game")
        return Room(EndGame)


def __str__(self):
    return "Room($occupant) $doors"


class RoomBuilder:
    def __init__(self, maze: String):
        self.grid = mutableMapOf < Pair < Int, Int >, Room > ()

    def room(self, row: Int, col: Int):
        "($row, $col) " + \
        grid.getOrDefault(Pair(row, col), edge)


robot = Robot(edge)  # Nowhere


def build(self) -> RoomBuilder:
    # Stage 1: Create grid
    lines = maze.split("\n")
    lines.withIndex().forEach
    {(r, line) ->
    line.withIndex().forEach
    {(c, char) ->
    grid[Pair(r, c)] = createRoom(char)
    # Stage 2: Connect the rooms
    grid.forEach
    {(pair, r) ->
    r.doors.connect(pair.first, pair.second, grid)
    # Stage 3: Locate the robot
    robot.room = grid.values
    .find


{it.occupant == Mech}
?: robot.room
return self


def createRoom(self, c: Char) -> Room:
    Item.values().forEach
    {item ->
    if (item.symbol == c):
        return Room(item)
    return Room(Teleport)


def __str__(self):
    grid.map
    {"${it.key} ${it.value}"}.joinToString("\n")


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
