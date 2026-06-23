# Imports
import random
import time
from collections import defaultdict, deque
from player import Player
#from constants import DUNGEON_MAX_SIZE

class Room():
    def __init__(self, pos_x: int, pos_y: int, doors: str, type: str, visited: bool):
        self.coordinates = (pos_x, pos_y)
        self.doors = doors
        self.type = type
        self.visited = visited

    def get_description(self):
        # TODO: Make unique descriptions for each type of room

        directions = ["north", "east", "south", "west"]
        open_doors = []
        for i in len(self.doors):
            if self.doors[i] == "1":
                open_doors.append(directions[i])
        if len(open_doors) == 1:
            print(f"A door leads to the {open_doors[0]}.")
        elif len(open_doors) == 2:
            print(f"Doors lead to the {open_doors[0]} and {open_doors[1]}.")
        elif len(open_doors) == 3:
            print(f"Doors lead to the {open_doors[0]}, {open_doors[1]}, and {open_doors[2]}.")
        else:
            print(f"Doors lead in all directions.")

class Dungeon():
    def __init__(self, player: Player, rooms: dict[Room, list[Room]], size: int):
        self.player = player
        self.rooms = rooms
        self.size = size
        self.player_pos = (0, 0)
        self.commands = {
                            "map": self.map,
                            "move": self.move
                        }

    def gen_dungeon(self, rooms: list[Room] | None) -> None:
        '''
        Generates a dungeon of the given size. The size is a tuple of 
        (width, height).
        '''
        print(f"\nGenerating dungeon of size: {self.size}x{self.size}")
        min_rooms = int(pow(self.size, 2) * 0.75)

        time_start = time.perf_counter()
        while len(self.rooms) < min_rooms:
            if rooms == None:
                entrance = self.gen_entrance()
            else:
                entrance = [room for room in rooms if room.type == "entrance"][0]
            self.set_player_start(entrance)
            print(f"\nEntrance generated at coordinates: {entrance.coordinates} with doors: {entrance.doors}")

            self.rooms = defaultdict(list)
            self.rooms[entrance] = [None, None, None, None]
            queue = deque([entrance])
            visited = set()
            visited.add(entrance.coordinates)
            self.generation_loop(rooms, queue, visited)
            if len(self.rooms) < min_rooms:
                print(f"\nGenerated dungeon with only {len(self.rooms)} rooms. Regenerating...")
                print("-" * 50)
        
        time_end = time.perf_counter()
        print(f"\nGenerated dungeon with {len(self.rooms)} rooms in {time_end - time_start:.4f} seconds.\n")

    def generation_loop(self, rooms: list[Room], queue: deque[Room], visited: set[tuple[int, int]]):
        '''
        A helper function for the dungeon generation process. It performs a 
        breadth-first search to generate rooms and connect them based on the 
        doors of the current room.
        '''
        while queue:
            current_room = queue.popleft()
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
                    
                    print(f"\nGenerating room at {next_coordinates}")
                    if next_coordinates not in visited:
                        if rooms == None:
                            next_room = self.gen_room(next_coordinates[0], 
                                                    next_coordinates[1])
                        else:
                            next_room = [room for room in rooms if room.coordinates == next_coordinates][0]
                        self.rooms[current_room][i] = next_room
                        self.rooms[next_room] = [None, None, None, None]
                        self.rooms[next_room][(i + 2) % 4] = current_room
                        queue.append(next_room)
                        visited.add(next_coordinates)
                    else:
                        print(f"There's already a room here.")

    def gen_entrance(self) -> Room:
        '''
        Generates an entrance for the dungeon. The entrance is placed on a 
        random edge of the dungeon.
        '''
        doors = f"{random.randint(0, 15):0{4}b}"
        doors_list = []
        for i in doors:
            doors_list.append(i)

        entrance_side = random.randint(0, 3)
        doors_list[entrance_side] = "1"

        # Entrance is on the north or south edge
        if entrance_side == 0 or entrance_side == 2:
            if entrance_side == 0:
                entrance_x = 0
            else:
                entrance_x = self.size - 1
            entrance_y = random.randint(0, self.size - 1)

            if entrance_y == self.size - 1:
                # Entrance is in the east corner
                doors_list[1] = "0"
            elif entrance_y == 0:
                # Entrance is in the west corner
                doors_list[3] = "0"
        
        # Entrance is on the east or west edge
        if entrance_side == 1 or entrance_side == 3:
            if entrance_side == 1:
                entrance_y = self.size - 1
            else:
                entrance_y = 0
            entrance_x = random.randint(0, self.size - 1)

            if entrance_x == 0:
                # Entrance is in the north corner
                doors_list[0] = "0"
            elif entrance_x == self.size - 1:
                # Entrance is in the south corner
                doors_list[2] = "0"
        
        doors = "".join(doors_list)
        return Room(entrance_x, entrance_y, doors, "entrance", True)

    def gen_room(self, pos_x: int, pos_y: int) -> Room:
        '''
        Generates a room at the given coordinates. The coordinates are a tuple 
        of (x, y).
        '''
        doors = f"{random.randint(0, 15):0{4}b}"
        doors_list = []
        for i in doors:
            doors_list.append(i)
        print(f"Starting doors: {doors}")
        
        # Remove doors that lead outside the dungeon
        if pos_x == 0 and doors_list[0] == "1":
            print("Removing north door")
            doors_list[0] = "0"
        if pos_y == self.size - 1 and doors_list[1] == "1":
            print("Removing east door")
            doors_list[1] = "0"
        if pos_x == self.size - 1 and doors_list[2] == "1":
            print("Removing south door")
            doors_list[2] = "0"
        if pos_y == 0 and doors_list[3] == "1":
            print("Removing west door")
            doors_list[3] = "0"

        # Match doors with adjacent rooms
        for room in self.rooms:
            # Check north
            if pos_x > 0 and room.coordinates == (pos_x - 1, pos_y):
                print(f"Has north neighbor with doors: {room.doors}")
                if room.doors[2] != doors_list[0]:
                    print("Matching north door with neighbor's south door")
                    doors_list[0] = room.doors[2]
                else:
                    print("North door already matches neighbor's south door")
            # Check east
            if pos_y < self.size - 1 and room.coordinates == (pos_x, pos_y + 1):
                print(f"Has east neighbor with doors: {room.doors}")
                if room.doors[3] != doors_list[1]:
                    print("Matching east door with neighbor's west door")
                    doors_list[1] = room.doors[3]
                else:
                    print("East door already matches neighbor's west door")
            # Check south
            if pos_x < self.size - 1 and room.coordinates == (pos_x + 1, pos_y):
                print(f"Has south neighbor with doors: {room.doors}")
                if room.doors[0] != doors_list[2]:
                    print("Matching south door with neighbor's north door")
                    doors_list[2] = room.doors[0]
                else:
                    print("South door already matches neighbor's north door")
            # Check west
            if pos_y > 0 and room.coordinates == (pos_x, pos_y - 1):
                print(f"Has west neighbor with doors: {room.doors}")
                if room.doors[1] != doors_list[3]:
                    print("Matching west door with neighbor's east door")
                    doors_list[3] = room.doors[1]
                else:
                    print("West door already matches neighbor's east door")
        
        doors = "".join(doors_list)
        print(f"Generated room at coordinates: ({pos_x}, {pos_y}) with doors: {doors}")
        return Room(pos_x, pos_y, doors, "empty", False)

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

    def set_player_start(self, entrance: Room) -> None:
        self.player_pos = entrance.coordinates

    def print_dungeon(self) -> None:
        '''
        Prints the dungeon to the console. The dungeon is represented as a grid 
        of rooms, where each room is represented by a 4x9 block of characters. 
        The doors of the rooms are represented by spaces in the appropriate 
        locations. The walls of the rooms are represented by dashes and pipes. 
        The corners of the rooms are represented by pluses. The size of the grid 
        is determined by the size of the dungeon, and the rooms are placed 
        according to their coordinates.
        '''
        num_rows = self.size * 4 + 1
        num_cols = self.size * 10 + 1
        for i in range(num_rows):
            for j in range(num_cols):
                if (i % 4 == 0 and j % 10 == 0):
                        print("+", end="")
                        continue
                room_x = i // 4
                room_y = j // 10
                if (room_x, room_y) in [room.coordinates for room in self.rooms]:
                    room = [room for room in self.rooms if room.coordinates == (room_x, room_y)][0]
                    if i % 4 == 0:
                        room_n = self.rooms[room][0] if self.rooms[room][0] else None
                        if ((room.visited or (room_n and room_n.visited)) and 
                            room.doors[0] == "1" and
                            (i > 0 or room.type == "entrance") and 
                            j % 10 > 2 and j % 10 < 8):
                            print(" ", end="")
                        else:
                            print("-", end="")
                    elif j % 10 == 0:
                        room_w = self.rooms[room][3] if self.rooms[room][3] else None
                        if ((room.visited or (room_w and room_w.visited)) and 
                            room.doors[3] == "1" and
                            i % 4 == 2 and 
                            (j > 0 or room.type == "entrance")):
                            print(" ", end="")
                        else:
                            print("|", end="")
                    elif (i % 4 == 2 and j % 10 == 5 and 
                          room.coordinates == self.player_pos):
                        print("X", end="")
                    elif room.visited:
                        print(" ", end="")
                    else:
                        print("-", end="")
                else:
                    room_x = (i - 1) // 4
                    room_y = j // 10
                    if (room_x, room_y) in [room.coordinates for room in self.rooms]:
                        room = [room for room in self.rooms if room.coordinates == (room_x, room_y)][0]
                        if (room.type == "entrance" and 
                            room.doors[2] == "1" and 
                            j % 10 > 2 and j % 10 < 8):
                            print(" ", end="")
                            continue
                        else:
                            print("-", end="")
                            continue

                    room_x = i // 4
                    room_y = (j - 1) // 10
                    if (room_x, room_y) in [room.coordinates for room in self.rooms]:
                        room = [room for room in self.rooms if room.coordinates == (room_x, room_y)][0]
                        if (room.type == "entrance" and 
                            room.doors[1] == "1" and 
                            i % 4 == 2):
                            print(" ", end="")
                            continue
                        else:
                            print("|", end="")
                            continue

                    if i == 0 or i == num_rows - 1:
                        print("-", end="")
                    elif j == 0 or j == num_cols - 1:
                        print("|", end="")
                    else:
                        print("-", end="")
            print()

    def map(self, arg: None) -> None:
        self.print_dungeon()

    def move(self, direction: str | None) -> None:
        if direction == None:
            print("Move where?")
            return
        else:
            if direction == "n":
                direction = "north"
            elif direction == "e":
                direction = "east"
            elif direction == "s":
                direction = "south"
            elif direction == "w":
                direction = "west"
            
        if (direction != "north" and direction != "east" and
            direction != "south" and direction != "west"):
            print(f"'{direction}' is not a direction.")
            return

        current_room = [room for room in self.rooms if self.player_pos == room.coordinates][0]
        if direction == "north" and current_room.doors[0] == "1":
            self.player_pos = (self.player_pos[0] - 1, self.player_pos[1])
            new_room = self.rooms[current_room][0]
        elif direction == "east" and current_room.doors[1] == "1":
            self.player_pos = (self.player_pos[0], self.player_pos[1] + 1)
            new_room = self.rooms[current_room][1]
        elif direction == "south" and current_room.doors[2] == "1":
            self.player_pos = (self.player_pos[0] + 1, self.player_pos[1])
            new_room = self.rooms[current_room][2]
        elif direction == "west" and current_room.doors[3] == "1":
            self.player_pos = (self.player_pos[0], self.player_pos[1] - 1)
            new_room = self.rooms[current_room][3]
        else:
            print("A wall blocks your path.")
            return
        
        new_room.visited = True
        print(f"You walk through the {direction}ern door.")
        return
        
        