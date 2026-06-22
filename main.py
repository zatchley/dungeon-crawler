import sys
from constants import DUNGEON_MAX_SIZE
from player import Player
from dungeon import Dungeon, Room
from tutorial import tutorial_main

def main():
    #print("Hello from dungeon-crawler!")
    #start()
    player = Player()
    dungeon = Dungeon(player, [], 3)
    dungeon.gen_dungeon()

    player.in_dungeon = True

    print("Welcome to the dungeon\n\n")

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
    #dungeon = TRAINING_DUNGEON
    #tutorial_main()
    
    #dungeon.print_dungeon()


def start():
    print("[title splash]")
    print("\n\n")
    print("New Game")
    print("Load Game")
    print("Training")
    print("Quit")
    print("\n\n")

    selection = input()

    match selection:
        case "new" | "New" | "New Game":
            pass
        case "load" | "Load" | "Load Game":
            pass
        case "train" | "Train" | "Training":
            pass
        case "q" | "quit" | "Quit":
            sys.exit
        case _:
            print("unknown command")
    


if __name__ == "__main__":
    main()
