from math import *


def plot_line(start_x, start_y, end_y):
    end_x = start_x + 1
    if end_y != start_y:
        slope = (end_y - start_y) / (end_x - start_x)
        for delta_x in range(1, end_x - start_x + 1):
            current_x = start_x + delta_x
            current_y = round(start_y + slope * delta_x)
            if 0 <= current_y < H and 0 <= current_x < W:
                grid[current_y][current_x] = '*'
    if 0 <= end_y < H and 0 <= end_x < W:
        grid[end_y][end_x] = '*'


W, H, A, B, function_str = input().split()
W, H, A, B = int(W), int(H), float(A), float(B)

function_eval = lambda x: eval(function_str)

grid = [[' '] * W for _ in range(H)]

y_values = []
min_y = float('inf')
max_y = float('-inf')

for x in range(W):
    y = function_eval(A + x * (B - A) / W)
    min_y = min(min_y, y)
    max_y = max(max_y, y)
    y_values.append(y)

normalized_coords = [H - 1 - round((y - min_y) * (H - 1) / (max_y - min_y)) for y in y_values]

for x_index, y_start in enumerate(normalized_coords[:-1]):
    plot_line(x_index, y_start, normalized_coords[x_index + 1])

print("\n".join("".join(row) for row in grid))
