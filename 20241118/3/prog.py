class Undead(Exception):
    pass
class Skeleton(Undead):
    pass
class Zombie(Undead):
    pass
class Ghoul(Undead):
    pass

def necro(a):
    match a % 3:
        case 0:
            raise Skeleton()
        case 1:
            raise Zombie()
        case 2:
            raise Ghoul()

for stroka in range(*eval(input())):
    try:
        necro(stroka)
    except Skeleton:
        print("Skeleton")
    except Zombie:
        print("Zombie")
    except Undead:
        print("Generic Undead")