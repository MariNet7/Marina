import shlex
import asyncio
import cowsay
from io import StringIO
import cmd

urons = {'sword': 10, 'spear': 15, 'axe': 20}
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


def encounter(name, hello):
    if name in cowsay.list_cows():
        print(cowsay.cowsay(hello, cow = name))
    else:
        print(cowsay.cowsay(hello, cowfile=zluchki[name]))


def antichaos_addmon(args):
    hp = None
    meow = None
    coords = None
    kitty_name = None
    try:
        args = shlex.split(args.strip())

        if len(args) != 8:
            raise ValueError

        kitty_name = args[0]
        kitty_params = args[1:]

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

    except Exception as e:
        print('Invalid arguments')

    return kitty_name, coords, meow, hp


def antichaos_attack(args):
    args = shlex.split(args)
    if not (name := args[0]):
        print("Invalid argument")
        return

    if len(args) == 1:
        uron = urons['sword']
    elif args[1] == 'with':
        if args[2] not in urons:
            print("Unknown weapon")
            return
        uron = urons[args[2]]

    return name, uron


class MUD(cmd.Cmd):
    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = 'MUD>> '

    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.reader = None
        self.writer = None

    def preloop(self):
        self.loop.run_until_complete(self.init_gamer())

    async def init_gamer(self):
        self.reader, self.writer = await asyncio.open_connection('localhost', 1111)

    async def send(self, request):
        self.writer.write((request + '\n').encode())
        await self.writer.drain()
        reply = await self.reader.readline()
        return reply.decode().strip()


    def do_up(self, arg):
        self.loop.run_until_complete(self.move(0, -1))

    def do_down(self, arg):
        self.loop.run_until_complete(self.move(0, 1))

    def do_left(self, arg):
        self.loop.run_until_complete(self.move(-1, 0))

    def do_right(self, arg):
        self.loop.run_until_complete(self.move(1, 0))

    async def move(self, dx, dy):
        otvet = await self.send(f"move {dx} {dy}")
        x, y, *kitty = shlex.split(otvet)
        print(f'Moved to ({x}, {y})')
        if kitty:
            name, *meows = kitty
            meow = ' '.join(meows)
            encounter(name, meow)

    def do_addmon(self, arg):
        name, coords, meow, hp  = antichaos_addmon(arg)
        if (name not in cowsay.list_cows()) and (name not in zluchki):
            print('Cannot add unknown monster')
            return
        self.loop.run_until_complete(self._add_monster(name, meow, hp, coords))

    async def _add_monster(self, name, meow, hp, coords):
        otvet = await self.send(f"addmon {name} {coords[0]} {coords[1]} {hp} {meow}")
        print(f'Added monster {name} to ({coords[0]}, {coords[1]}) saying {meow}')
        if otvet == 'zamena':
            print('Replaced the old monster')

    def complete_addmon(self, text):
        kitties = cowsay.list_cows() + list(zluchki.keys())
        if len(kitties) < 3:
            return [name for name in kitties if name.startswith(text)]
        else:
            return [name for name in ['coords', 'meow', 'hp'] if name.startswith(text)]

    def do_attack(self, arg):
        name, uron = antichaos_attack(arg)
        self.loop.run_until_complete(self.attack(name, uron))

    async def attack(self, name, uron):
        otvet = await self.send(f"attack {name} {uron}")
        if otvet:
            uron, hp = otvet.split(' ', 1)
            print(f'Attacked {name},  damage {uron} hp')
            if hp == '0':
                print(f'{name} died')
            else:
                print(f'{name} now has {hp}')
        else:
            print(f'No {name} here')

    def complete_attack(self, line, text):
        kitties = cowsay.list_cows() + list(zluchki.keys())
        if len(line.split()) == 2:
            return [name for name in kitties if name.startswith(text)]
        elif len(line.split()) == 3:
            return ['with']
        else:
            return [name for name in list(urons.keys()) if name.startswith(text)]


def main():
    MUD().cmdloop()

if __name__ == "__main__":
    main()