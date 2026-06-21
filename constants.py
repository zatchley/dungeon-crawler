from dungeon import Room, Dungeon


DUNGEON_MAX_SIZE = 5
TRAINING_DUNGEON = Dungeon({Room("0111", "entrance", 2, 1, False): [None, Room("1001", "normal", 2, 2, False), None, Room("1100", "normal", 2, 0, False)],
                            Room("1001", "normal", 2, 2, False): [Room("1010", "normal", 1, 2, False), None, None, Room("0111", "entrance", 2, 1, False)],
                            Room("1100", "normal", 2, 0, False): [Room("0110", "normal", 1, 0, False), Room("0111", "entrance", 2, 1, False), None, None],
                            Room("1010", "normal", 1, 2, False): [Room("0011", "normal", 0, 2, False), None, Room("1001", "normal", 2, 2, False), None],
                            Room("0110", "normal", 1, 0, False): [None, Room("1001", "normal", 1, 1, False), Room("1100", "normal", 2, 0, False), None],
                            Room("0011", "normal", 0, 2, False): [None, None,Room("1010", "normal", 1, 2, False), Room("0111", "normal", 0, 1, False)],
                            Room("1001", "normal", 1, 1, False): [Room("0111", "normal", 0, 1, False), None, None, Room("0110", "normal", 1, 0, False)],
                            Room("0111", "normal", 0, 1, False): [None, Room("0011", "normal", 0, 2, False), Room("1001", "normal", 1, 1, False), Room("0100", "normal", 0, 0, False)],
                            Room("0100", "normal", 0, 0, False): [None, Room("0111", "normal", 0, 1, False), None, None]
                            }, 3)