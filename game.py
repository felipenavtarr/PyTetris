class Piece:
    def __init__(self, name, rotations):
        self.name = name
        self.rotations = rotations

    def rotate(self):
        self.rotations.append(self.rotations.pop(0))

    def get_current_rotation(self):
        return self.rotations[0]

    def get_num_rotations(self):
        return len(self.rotations)


class Grid:
    def __init__(self):
        self.dim = 4
        self.squares = [["-" for _ in range(self.dim)] for _ in range(self.dim)]

    def update(self, rotation):
        self.squares = [["-" for _ in range(self.dim)] for _ in range(self.dim)]
        for num in rotation:
            self.squares[num // self.dim][num % self.dim] = '0'

    def render(self):
        for i, row in enumerate(self.squares):
            for j, slot in enumerate(row):
                if j < len(row) - 1:
                    print(slot + " ", end="")
                else:
                    print(slot, end="")
            if i < len(self.squares) - 1:
                print()
        print()


grid = Grid()
pieces = [Piece('I', [[1, 5, 9, 13], [4, 5, 6, 7]]),
          Piece('S', [[6, 5, 9, 8], [5, 9, 10, 14]]),
          Piece('Z', [[4, 5, 9, 10], [2, 5, 6, 9]]),
          Piece('L', [[1, 5, 9, 10], [6, 8, 9, 10], [5, 6, 10, 14], [5, 6, 7, 9]]),
          Piece('J', [[2, 6, 9, 10], [4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6]]),
          Piece('O', [[5, 6, 9, 10]]),
          Piece('T', [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]])]

command = input()
piece = [piece for piece in pieces if piece.name == command].pop()
# for _ in range(piece.get_num_rotations() + 1):
for _ in range(6):
    print()
    grid.render()
    grid.update(piece.get_current_rotation())
    piece.rotate()
