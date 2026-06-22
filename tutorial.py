from dungeon import Dungeon, Room
from player import Player

def tutorial_main():
    player = Player()
    dungeon = Dungeon(player, [], 3)
    rooms = [Room(2, 1, "0111", "entrance", True), 
             Room(2, 2, "1001", "normal", False),
             Room(2, 0, "1100", "normal", False),
             Room(1, 2, "1010", "normal", False),
             Room(1, 0, "0110", "normal", False),
             Room(0, 2, "0011", "normal", False),
             Room(1, 1, "1001", "normal", False),
             Room(0, 1, "0111", "normal", False),
             Room(0, 0, "0100", "normal", False)]
    

    dungeon.player_pos = (2, 1)
    player.in_dungeon = True

    print("Welcome to the training dungeon\n\n")

    while True:
        command = input(">:")
        if player.in_dungeon:
            location = dungeon
        cmd_parser(command, location)

def cmd_parser(command: str, location) -> None:
        cmd_parts = command.split(" ")
        verb = cmd_parts[0].lower()
        if len(cmd_parts) > 1:
            noun = cmd_parts[1:]
            for word in noun:
                word.lower()
            if len(noun) > 1:
                noun = noun.join(" ")
            else:
                noun = noun[0]
        else: 
            noun = None

        if verb in location.commands:
            location.commands[verb](noun)