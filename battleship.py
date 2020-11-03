"""
Игра «Морской бой» на поле 6x6.
Итоговое практическое задание B7.5 для SkillFactory.
Используются модули только из стандартной библиотеки Python 3.8.5.
"""


import os
import random
import time


CLEAR_SCREEN        = 'cls' if os.name == 'nt' else 'clear'
TIMEOUT             = 1
EMPTY_SYMBOL        = '~'
SHIP_SYMBOL         = '■'
HIT_SYMBOL          = 'X'
MISS_SYMBOL         = 'T'


def print_intro(board1, board2, with_ships = True):
    """ Функция очистки экрана и вывода игровых полей. """
    # Изначально использовался метод draw класса Board, но для более
    # симпатичного вывода решил использовать эту функцию.
    # Код метода оставлен в программе и закомментирован.
    os.system(CLEAR_SCREEN)
    print('-' * 50)
    print('Морской бой'.center(50))
    print()
    print('формат ввода ходов: «строка колонка»'.center(50))
    print('-' * 50)
    print()
    print('Игрок'.center(13) + ' ' * 24 + 'Компьютер'.center(13))
    print()
    print(' ', *range(1, board1.size + 1), sep='|', end=' ' * 24)
    print(' ', *range(1, board2.size + 1), sep='|')
    for row_number, rows in enumerate(zip(board1.state, board2.state), 1):
        hidden_row1 = [EMPTY_SYMBOL if cell == SHIP_SYMBOL
                        else cell for cell in rows[0]]
        hidden_row2 = [EMPTY_SYMBOL if cell == SHIP_SYMBOL
                        else cell for cell in rows[0]]
        print(row_number, end='|')
        print(*rows[0] if with_ships else hidden_row1, sep='|', end=' ' * 24)
        print(row_number, end='|')
        print(*rows[1] if with_ships else hidden_row2, sep='|')
    print()


