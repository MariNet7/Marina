import sys
import cowsay

player_position = (0, 0)
game_map = [ (10 * [None]) for _ in range(10) ]


class Kitty:
    def __init__(self, meow):
        self.meow = meow


def move(direction):
    global player_position
    player_position = ((player_position[0] + direction[0]) % 10, (player_position[1] + direction[1]) % 10)
    print(f'Moved to ({player_position[0]}, {player_position[1]})')

    if game_map[player_position[1]][player_position[0]]:
        encounter()

    return player_position


def add_monster(location, meow):
    print(f'Added monster to ({location[0]}, {location[1]}) saying {meow}')

    if game_map[player_position[1]][player_position[0]]:
        print('Replaced the old monster')

    game_map[location[1]][location[0]] = Kitty(meow)


def encounter():
    print(cowsay.cowsay(game_map[player_position[1]][player_position[0]].meow))


def main():
    for user_input in sys.stdin:
        if not user_input.strip:
            continue

        args = user_input.strip().split()
        command = args[0]

        try:
             match command:
                case("up"):
                    move((0, -1))
                case("down"):
                    move((0, 1))
                case("right"):
                    move((1, 0))
                case("left"):
                    move((-1, 0))
                case("addmon"):
                    if len(args) != 4:
                        raise ValueError
                    add_monster((int(args[1]), int(args[2])), args[3])
                case _:
                    print("Invalid command")
        except:
            print('Invalid arguments')


if __name__ == "__main__":
    main()
