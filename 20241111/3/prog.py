class Maze:
    def __init__(self, size):
        self.size = size
        self.grid = [['█' for _ in range(size * 2 + 1)] for _ in range(size * 2 + 1)]
        for row in range(1, size * 2, 2):
            for col in range(1, size * 2, 2):
                self.grid[row][col] = '·'

    def __str__(self):
        return '\n'.join(''.join(line) for line in self.grid)

    def __getitem__(self, key):
        start_x, start_y, end_x, end_y = self._extract_coordinates(key)
        return self._can_reach(start_x, start_y, end_x, end_y)

    def __setitem__(self, key, value):
        start_x, start_y, end_x, end_y = self._extract_coordinates(key)
        if value == '·':
            self._create_passage(start_x, start_y, end_x, end_y)
        elif value == '█':
            self._block_passage(start_x, start_y, end_x, end_y)

    def _extract_coordinates(self, key):
        x_start, y_start_end = key
        y_start, x_end = y_start_end.start, y_start_end.stop
        return min(x_start, x_end), min(y_start, y_end), max(x_start, x_end), max(y_start, y_end)

    def _can_reach(self, start_x, start_y, end_x, end_y):
        if not (0 <= start_x < self.size and 0 <= start_y < self.size and 0 <= end_x < self.size and 0 <= end_y < self.size):
            return False

        from collections import deque

        queue = deque([(start_x, start_y)])
        visited = set((start_x, start_y))

        while queue:
            current_x, current_y = queue.popleft()
            if (current_x, current_y) == (end_x, end_y):
                return True

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_x, next_y = current_x + dx, current_y + dy
                if 0 <= next_x < self.size and 0 <= next_y < self.size and (next_x, next_y) not in visited:
                    if self.grid[2 * current_y + 1 + dy][2 * current_x + 1 + dx] == '·':
                        visited.add((next_x, next_y))
                        queue.append((next_x, next_y))

        return False

    def _create_passage(self, start_x, start_y, end_x, end_y):
        if start_x == end_x:
            for j in range(min(start_y, end_y), max(start_y, end_y)):
                self.grid[2 * j + 2][2 * start_x + 1] = '·'
        elif start_y == end_y:
            for i in range(min(start_x, end_x), max(start_x, end_x)):
                self.grid[2 * start_y + 1][2 * i + 2] = '·'

    def _block_passage(self, start_x, start_y, end_x, end_y):
        if start_x == end_x:
            for j in range(min(start_y, end_y), max(start_y, end_y)):
                self.grid[2 * j + 2][2 * start_x + 1] = '█'
        elif start_y == end_y:
            for i in range(min(start_x, end_x), max(start_x, end_x)):
                self.grid[2 * start_y + 1][2 * i + 2] = '█'

m = Maze(4)
print(m)
print(m[0,0 : 1,0],m[0,0 : 2,2],m[1,0 : 1,2])
m[0,0 : 0,3] = m[0,3 : 3,3] = m[3,3 : 3,0] = m[3,0 : 2,0] = m[2,0 : 2,2] = m[1,0 : 1,2] = "·"
print(m)
print(m[0,0 : 1,0],m[0,0 : 2,2],m[1,0 : 1,2])