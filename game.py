class Piece:
    def __init__(self, name, rotations):
        self.name = name
        self.rotations = rotations

    def rotate(self):
        self.rotations.append(self.rotations.pop(0))

    def move_down(self, dim_x):
        for row in self.rotations:
            for i in range(len(row)):
                row[i] += dim_x

    def move_right(self, dim_x):
        for row in self.rotations:
            for i in range(len(row)):
                row[i] = (row[i] + 1) % dim_x + (row[i] // dim_x) * dim_x

    def move_left(self, dim_x):
        for row in self.rotations:
            for i in range(len(row)):
                row[i] = (row[i] - 1) % dim_x + (row[i] // dim_x) * dim_x

    def get_current_rotation(self):
        return self.rotations[0]

    def get_num_rotations(self):
        return len(self.rotations)


class Grid:
    def __init__(self, dim_x, dim_y):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.squares = [["-" for _ in range(self.dim_x)] for _ in range(self.dim_y)]

    def get_width(self):
        return self.dim_x

    def update(self, rotation):
        self.squares = [["-" for _ in range(self.dim_x)] for _ in range(self.dim_y)]
        for num in rotation:
            if num // self.dim_x >= self.dim_y:
                continue
            self.squares[num // self.dim_x][num % self.dim_x] = '0'

    def render(self):
        print()
        for i, row in enumerate(self.squares):
            for j, slot in enumerate(row):
                if j < len(row) - 1:
                    print(slot + " ", end="")
                else:
                    print(slot, end="")
            if i < len(self.squares) - 1:
                print()
        print()
        print()


pieces = [Piece('I', [[4, 14, 24, 34], [3, 4, 5, 6]]),
          Piece('S', [[5, 4, 14, 13], [4, 14, 15, 25]]),
          Piece('Z', [[4, 5, 15, 16], [5, 15, 14, 24]]),
          Piece('L', [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]),
          Piece('J', [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]),
          Piece('O', [[4, 14, 15, 5]]),
          Piece('T', [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]])]

piece, grid = None, None

while not piece or not grid:
    command = input("Input command: ")
    if command == 'exit':
        break
    if command.startswith('piece:'):
        piece = [piece for piece in pieces if piece.name == command.split()[1]].pop()
    elif command.startswith('dimensions:'):
        x, y = command.split()[1:]
        grid = Grid(int(x), int(y))
        grid.render()

x = grid.get_width()
while True:
    grid.update(piece.get_current_rotation())
    grid.render()
    command = input("Input command: ")
    if command == 'exit':
        break
    if command == 'down':
        pass
    elif command == 'right':
        piece.move_right(x)
    elif command == 'left':
        piece.move_left(x)
    elif command == 'rotate':
        piece.rotate()
    piece.move_down(x)
