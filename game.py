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
        # check for out of bounds when rotate?
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

    def update(self, rotation):
        self.squares = [["-" for _ in range(self.dim_x)] for _ in range(self.dim_y)]
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


pieces = [Piece('I', [[4, 14, 24, 34], [3, 4, 5, 6]]),
          Piece('S', [[5, 4, 14, 13], [4, 14, 15, 25]]),
          Piece('Z', [[4, 5, 15, 16], [5, 15, 14, 24]]),
          Piece('L', [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]),
          Piece('J', [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]),
          Piece('O', [[4, 14, 15, 5]]),
          Piece('T', [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]])]

piece, grid = None, None

while True:
    if piece and grid:
        grid.update(piece.get_current_rotation())
        grid.render()
    command = input()
    if command == 'exit':
        break
    if command in {'I', 'S', 'Z', 'L', 'J', 'O', 'T'}:
        piece = [piece for piece in pieces if piece.name == command].pop()
    elif len(command.split()) == 2:
        x, y = command.split()
        try:
            grid = Grid(int(x), int(y))
            grid.render()
            x = grid.get_width()
            y = grid.get_height()
        except ValueError:
            continue
    elif grid and not piece.is_frozen():
        if command == 'down':
            pass
        elif command == 'right':
            if not piece.check_right_collision(x):
                piece.move(1)
        elif command == 'left':
            if not piece.check_left_collision(x):
                piece.move(-1)
        elif command == 'rotate':
            piece.rotate()
        else:
            continue
        piece.move(x)
        if piece.check_floor_collision(x, y):
            piece.freeze()
