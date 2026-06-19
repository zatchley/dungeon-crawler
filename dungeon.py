# Imports
import random
from constants import DUNGEON_MAX_SIZE

class Room():
    def __init__(self, doors: str, type: str, pos_x: int, pos_y: int):
        self.doors = doors
        self.type = type
        self.coordinates = (pos_x, pos_y)


class Dungeon():
    def __init__(self, rooms: list(list(Room)), size: tuple(int, int)):
        self.rooms = rooms
        self.size = size

    def gen_dungeon(self):
        '''
        Generates a dungeon of the given size. The size is a tuple of (width, height).
        '''
        #pass
        print(self.size)
        for i in range(self.size[0]):
            self.rooms.append([None] * self.size[1])

        self.gen_entrance()

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.rooms[i][j] is None:
                    self.rooms[i][j] = self.gen_room(i, j)

    def gen_entrance(self) -> None:
        '''
        Generates an entrance for the dungeon. The entrance is a room with all doors open and is placed on a random edge of the dungeon.
        '''
        entrance_side = random.randint(0, 3)

        # Entrance is on the north or south edge
        if entrance_side == 0 or entrance_side == 2:
            entrance_y = random.randint(0, self.size[0] - 1)
            if entrance_side == 0 and entrance_y == 0:
                # North edge entrance at the top-left corner
                self.rooms[0][entrance_y] = Room("1110", "entrance", 0, entrance_y)
            elif entrance_side == 2 and entrance_y == 0:
                # South edge entrance at the bottom-left corner
                self.rooms[self.size[0] - 1][entrance_y] = Room("1110", "entrance", self.size[0] - 1, entrance_y)
            elif entrance_side == 0 and entrance_y == self.size[0] - 1:
                # North edge entrance at the top-right corner
                self.rooms[0][entrance_y] = Room("1011", "entrance", 0, entrance_y)
            elif entrance_side == 2 and entrance_y == self.size[0] - 1:
                # South edge entrance at the bottom-right corner
                self.rooms[self.size[0] - 1][entrance_y] = Room("1011", "entrance", self.size[0] - 1, entrance_y)
            else:
                self.rooms[self.size[0] - 1][entrance_y] = Room("1111", "entrance", self.size[0] - 1, entrance_y)
        
        # Entrance is on the east or west edge
        if entrance_side == 1 or entrance_side == 3:
            entrance_x = random.randint(0, self.size[1] - 1)
            if entrance_side == 1 and entrance_x == 0:
                # West edge entrance at the top-left corner
                self.rooms[entrance_x][0] = Room("0111", "entrance", entrance_x, 0)
            elif entrance_side == 3 and entrance_x == 0:
                # East edge entrance at the top-right corner
                self.rooms[entrance_x][self.size[1] - 1] = Room("1101", "entrance", entrance_x, self.size[1] - 1)
            elif entrance_side == 1 and entrance_x == self.size[1] - 1:
                # West edge entrance at the bottom-left corner
                self.rooms[entrance_x][0] = Room("1101", "entrance", entrance_x, 0)
            elif entrance_side == 3 and entrance_x == self.size[1] - 1:
                # East edge entrance at the bottom-right corner
                self.rooms[entrance_x][self.size[1] - 1] = Room("0111", "entrance", entrance_x, self.size[1] - 1)
            else:
                self.rooms[entrance_x][self.size[1] - 1] = Room("1111", "entrance", entrance_x, self.size[1] - 1)   

    def gen_room(self, pos_x: int, pos_y: int) -> Room:
        '''
        Generates a room at the given coordinates. The coordinates are a tuple of (x, y).
        '''
        doors = f"{random.randint(0, 15):0{4}b}"
        
        # Remove doors that lead outside the dungeon
        if pos_x == 0 and doors[0] == "1":
            doors = f"{(int(doors, 2) ^ int('1000', 2)):0{4}b}"
        if pos_x == self.size[0] - 1 and doors[2] == "1":
            doors = f"{(int(doors, 2) ^ int('0010', 2)):0{4}b}"
        if pos_y == 0 and doors[3] == "1":
            doors = f"{(int(doors, 2) ^ int('0001', 2)):0{4}b}"
        if pos_y == self.size[1] - 1 and doors[1] == "1":
            doors = f"{(int(doors, 2) ^ int('0100', 2)):0{4}b}"

        # Match doors with adjacent rooms
        # North
        if pos_x > 0 and self.rooms[pos_x - 1][pos_y] is not None:
            if self.rooms[pos_x - 1][pos_y].doors[2] != doors[0]:
                doors = f"{(int(doors, 2) ^ int('1000', 2)):0{4}b}"
        # East
        if pos_y < self.size[1] - 1 and self.rooms[pos_x][pos_y + 1] is not None:
            if self.rooms[pos_x][pos_y + 1].doors[3] != doors[1]:
                doors = f"{(int(doors, 2) ^ int('0100', 2)):0{4}b}"
        # South
        if pos_x < self.size[0] - 1 and self.rooms[pos_x + 1][pos_y] is not None:
            if self.rooms[pos_x + 1][pos_y].doors[0] != doors[2]:
                doors = f"{(int(doors, 2) ^ int('0010', 2)):0{4}b}"
        # West
        if pos_y > 0 and self.rooms[pos_x][pos_y - 1] is not None:
            if self.rooms[pos_x][pos_y - 1].doors[1] != doors[3]:
                doors = f"{(int(doors, 2) ^ int('0001', 2)):0{4}b}"

        return Room(doors, "normal", pos_x, pos_y)

    def print_dungeon(self):
        '''
        Prints the dungeon to the console. The rooms are represented by their type and the doors are represented by their binary value.
        '''
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                print(f"{self.rooms[i][j].type: <8} ({self.rooms[i][j].doors: <4})", end=" | ")
            print()