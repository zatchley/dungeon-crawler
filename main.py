import sys
from constants import DUNGEON_MAX_SIZE, TRAINING_DUNGEON
from dungeon import Dungeon, Room

def main():
    print("Hello from dungeon-crawler!")
    #start()
    dungeon = Dungeon([], DUNGEON_MAX_SIZE)
    dungeon.gen_dungeon()
    #dungeon = TRAINING_DUNGEON
    
    dungeon.print_dungeon()


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
