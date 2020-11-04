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


def print_intro(board1, board2, with_ships = False):
    """
    Функция очистки экрана и вывода игровых полей.
    Аргументы:
    with_ships — отображать или нет при выводе поля противника расставленные
    корабли. По умолчанию False.
    """
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
        hidden_row = [EMPTY_SYMBOL if cell == SHIP_SYMBOL
                        else cell for cell in rows[1]]
        print(row_number, end='|')
        print(*rows[0], sep='|', end=' ' * 24)
        print(row_number, end='|')
        print(*rows[1] if with_ships else hidden_row, sep='|')
    print()


class Board:
    """
    Класс игрового поле.
    Атрибуты:
    size — размер игрового поля.
    state — текущее состояние игрового поля.
    ships — список кораблей (объектов класса Ship), находящихся на поле
    """
    board_size = 6
    ship_rules = [3, 2, 2, 1, 1, 1, 1]


    def __init__(self):
        self.size = self.board_size
        self.state = [[EMPTY_SYMBOL for col in range(self.size)]
                      for row in range(self.size)]
        self.ships = []


    def clear(self):
        """ Метод приведения игрового поля в изначальное состояние. """
        self.state = [[EMPTY_SYMBOL for col in range(self.size)]
                      for row in range(self.size)]
        self.ships = []


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
        """
        Метод расстановки кораблей на поле.
        Аргументы:
        auto — расставлять ли корабли автоматически случайным образом.
        По умолчанию True.
        """
        # Заглушка в виде пустой доски для функции отображения.
        dummy = Board()
        if auto:
            while len(self.ships) < len(self.ship_rules):

                # На случай возникновения тупиковой ситуации, при которой
                # следующий корабль невозможно разместить, используется
                # ограниченное количество попыток (50). По их истечению, поле
                # сбрасывается, и расстановка начинается сначала.
                try_count = 0
                while try_count <= 50:
                    try_count += 1
                    orientation = random.choice(('h', 'v'))
                    start_position = (random.randrange(self.size),
                                      random.randrange(self.size))
                    ship = Ship(self.ship_rules[len(self.ships)],
                                orientation, start_position)
                    if self.is_ship_fit(ship):
                        self.ships.append(ship)
                        self.add_ship(ship)
                        break
                if try_count > 50:
                    self.clear()
        else:
            for ship_number, ship_size in enumerate(self.ship_rules, 1):
                print_intro(self, dummy)
                print(f'Расстановка — Корабль №{ship_number}, '
                      f'{ship_size}-палубный')
                orientation = input('Введите ориентацию корабля — '
                                    'горизонтальная (h) или вертикальная (v): ')
                start_position = map(lambda x: x - 1, map(int, input('Введите '
                'координаты верхней левой точки корабля: ').split()))
                ship = Ship(ship_size, orientation, start_position)
                self.ships.append(ship)
                self.add_ship(ship)


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
        Метод проверки возможности размещения корабля в заданных координатах.
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


    def take_shot(self, ai):
        """
        Метод проведения выстрела по указанным координатам. Возвращает True при
        попадании и Else при промахе.
        Аргументы:
        ai — кто делает выстрел: компьютер или человек.
        """
        while True:
            if ai:
                x, y = (random.randrange(self.size),
                        random.randrange(self.size))
                if self.state[x][y] in (MISS_SYMBOL, HIT_SYMBOL):
                    continue
                time.sleep(TIMEOUT)
                print(*map(lambda x: x + 1, (x, y)))
                break
            try:
                x, y = map(lambda x: x - 1, map(int, input().split()))
            except ValueError:
                print('Неверный формат ввода. '
                      'Попробуйте ещё раз: ', end='')
                continue
            else:
                if x < 0 or x > self.size or y < 0 or y > self.size:
                    print('Таких координат не существует. '
                          'Попробуйте ещё раз: ', end='')
                    continue
                if self.state[x][y] in (MISS_SYMBOL, HIT_SYMBOL):
                    print('Вы уже стреляли в эту точку. '
                          'Попробуйте ещё раз: ', end='')
                    continue
                break
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
        """ Метод проверки игрового поля на предмет окончания игры. """
        for row in self.state:
            for cell in row:
                if cell == SHIP_SYMBOL:
                    return False
        # Если не осталось ни одного символа корабля, значит, игра окончена.
        return True


class Ship:
    """
    Класс корабля.
    Атрибуты:
    size — размер корабля.
    orientation — горизонтально или вертикально установлен корабль.
    width — условная ширина корабля.
    height — условная длина корабля.
    x, y — координаты левой верхней точки корабля.
    coordinates — список всех пар координат корабля.
    """
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
        print(f'Ход №{turn_count} — ', end='')
        print('Компьютер' if current_board == board1 else 'Игрок')
        print('Координаты выстрела:', end=' ', flush=True)

        # Если текущий игрок — компьютер, то ход происходит автоматически,
        # и если выстрел попал, то не меняем текущего игрока.
        if not current_board.take_shot(ai=current_board == board1):
            current_board = board2 if current_board == board1 else board1
        if current_board.is_win():
            break

    # Игрок, на котором закончился игровой цикл, является победителем.
    print_intro(board1, board2)
    print('Вы проиграли!' if current_board == board1 else 'Вы выиграли!')


    restart = input('Хотите сыграть ещё раз? (y/n) ') in ('y', 'Y')
    if restart:
        battleship()

    os.system(CLEAR_SCREEN)

if __name__ == '__main__':
    battleship()
