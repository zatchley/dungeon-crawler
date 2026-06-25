import sys
import time
from constants import DUNGEON_MAX_SIZE
from player import Player
from dungeon import Dungeon, Room
from tutorial import tutorial_main

def main():
    start()

def start():
    print("[title splash]")
    print("\n")
    print("New Game    <-- COMING SOON")
    print("Load Game   <-- COMING SOON")
    print("Training")
    print("Quit")   
    print("\n")

    while True:
        selection = input("\n>:")

        match selection:
            case "new" | "New" | "New Game":
                print_slow("\nThis option is not available yet.")
            case "load" | "Load" | "Load Game":
                print_slow("\nThis option is not available yet.")
            case "train" | "Train" | "training" | "Training":
                tutorial_main()
            case "q" | "quit" | "Quit":
                sys.exit()
            case _:
                print_slow("\nunknown command")
    
def print_slow(message):
    for letter in message:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.07)
    time.sleep(0.5)
    print()


if __name__ == "__main__":
    main()
