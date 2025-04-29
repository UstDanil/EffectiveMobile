import random


class Cell:
    def __init__(self, around_mines, mine):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

    def create_mine(self):
        self.around_mines = 0
        self.mine = True

    def increase_around_mines(self):
        self.around_mines += 1


class GamePole:
    def __init__(self, size, mines):
        self.size = size
        self.mines = mines
        self.no_mines = size * size - mines
        self.pole = list()
        self.mines_dict = dict()
        self.init()

    def init(self):
        self.create_empty_pole()
        self.set_mines_dict()
        self.fill_pole_with_mines()

    def create_empty_pole(self):
        for _ in range(self.size):
            row_cells = list()
            for _ in range(self.size):
                row_cells.append(Cell(0, False))
            self.pole.append(row_cells)

    def set_mines_dict(self):
        counter = 0
        while counter < self.mines:
            x = random.randint(0, self.size - 1)
            if x not in self.mines_dict:
                self.mines_dict[x] = set()
            y = random.randint(0, self.size - 1)
            if y in self.mines_dict[x]:
                continue
            self.mines_dict[x].add(y)
            counter += 1

    def fill_pole_with_mines(self):
        for mine_x, mine_ys in self.mines_dict.items():
            for mine_y in mine_ys:
                self.pole[mine_x][mine_y].create_mine()
                for add_x in (-1, 0, 1):
                    for add_y in (-1, 0, 1):
                        if add_x == 0 and add_y == 0:
                            continue

                        x_in_pole = 0 <= mine_x + add_x <= self.size-1
                        y_in_pole = 0 <= mine_y + add_y <= self.size-1
                        if x_in_pole and y_in_pole:
                            neighbour = self.pole[mine_x + add_x][mine_y + add_y]
                            if not neighbour.mine:
                                neighbour.increase_around_mines()

    def show(self):
        for row in self.pole:
            row_str = ""
            for cell in row:
                if cell.fl_open:
                    if cell.mine:
                        row_str += "* "
                    else:
                        row_str += str(cell.around_mines) + " "
                else:
                    row_str += "# "
            row_str += "\n"
            print(row_str)


if __name__ == '__main__':
    pole_game = GamePole(10, 12)
    game_over = False
    counter = 0
    while not game_over:
        answer = input("Введите координаты ячейки в формате 1,1 \n")
        row, col = answer.replace(" ", "").split(',')
        cell = pole_game.pole[int(row) - 1][int(col) - 1]
        cell.fl_open = True
        if cell.mine:
            print('ВЫ ПРОИГРАЛИ')
            game_over = True
        else:
            counter += 1
            if counter == pole_game.no_mines:
                print('ВЫ ВЫИГРАЛИ')
                game_over = True
        pole_game.show()
