import shlex
import sys
import cowsay
from io import StringIO
import cmd


player_position = (0, 0)
game_map = [ (10 * [None]) for _ in range(10) ]
zluchki = {"jgsbat": cowsay.read_dot_cow(StringIO(r"""
    $the_cow = <<EOC;
             $thoughts
              $thoughts
        ,_                    _,
        ) '-._  ,_    _,  _.-' (
        )  _.-'.|\\\\--//|.'-._  (
         )'   .'\\/o\\/o\\/'.   `(
          ) .' . \\====/ . '. (
           )  / <<    >> \\  (
            '-._/`  `\\_.-'
      jgs     \\\\'--'//
             (((""  "")))
    EOC
    """))
}


class Kitty:
    def __init__(self, name, meow, hp):
        self.meow = meow
        self.name = name
        self.hp = hp


def move(direction):
    global player_position
    player_position = ((player_position[0] + direction[0]) % 10, (player_position[1] + direction[1]) % 10)
    print(f'Moved to ({player_position[0]}, {player_position[1]})')

    if game_map[player_position[1]][player_position[0]]:
        encounter()

    return player_position


def add_monster(name, location, meow, hp):
    if (name not in cowsay.list_cows()) and (name not in zluchki):
        print(f'Cannot add unknown monster')
        return

    print(f'Added monster {name} to ({location[0]}, {location[1]}) saying {meow} with {hp} hp')

    if game_map[player_position[1]][player_position[0]]:
        print('Replaced the old monster')

    game_map[location[1]][location[0]] = Kitty(name, meow, hp)


def encounter():
    kitty = game_map[player_position[1]][player_position[0]]

    if kitty.name in cowsay.list_cows():
        print(cowsay.cowsay(game_map[player_position[1]][player_position[0]].meow,
                        cow=cowsay.cowsay(game_map[player_position[1][player_position[0]]].name)))
    else:
        print(cowsay.cowsay(game_map[player_position[1]][player_position[0]].meow,
                            cowfile=zluchki[kitty.name]))


class MUD(cmd.Cmd):
    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = 'MUD>> '

    def do_up(self, args):
        move((0, -1))

    def do_down(self, args):
        move((0, 1))

    def do_left(self, args):
        move((-1, 0))

    def do_right(self, args):
        move((1, 0))

    def do_addmon(self, arg):
        try:
            args = shlex.split(arg.strip())

            if len(args) != 9:
                raise ValueError

            kitty_name = args[1]
            kitty_params = args[2:]

            hp = None
            meow = None
            coords = None
            i = 0
            while i < len(kitty_params):
                if kitty_params[i] == 'hello':
                    meow = kitty_params[i + 1]
                    i += 2
                elif kitty_params[i] == 'hp':
                    hp = int(kitty_params[i + 1])
                    i += 2
                elif kitty_params[i] == 'coords':
                    coords = (int(kitty_params[i + 1]), int(kitty_params[i + 2]))
                    i += 3
                else:
                    raise ValueError("Unknown parameter")

            if None in (meow, coords, hp):
                raise ValueError("Missing parameter")

            add_monster(kitty_name, coords, meow, hp)

        except Exception as e:
            print('Invalid arguments')


def main():
    MUD().cmdloop()

if __name__ == "__main__":
    main()