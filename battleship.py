"""
Игра «Морской бой» на поле 6x6.
Итоговое практическое задание B7.5 для SkillFactory.
Используются модули только из стандартной библиотеки Python 3.8.5.

TODO: Авторасстановка кораблей
TODO: Отображать поле компьютера в скрытом состоянии (без кораблей)
"""


import os
import random
import time


CLEAR_SCREEN        = 'cls' if os.name == 'nt' else 'clear'
EMPTY_SYMBOL        = 'O'
SHIP_SYMBOL         = '■'
HIT_SYMBOL          = 'X'
MISS_SYMBOL         = 'T'


def print_intro(board1, board2):
    """ Функция очистки экрана и вывода игровых полей. """
    os.system(CLEAR_SCREEN)
    print('-' * 50)
    print('Морской бой')
    print()
    print('формат ввода ходов: «строка колонка»')
    print('-' * 50)
    print()
    print('Ваше поле:')
    board1.draw(with_ships=True)
    print('Поле противника:')
    board2.draw(with_ships=True)


class Board:
    """ Класс игрового поле. """
    board_size = 6

    def __init__(self):
        self.size = self.board_size
        self.state = [[EMPTY_SYMBOL for col in range(self.size)]
                      for row in range(self.size)]


    def clear(self):
        """ Метод приведения игрового поля в изначальное состояние. """
        self.state = [[EMPTY_SYMBOL for col in range(self.size)]
                      for row in range(self.size)]


    def draw(self, with_ships = True):
        """
        Метод отображения игрового поля.
        Аргументы:
        with_ships — отображать или, в случае компьютерного игрока,
        скрывать корабли на поле. Значение по умолчанию: True.
        """
        print(' ', *range(1, self.size + 1), sep='|')
        for row_number, row in enumerate(self.state, 1):
            print(row_number, end='|')
            hidden_row = [EMPTY_SYMBOL if cell == SHIP_SYMBOL
                          else cell for cell in row]
            print(*row if with_ships else hidden_row, sep='|')
        print()

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


    def shot(self, coordinates):
        """
        Метод проведения выстрела по указанным координатам.
        Возвращает True при попадании и Else при промахе.
        Аргументы:
        coordinates — кортеж с двумя координатами
        """
        x, y = coordinates
        if self.state[x][y] == SHIP_SYMBOL:
            self.state[x][y] = HIT_SYMBOL
            time.sleep(0.5)
            print('Попадание!')
            time.sleep(0.5)
            return True
        elif self.state[x][y] == EMPTY_SYMBOL:
            self.state[x][y] = MISS_SYMBOL
            time.sleep(0.5)
            print('Промах!')
            time.sleep(0.5)
            return False

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
    ships = [3, 2, 2, 1, 1, 1, 1]
    player_ships = []
    ai_ships = []
    board1 = Board()
    board2 = Board()

    # Расстановка кораблей игроком
    """
    for ship_number, ship_size in enumerate(ships, 1):
        print_intro(board1, board2)
        print(f'Расстановка — Корабль №{ship_number}, {ship_size}-палубный')
        orientation = input('Введите ориентацию корабля — '
                            'горизонтальная (h) или вертикальная (v): ')
        start_position = map(lambda x: x - 1, map(int, input('Введите '
        'координаты верхней левой точки корабля: ').split()))
        player_ship = Ship(ship_size, orientation, start_position)
        player_ships.append(player_ship)
        board1.add_ship(player_ship)
    """
    while len(player_ships) < len(ships):
        try_count = 0
        while try_count <= 50:
            try_count += 1
            player_orientation = random.choice(('h', 'v'))
            player_start_position = (random.randrange(6), random.randrange(6))
            player_ship = Ship(ships[len(player_ships)], player_orientation, player_start_position)
            if board1.is_ship_fit(player_ship):
                player_ships.append(player_ship)
                board1.add_ship(player_ship)
                break
        if try_count > 50:
            player_ships = []
            board1.clear()

    # Расстановка кораблей компьютером
    while len(ai_ships) < len(ships):
        try_count = 0
        while try_count <= 50:
            try_count += 1
            ai_orientation = random.choice(('h', 'v'))
            ai_start_position = (random.randrange(6), random.randrange(6))
            ai_ship = Ship(ships[len(ai_ships)], ai_orientation, ai_start_position)
            if board2.is_ship_fit(ai_ship):
                ai_ships.append(ai_ship)
                board2.add_ship(ai_ship)
                break
        if try_count > 50:
            ai_ships = []
            board2.clear()

    # Перестрелка
    turn_count = 0
    current_board = board2
    while True:
        turn_count += 1
        print_intro(board1, board2)
        print(f'Ход №{turn_count}')
        if current_board == board2:
            shot = map(lambda x: x - 1,
                       map(int, input('Координаты выстрела: ').split()))
        else:
            shot = (random.randrange(6), random.randrange(6))
        
        # Если выстрел не попал, то меняем текущего игрока.
        if not current_board.shot(shot):
            current_board = board2 if current_board == board1 else board1
        if current_board.is_win():
            break

    print_intro(board1, board2)
    if board2.is_win():
        print('Вы выиграли!')
    elif board1.is_win():
        print('Вы проиграли!')


    restart = input('Хотите сыграть ещё раз? (y/n) ')
    if restart in ('y', 'Y'):
        battleship()

    os.system(CLEAR_SCREEN)

if __name__ == '__main__':
    battleship()
