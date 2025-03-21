import asyncio


player_position = (0, 0)
game_map = [ (10 * [None]) for _ in range(10) ]


class Kitty:
    def __init__(self, name, meow, hp):
        self.meow = meow
        self.name = name
        self.hp = hp


def move(dx, dy):
    global player_position
    player_position = ((player_position[0] + dx) % 10, (player_position[1] + dy) % 10)
    otvet = f"{player_position[0]} {player_position[1]} "

    if game_map[player_position[1]][player_position[0]]:
        otvet += f"{game_map[player_position[1]][player_position[0]].name} {game_map[player_position[1]][player_position[0]].meow}"

    return otvet


def add_monster(name, x, y, hp, meow):
    if game_map[x][y]:
        return 'zamena'
    game_map[y][x] = Kitty(name, meow, hp)
    return


def attack(name, uron):
    kitty = game_map[player_position[1]][player_position[0]]

    if not kitty or (kitty.name != name):
        return
    else:
        uron = min(uron, kitty.hp)
        kitty.hp -= uron
        if kitty.hp == 0:
            game_map[player_position[1]][player_position[0]] = None
        return f'{uron} {kitty.hp}'


async def zapros(reader, writer):
    while args := await reader.readline():
        args = args.decode().strip().split()

        match args[0]:
            case "move":
                otvet = move(int(args[1]), int(args[2]))
            case "addmon":
                otvet = add_monster(args[1], int(args[2]), int(args[3]), int(args[4]), ' '.join(*args[5:]))
            case "attack":
                otvet = attack(args[1], int(args[2]))
            case _:
                continue

        writer.write((otvet + '\n').encode())
        await writer.drain()
    writer.close()


async def main():
    server = await asyncio.start_server(zapros, 'localhost', 1111)
    async with server:
        await server.serve_forever()

asyncio.run(main())