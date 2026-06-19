import sys

def main():
    print("Hello from dungeon-crawler!")
    start()


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
