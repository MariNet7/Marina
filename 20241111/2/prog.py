class Triangle:
    def __init__(self, t1, t2, t3):
        self.vershini = [t1, t2, t3]

    def __abs__(self):
        x1, y1 = self.vershini[0]
        x2, y2 = self.vershini[1]
        x3, y3 = self.vershini[2]
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)

    def __bool__(self):
        return self.__abs__() > 0

    def __lt__(self, other):
        return abs(self) < abs(other)

    def contains(self, tochka):
        x, y = tochka
        x1, y1 = self.vershini[0]
        x2, y2 = self.vershini[1]
        x3, y3 = self.vershini[2]

        ploshad = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)
        pl1 = abs((x * (y2 - y3) + x2 * (y3 - y) + x3 * (y - y2)) / 2)
        pl2 = abs((x1 * (y - y3) + x * (y3 - y1) + x3 * (y1 - y)) / 2)
        pl3 = abs((x1 * (y2 - y) + x2 * (y - y1) + x * (y1 - y2)) / 2)

        return ploshad == pl1 + pl2 + pl3

    def __contains__(self, other):
        if isinstance(other, Triangle):
            return all(self.contains(tochka) for tochka in other.vershini)
        return False

    def intersects(self, other):
        if abs(self) == 0 or abs(other) == 0:
            return False

        def peresech(t1, t2, q1, q2):
            def ccw(a, b, c):
                return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
            return ccw(t1, q1, q2) != ccw(t2, q1, q2) and ccw(t1, t2, q1) != ccw(t1, t2, q2)

        for i in range(3):
            for j in range(3):
                if peresech(self.vershini[i], self.vershini[(i + 1) % 3], other.vershini[j], other.vershini[(j + 1) % 3]):
                    return True
        return False

    def __and__(self, other):
        return self.intersects(other)

r = Triangle((4, 2), (1, 3), (2, 4))
s = Triangle((1, 1), (3, 1), (2, 2))
t = Triangle((0, 0), (2, 3), (4, 0))
o = Triangle((1, 1), (2, 2), (3, 3))

print(*(f"{n}({bool(x)}):{round(abs(x), 3)}" for n, x in zip("rsto", (r, s, t, o))))
print(f"{s < t=}, {o < t=}, {r < t=}, {r < s=}")
print(f"{s in t=}, {o in t=}, {r in t=}")
print(f"{r & t=}, {t & r=}, {s & r=}, {o & t=}")
