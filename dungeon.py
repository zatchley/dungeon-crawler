# Imports
import random
import time
from collections import defaultdict, deque
from constants import DUNGEON_MAX_SIZE

class Room():
    def __init__(self, doors: str, type: str, pos_x: int, pos_y: int):
        self.doors = doors
        self.type = type
        self.coordinates = (pos_x, pos_y)


class Dungeon():
    def __init__(self, rooms: dict[Room, list[Room]], size: int):
        self.rooms = rooms
        self.size = size

    def gen_dungeon(self):
        '''
        Generates a dungeon of the given size. The size is a tuple of 
        (width, height).
        '''
        print(f"\nGenerating dungeon of size: {self.size}x{self.size}")

        entrance = self.gen_entrance()
        print(f"\nEntrance generated at coordinates: {entrance.coordinates} with doors: {entrance.doors}")

        time_start = time.perf_counter()
        while len(self.rooms) < int(pow(self.size, 2) * 0.75):
            self.rooms = defaultdict(list)
            self.rooms[entrance] = []
            queue = deque([entrance])
            visited = set()
            visited.add(entrance.coordinates)
            self.generation_loop(queue, visited)
        
        time_end = time.perf_counter()
        print(f"\nGenerated dungeon with {len(self.rooms)} rooms in {time_end - time_start:.4f} seconds.\n")

    def generation_loop(self, queue: deque[Room], visited: set[tuple[int, int]]):
        '''
        A helper function for the dungeon generation process. It performs a 
        breadth-first search to generate rooms and connect them based on the 
        doors of the current room.
        '''
        while queue:
            current_room = queue.popleft()
            print(f"\nCurrent room: {current_room.coordinates} with doors: {current_room.doors}")
            for i in range(len(current_room.doors)):
                if current_room.doors[i] == "1":
                    next_coordinates = self.get_next_coordinates(
                        current_room.coordinates, i)
                    if (
                        next_coordinates[0] < 0 or 
                        next_coordinates[0] >= self.size or
                        next_coordinates[1] < 0 or 
                        next_coordinates[1] >= self.size
                    ):
                        if current_room.type != "entrance":
                            print("There shouldn't be a door here.")
                        continue
                    
                    print(f"\nNext coordinates: {next_coordinates}")
                    if next_coordinates not in visited:
                        next_room = self.gen_room(next_coordinates[0], 
                                                  next_coordinates[1])
                        self.rooms[current_room].append(next_room)
                        self.rooms[next_room].append(current_room)
                        queue.append(next_room)
                        visited.add(next_coordinates)
                    else:
                        print(f"There's already a room here.")

    def gen_entrance(self) -> Room:
        '''
        Generates an entrance for the dungeon. The entrance is a room with all 
        doors open and is placed on a random edge of the dungeon.
        '''
        entrance_side = random.randint(0, 3)

        # Entrance is on the north or south edge
        if entrance_side == 0 or entrance_side == 2:
            entrance_y = random.randint(0, self.size - 1)
            if entrance_side == 0 and entrance_y == 0:
                # North edge entrance at the northwest corner
                return Room("1110", "entrance", 0, entrance_y)
            elif entrance_side == 2 and entrance_y == 0:
                # South edge entrance at the southwest corner
                return Room("1110", "entrance", self.size - 1, entrance_y)
            elif entrance_side == 0 and entrance_y == self.size - 1:
                # North edge entrance at the northeast corner
                return Room("1011", "entrance", 0, entrance_y)
            elif entrance_side == 2 and entrance_y == self.size - 1:
                # South edge entrance at the southeast corner
                return Room("1011", "entrance", self.size - 1, entrance_y)
            else:
                return Room("1111", "entrance", self.size - 1, entrance_y)
        
        # Entrance is on the east or west edge
        if entrance_side == 1 or entrance_side == 3:
            entrance_x = random.randint(0, self.size - 1)
            if entrance_side == 1 and entrance_x == 0:
                # East edge entrance at the northeast corner
                return Room("0111", "entrance", entrance_x, 0)
            elif entrance_side == 3 and entrance_x == 0:
                # West edge entrance at the northwest corner
                return Room("0111", "entrance", entrance_x, self.size - 1)
            elif entrance_side == 1 and entrance_x == self.size - 1:
                # East edge entrance at the southeast corner
                return Room("1101", "entrance", entrance_x, 0)
            elif entrance_side == 3 and entrance_x == self.size - 1:
                # West edge entrance at the southwest corner
                return Room("1101", "entrance", entrance_x, self.size - 1)
            else:
                return Room("1111", "entrance", entrance_x, self.size - 1)
   
    def get_next_coordinates(self, coordinates: tuple[int, int], door: int) -> tuple[int, int]:
        '''
        Returns the coordinates of the neighboring room based on the current 
        coordinates and the door direction. The door is an integer from 0 to 3, 
        where 0 is north, 1 is east, 2 is south, and 3 is west.
        '''
        if door == 0:  # North
            return (coordinates[0] - 1, coordinates[1])
        elif door == 1:  # East
            return (coordinates[0], coordinates[1] + 1)
        elif door == 2:  # South
            return (coordinates[0] + 1, coordinates[1])
        elif door == 3:  # West
            return (coordinates[0], coordinates[1] - 1)

    def gen_room(self, pos_x: int, pos_y: int) -> Room:
        '''
        Generates a room at the given coordinates. The coordinates are a tuple 
        of (x, y).
        '''
        doors = f"{random.randint(0, 15):0{4}b}"
        print(f"Starting doors: {doors}")
        
        # Remove doors that lead outside the dungeon
        if pos_x == 0 and doors[0] == "1":
            print("Removing north door")
            doors = f"{(int(doors, 2) ^ int('1000', 2)):0{4}b}"
            print(f"New doors: {doors}")
        if pos_y == self.size - 1 and doors[1] == "1":
            print("Removing east door")
            doors = f"{(int(doors, 2) ^ int('0100', 2)):0{4}b}"
            print(f"New doors: {doors}")
        if pos_x == self.size - 1 and doors[2] == "1":
            print("Removing south door")
            doors = f"{(int(doors, 2) ^ int('0010', 2)):0{4}b}"
            print(f"New doors: {doors}")
        if pos_y == 0 and doors[3] == "1":
            print("Removing west door")
            doors = f"{(int(doors, 2) ^ int('0001', 2)):0{4}b}"
            print(f"New doors: {doors}")
        

        # Match doors with adjacent rooms
        for key in self.rooms:
            # Check north
            if pos_x > 0 and key.coordinates == (pos_x - 1, pos_y):
                print(f"Has north neighbor with doors: {key.doors}")
                if key.doors[2] != doors[0]:
                    print("Matching north door with neighbor's south door")
                    doors = f"{(int(doors, 2) ^ int('1000', 2)):0{4}b}"
                    print(f"New doors: {doors}")
                else:
                    print("North door already matches neighbor's south door")
            # Check east
            if pos_y < self.size - 1 and key.coordinates == (pos_x, pos_y + 1):
                print(f"Has east neighbor with doors: {key.doors}")
                if key.doors[3] != doors[1]:
                    print("Matching east door with neighbor's west door")
                    doors = f"{(int(doors, 2) ^ int('0100', 2)):0{4}b}"
                    print(f"New doors: {doors}")
                else:
                    print("East door already matches neighbor's west door")
            # Check south
            if pos_x < self.size - 1 and key.coordinates == (pos_x + 1, pos_y):
                print(f"Has south neighbor with doors: {key.doors}")
                if key.doors[0] != doors[2]:
                    print("Matching south door with neighbor's north door")
                    doors = f"{(int(doors, 2) ^ int('0010', 2)):0{4}b}"
                    print(f"New doors: {doors}")
                else:
                    print("South door already matches neighbor's north door")
            # Check west
            if pos_y > 0 and key.coordinates == (pos_x, pos_y - 1):
                print(f"Has west neighbor with doors: {key.doors}")
                if key.doors[1] != doors[3]:
                    print("Matching west door with neighbor's east door")
                    doors = f"{(int(doors, 2) ^ int('0001', 2)):0{4}b}"
                    print(f"New doors: {doors}")
                else:
                    print("West door already matches neighbor's east door")
        print(f"Generated room at coordinates: ({pos_x}, {pos_y}) with doors: {doors}")
        return Room(doors, "normal", pos_x, pos_y)

    def print_dungeon(self):
        '''
        Prints the dungeon to the console. The rooms are represented by their 
        type and the doors are represented by their binary value.
        '''
        print("Coordinates     |   Doors   |    Type    | Connections")
        print("----------------|-----------|------------|-----------------")
        for key in self.rooms:
            values = ", ".join([str(room.coordinates) for room in self.rooms[key]])
            print(f"{str(key.coordinates): <15} | {key.doors: ^9} | {key.type: <10} | {values}")