class Board:
    """ Класс игрового поле. """
    board_size = 6
    ships = [3, 2, 2, 1, 1, 1, 1]

    def __init__(self):
        self.size = self.board_size
        self.state = [[EMPTY_SYMBOL for col in range(self.size)]
                      for row in range(self.size)]


    def clear(self):
        """ Метод приведения игрового поля в изначальное состояние. """
        self.state = [[EMPTY_SYMBOL for col in range(self.size)]
                      for row in range(self.size)]


    # def draw(self, with_ships = True):
    #     """
    #     Метод отображения игрового поля.
    #     Аргументы:
    #     with_ships — отображать или, в случае компьютерного игрока,
    #     скрывать корабли на поле. Значение по умолчанию: True.
    #     """
    #     print(' ', *range(1, self.size + 1), sep='|')
    #     for row_number, row in enumerate(self.state, 1):
    #         print(row_number, end='|')
    #         hidden_row = [EMPTY_SYMBOL if cell == SHIP_SYMBOL
    #                       else cell for cell in row]
    #         print(*row if with_ships else hidden_row, sep='|')
    #     print()


    def setup(self, auto = True):
        # Заглушка в виде пустой доски для функции отображения.
        dummy = Board()
        player_ships = []
        if auto:
            while len(player_ships) < len(self.ships):
                try_count = 0
                while try_count <= 50:
                    try_count += 1
                    orientation = random.choice(('h', 'v'))
                    start_position = (random.randrange(6), random.randrange(6))
                    ship = Ship(self.ships[len(player_ships)], orientation, start_position)
                    if self.is_ship_fit(ship):
                        player_ships.append(ship)
                        self.add_ship(ship)
                        break
                if try_count > 50:
                    player_ships = []
                    self.clear()
        else:
            for ship_number, ship_size in enumerate(self.ships, 1):
                print_intro(self, dummy)
                print(f'Расстановка — Корабль №{ship_number}, {ship_size}-палубный')
                orientation = input('Введите ориентацию корабля — '
                                    'горизонтальная (h) или вертикальная (v): ')
                start_position = map(lambda x: x - 1, map(int, input('Введите '
                'координаты верхней левой точки корабля: ').split()))
                player_ship = Ship(ship_size, orientation, start_position)
                player_ships.append(player_ship)
                self.add_ship(player_ship)


    def add_ship(self, ship):
        """
        Метод добавления корабля на игровое поле.
        Аргументы:
        ship — объект класса Ship
        """
        for x, y in ship.coordinates:
            self.state[x][y] = SHIP_SYMBOL


    def is_ship_fit(self, ship):
        """
        Метод проверки возможности размещения корабля в заданных
        координатах.
        Аргументы:
        ship — объект класса Ship
        """
        # Проверяем, помещается ли корабль целиком на поле.
        if ship.x + ship.height - 1 >= self.size or \
           ship.y + ship.width - 1 >= self.size:
            return False

        # Если да, то проверяем, нет ли в радиусе одной клетки от него
        # другого корабля.
        for x in range(ship.x - 1, ship.x + ship.height + 1):
            for y in range(ship.y - 1, ship.y + ship.width + 1):
                try:
                    if self.state[x][y] != EMPTY_SYMBOL:
                        return False
                except IndexError:
                    continue

        # Если обе проверки пройдены, значит, корабль можно разместить.
        return True


    def take_shot(self, coordinates):
        """
        Метод проведения выстрела по указанным координатам.
        Возвращает True при попадании и Else при промахе.
        Аргументы:
        coordinates — кортеж с двумя координатами
        """
        x, y = coordinates
        if self.state[x][y] == SHIP_SYMBOL:
            self.state[x][y] = HIT_SYMBOL
            time.sleep(TIMEOUT)
            print('Попадание!')
            time.sleep(TIMEOUT)
            return 1
        elif self.state[x][y] == EMPTY_SYMBOL:
            self.state[x][y] = MISS_SYMBOL
            time.sleep(TIMEOUT)
            print('Промах!')
            time.sleep(TIMEOUT)
            return 0
        return -1

    def is_win(self):
        """
        Метод проверки игрового поля на предмет окончания игры.
        Если не осталось ни одного символа корабля, значит,
        игра окончена.
        """
        for row in self.state:
            for cell in row:
                if cell == SHIP_SYMBOL:
                    return False
        return True


class Ship:
    """ Класс корабля. """
    def __init__(self, size, orientation, start_position):
        self.size = size
        self.orientation = orientation
        self.width = size if orientation == 'h' else 1
        self.height = 1 if orientation == 'h' else size
        self.x, self.y = start_position
        self.coordinates = []
        for cell in range(self.size):
            self.coordinates.append((self.x, self.y + cell)
                if self.orientation == 'h' else (self.x + cell, self.y))


def battleship():
    """ Основная игровая функция. """
    board1 = Board()
    board2 = Board()

    # Расстановка кораблей
    print_intro(board1, board2)
    auto = input('Расставить корабли автоматически? (y/n) ') in ('y', 'Y')
    board1.setup(auto)
    board2.setup()

    # Начало игры
    turn_count = 0
    current_board = board2
    while True:
        turn_count += 1
        print_intro(board1, board2)
        print(f'Ход №{turn_count}')
        print('Координаты выстрела:', end=' ', flush=True)
        if current_board == board2:
            shot = map(lambda x: x - 1, map(int, input().split()))
            #TODO: if shot isn't legit -> retry
        else:
            shot = (random.randrange(6), random.randrange(6))
            time.sleep(TIMEOUT)
            print(*map(lambda x: x + 1, shot))

        # Если выстрел не попал, то меняем текущего игрока.
        if not current_board.take_shot(shot):
            current_board = board2 if current_board == board1 else board1
        if current_board.is_win():
            break

    print_intro(board1, board2)
    if board2.is_win():
        print('Вы выиграли!')
    elif board1.is_win():
        print('Вы проиграли!')


    restart = input('Хотите сыграть ещё раз? (y/n) ') in ('y', 'Y')
    if restart:
        battleship()

    os.system(CLEAR_SCREEN)

if __name__ == '__main__':
    battleship()
