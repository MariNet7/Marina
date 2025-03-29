import shlex
import asyncio
import cowsay
from io import StringIO
import cmd
import sys
import readline
import threading


urons = {'sword': 10, 'spear': 15, 'axe': 20}
zluchki = ["jgsbat"]


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
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.gamer = sys.argv[1]
        self.lloop = None
        self.lochered = None
        self.stop = None

    def postcmd(self, stop, line):
        if self.stop.is_set():
            return True
        return super().postcmd(stop, line)

    def send(self, vvod):
        if self.lloop and self.lochered:
            self.lloop.call_soon_threadsafe(self.lochered.put_nowait, vvod)
        else:
            exit(0)

    def do_up(self, arg):
        self.move(0, -1)

    def do_down(self, arg):
        self.move(0, 1)

    def do_left(self, arg):
        self.move(-1, 0)

    def do_right(self, arg):
        self.move(1, 0)

    async def move(self, dx, dy):
        self.send(f"move {dx} {dy}")

    def do_addmon(self, arg):
        name, (x, y), meow, hp  = antichaos_addmon(arg)
        if (name not in cowsay.list_cows()) and (name not in zluchki):
            print('Cannot add unknown monster')
            return
        self.send(f"addmon {name} {x} {y} {hp} {meow}")

    def complete_addmon(self, text):
        kitties = cowsay.list_cows() + zluchki
        if len(kitties) < 3:
            return [name for name in kitties if name.startswith(text)]
        else:
            return [name for name in ['coords', 'meow', 'hp'] if name.startswith(text)]

    def do_attack(self, arg):
        name, uron = antichaos_attack(arg)
        self.send(f"attack {name}, {uron}")

    def complete_attack(self, line, text):
        kitties = cowsay.list_cows() + zluchki
        if len(line.split()) == 2:
            return [name for name in kitties if name.startswith(text)]
        elif len(line.split()) == 3:
            return ['with']
        else:
            return [name for name in list(urons.keys()) if name.startswith(text)]

async def local_server(game):
    try:
        reader, writer = await asyncio.open_connection('localhost', 1111)
    except Exception:
        game.stop.set()
        print('Server is busy')
        exit(0)

    writer.write(f'{sys.argv[1]}\n'.encode())
    otvet = (await reader.readline()).decode().strip()

    if otvet == 'busy_name':
        game.stop.set()
        print('Username is already taken!')
        writer.close()
        await writer.wait_closed()
        exit(0)

    otpravleno = asyncio.create_task(game.local_srv_queue.get())
    polucheno = asyncio.create_task(reader.readline())

    try:
        while True:
            sdelano, _ = await asyncio.wait(
                [otpravleno, polucheno],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in sdelano:
                if task is otpravleno:
                    data = task.result()
                    writer.write(f"{data}\n".encode())
                    await writer.drain()
                    otpravleno = asyncio.create_task(game.local_srv_queue.get())

                elif task is polucheno:
                    otvet = task.result().decode().strip()
                    if otvet == 'server_busy':
                        game.stop.set()
                        print('server is unavailable!')
                        raise Exception('server is unavailable')

                    print(f'\n{otvet.replace('\\n', '\n')}\n{game.prompt}{readline.get_line_buffer()}', end='',
                          flush=True)
                    polucheno = asyncio.create_task(reader.readline())

    except Exception as e:
        if e.args[0] != 'server is busy':
            print(e)
    finally:
        otpravleno.cancel()
        polucheno.cancel()
        writer.close()
        await writer.wait_closed()


def play_game(game):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    game.lochered = asyncio.Queue()
    game.lloop = loop
    game.stop = threading.Event()
    loop.run_until_complete(local_server(game))


def main():
    if len(sys.argv) < 2:
        print('Input Username')
        return
    game = MUD()
    threading.Thread(target=play_game, args=(game,)).start()
    MUD().cmdloop()

if __name__ == "__main__":
    main()