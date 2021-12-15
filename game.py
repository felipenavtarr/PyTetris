from collections import deque


class Piece:
    def __init__(self, name, rotations):
        self.name = name
        self.rotations = deque(rotations)
        self.frozen = False

    def get_current_rotation(self):
        return self.rotations[0]

    def get_num_rotations(self):
        return len(self.rotations)

    def is_frozen(self):
        return self.frozen

    def rotate(self):
        # for num in self.rotations[1]:
        # check for out of bounds when rotated?
        self.rotations.rotate(-1)

    def move(self, step):
        for row in self.rotations:
            for i in range(len(row)):
                row[i] += step

    def check_left_collision(self, grid_width):
        return any([num % grid_width == 0 for num in self.rotations[0]])

    def check_right_collision(self, grid_width):
        return any([num % grid_width == grid_width - 1 for num in self.rotations[0]])

    def check_floor_collision(self, grid_width, grid_height):
        return any([num // grid_width == grid_height - 1 for num in self.rotations[0]])

    def check_block_collision(self, grid_width, grid_squares):
        # Always check before if the piece is in the bottom to avoid index out of bounds
        return any([grid_squares[(num + grid_width) // grid_width][(num + grid_width) % grid_width] == '0' for num in self.rotations[0]])

    def freeze(self):
        self.frozen = True


class Grid:
    def __init__(self, dim_x, dim_y):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.squares = [["-" for _ in range(self.dim_x)] for _ in range(self.dim_y)]

    def get_width(self):
        return self.dim_x

    def get_height(self):
        return self.dim_y

    def get_squares(self):
        return self.squares

    def clear_current_piece(self, rotation):
        for num in rotation:
            self.squares[num // self.dim_x][num % self.dim_x] = '-'

    def update(self, rotation):
        for num in rotation:
            self.squares[num // self.dim_x][num % self.dim_x] = '0'

    def render(self):
        for i, row in enumerate(self.squares):
            for j, slot in enumerate(row):
                if j < len(row) - 1:
                    print(slot + " ", end="")
                else:
                    print(slot, end="")
            if i < len(self.squares) - 1:
                print()
        print("\n")


pieces = {'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
          'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
          'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
          'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
          'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
          'O': [[4, 14, 15, 5]],
          'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}

piece, grid = None, None
game_over = False

while True:
    if piece and grid:
        grid.update(piece.get_current_rotation())
        grid.render()
        if game_over:
            print("Game Over!")
            break

    command = input()

    if command == 'exit':
        break
    if command == 'piece':
        requested = input()
        if requested in {'I', 'S', 'Z', 'L', 'J', 'O', 'T'}:
            piece = Piece(requested, [x[::] for x in pieces[requested]])
    elif len(command.split()) == 2:
        x, y = command.split()
        try:
            grid = Grid(int(x), int(y))
            grid.render()
            x = grid.get_width()
            y = grid.get_height()
        except ValueError:
            continue
    elif grid and piece:
        if command == 'break':
            rows = grid.get_squares()
            for row in rows:
                if '-' not in row:
                    rows.remove(row)
                    rows.insert(0, ['-' for _ in range(x)])
            grid.render()
            piece = None
        elif not piece.is_frozen():
            grid.clear_current_piece(piece.get_current_rotation())
            lateral_step = 0
            if command == 'down':
                pass
            elif command == 'right':
                if not piece.check_right_collision(x):
                    lateral_step = 1
            elif command == 'left':
                if not piece.check_left_collision(x):
                    lateral_step = -1
            elif command == 'rotate':
                piece.rotate()
            else:
                continue

            if lateral_step:
                piece.move(lateral_step)

            if piece.check_block_collision(x, grid.get_squares()):
                piece.freeze()
                # Check Game Over
                if lateral_step:
                    piece.move(-lateral_step)
                grid.update(piece.get_current_rotation())
                for col in range(x):
                    if '-' not in [row[col] for row in grid.get_squares()]:
                        game_over = True
                        break
                continue

            piece.move(x)

            if piece.check_floor_collision(x, y):
                piece.freeze()
