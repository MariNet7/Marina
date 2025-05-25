import asyncio
from io import StringIO
import shlex
import cowsay


players = {}
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


class Player:
    def __init__(self, ochered):
        self.ochered = ochered
        self.coords = (0, 0)


def move(player, dx, dy):
    players[player].coords = ((players[player].coords[0] + dx) % 10, (players[player].coords[1] + dy) % 10)
    otvet = f"Moved to {players[player].coords[0]}, {players[player].coords[1]}"
    if game_map[players[player].coords[1]][players[player].coords[0]]:
        otvet += f"\n{encounter(game_map[players[player].coords[1]][players[player].coords[0]].name, game_map[players[player].coords[1]][players[player].coords[0]].meow)}"
    return otvet


def add_monster(player, name, x, y, hp, meow):
    otvet_vsem = f"{player} added monster {name} saying {meow} with {hp} hp"
    otvet = f"Added monster {name} to {x} {y} saying {meow} with {hp} hp"
    if game_map[y][x]:
        otvet += "\nReplaced the old monster"
        otvet_vsem += "\nReplaced the old monster"
    game_map[y][x] = Kitty(name, meow, hp)
    return otvet, otvet_vsem


def encounter(name, meow):
    if name in cowsay.list_cows():
        print(cowsay.cowsay(meow, cow = name))
    else:
        print(cowsay.cowsay(meow, cowfile=zluchki[name]))



def attack(player, name, uron):
    kitty = game_map[players[player].coords[1]][players[player].coords[0]]
    otvet_vsem = None

    if (not kitty) or (kitty.name != name):
        otvet = f'No {name} here'
    else:
        uron = min(uron, kitty.hp)
        kitty.hp -= uron
        otvet = f'attacked {name}, damage {uron}'
        otvet_vsem = f'{player} attacked {name}, damage {uron}'
        if kitty.hp == 0:
            game_map[players[player].coords[1]][players[player].coords[0]] = None
            otvet += f"\n{name} died"
            otvet_vsem += f"\n{name} died"
        else:
            otvet += f"\n{name} now has {kitty.hp} hp"
            otvet_vsem += f"\n{name} now has {kitty.hp} hp"

    return otvet, otvet_vsem


async def zapros(reader, writer):
    try:
        player = (await reader.readline()).decode().strip()
        if player in players:
            writer.write(b'busy_name\n')
            await writer.drain()
            writer.close()
            return

        writer.write(b'connected\n')
        await writer.drain()
        players[player] = Player(asyncio.Queue())

        soobsh_vsem = f'{player} connected.'
        for player_name in players:
            if player_name != player:
                await players[player_name].queue.put(soobsh_vsem)

        prochitano = asyncio.create_task(reader.readline())
        v_ocheredi = asyncio.create_task(players[player].queue.get())

        while not reader.at_eof():
            done, _ = await asyncio.wait(
                [prochitano, v_ocheredi],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                if task is prochitano:
                    args = task.result().decode().strip()
                    if not args:
                        continue

                    args = shlex.split(args)
                    otvet_vsem = ""

                    match args[0]:
                        case 'move':
                            dx, dy = map(int, args[1:3])
                            otvet = move(player, dx, dy)

                        case 'addmon':
                            name = args[1]
                            x = int(args[2])
                            y = int(args[3])
                            hp = int(args[4])
                            hello = ' '.join(args[5:])
                            otvet, otvet_vsem = add_monster(player, name, x, y, hp, hello)

                        case 'attack':
                            name = args[1]
                            damage = int(args[2])
                            otvet, otvet_vsem = attack(player, name, damage)

                        case _:
                            otvet = 'Invalid command'

                    if otvet_vsem:
                        for player_name in players:
                            if player_name != player:
                                await players[player_name].queue.put(otvet_vsem)
                            else:
                                await players[player_name].queue.put((otvet.replace('\n', '\\n') + '\n').encode())

                    prochitano = asyncio.create_task(reader.readline())

                elif task is v_ocheredi:
                    writer.write((task.result().replace('\n', '\\n') + '\n').encode())
                    await writer.drain()
                    v_ocheredi = asyncio.create_task(players[player].queue.get())

    finally:
        if player in players:
            del players[player]
            soobsh_vsem = f'{player} disconnected.'
            for player_name in players:
                await players[player_name].queue.put(soobsh_vsem)

        writer.write(b'server_busy\n')
        await writer.drain()
        writer.close()


async def main():
    server = await asyncio.start_server(zapros, 'localhost', 1111)
    async with server:
        await server.serve_forever()

asyncio.run(main())
