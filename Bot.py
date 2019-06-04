from Display import *

INFINITY = 1000000 # nieskonczonosc


class Bot(GameScreenDisplay):
    """
    Sprawdza aktualny stan gry na planszy
    """
    def check_columns(self, win: list) -> bool:
        """
        Sprawdza kolumny pod wzgledem wygranej.
        :param win: paramentr reprezentujacy wygrywajaca sekwencje
        :return: True, jesli znaleziono sekwencje wygranej.
        """
        for row in range(self.size):
            column = [self.tags[x][row] for x in range(self.size)]
            for j in range(len(column) - len(win) + 1):
                if win == column[j:j+self.win_condition]:
                    return True

    def check_rows(self, win: list) -> bool:
        """
        Sprawdza wiersze pod wzgledem wygranej.
        :param win: paramentr reprezentujacy wygrywajaca sekwencje
        :return: True, jesli znaleziono sekwencje wygranej.
        """
        for row in self.tags:
            for j in range(len(row) - len(win) + 1):
                if win == row[j:j+self.win_condition]:
                    return True

    def check_diagonals(self, win: list) -> bool:
        """
        Sprawdza diagonale pod wzgledem wygranej.
        :param win: paramentr reprezentujacy wygrywajaca sekwencje
        :return: True, jesli znaleziono sekwencje wygranej.
        """
        for i in range(self.size - self.win_condition + 1):
            # [x x    ]
            # [  x x  ]
            # [    x x]
            # [      x]
            diagonal = []
            x = i
            y = 0
            for j in range(self.size - i):
                diagonal.append(self.tags[x][y])
                x += 1
                y += 1
            for j in range(len(diagonal) - len(win) + 1):
                if win == diagonal[j:j + self.win_condition]:
                    return True
            # [x      ]
            # [x x    ]
            # [  x x  ]
            # [    x x]
            diagonal = []
            x = 0
            y = i
            for j in range(self.size - i):
                diagonal.append(self.tags[x][y])
                x += 1
                y += 1
            for j in range(len(diagonal) - len(win) + 1):
                if win == diagonal[j:j + self.win_condition]:
                    return True

            # [    x x]
            # [  x x  ]
            # [x x    ]
            # [x      ]
            diagonal = []
            x = self.size - 1 - i
            y = 0
            for j in range(self.size - i):
                diagonal.append(self.tags[x][y])
                x -= 1
                y += 1
            for j in range(len(diagonal) - len(win) + 1):
                if win == diagonal[j:j + self.win_condition]:
                    return True
            # [      x]
            # [    x x]
            # [  x x  ]
            # [x x    ]
            diagonal = []
            x = self.size - 1
            y = 0 + i
            for j in range(self.size - i):
                diagonal.append(self.tags[x][y])
                x -= 1
                y += 1
            for j in range(len(diagonal) - len(win) + 1):
                if win == diagonal[j:j + self.win_condition]:
                    return True

    def check_if_win(self, tag: str) -> bool:
        """
        Sprawdza czy znaleziono zwycieska sekwencje
        :param tag:Symbol z ktorego bedzie skladala sie sekwencja -> {'x', 'o'}.
        :return: True, jesli znaleziono sekwencje wygranej.
        """
        win_line = [tag]*self.win_condition
        return self.check_rows(win_line) or self.check_columns(win_line) or self.check_diagonals(win_line)

    def full_board(self) -> bool:
        """
       Sprawdza czy tablica zostala w pelni wypeliona.
        :return: True, jesli plansza jest pelna
        """
        counter = 0
        for column in self.tags:
            if None in column:
                counter += 1
        return counter == 0

    def check_for_moves(self) -> list:
        """
        Szuka mozliwych ruchow, koordynaty pakuje w tuple i dodaje do listy mozliwych ruchow.
        :return: Lista mozliwych ruchow
        """
        avail_moves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.tags[x][y] is None:
                    avail_moves.append((x, y))
        return avail_moves

    def bot_handle_move(self) -> None:
        """
        Rekurencyjnie sprawdza najlepsze ruchy za pomoca algorytmu minimax, nastepnie wpisuje w to miejsce tag`a
        """
        best_value = -INFINITY  # Najwieksza wartosc dla maksymalizujacego gracza( w tym przypadku dla bota)
        available_moves = self.check_for_moves()
        depth = int(1.4*self.size - self.win_condition)  # (depth) decyduje o glebokosci rekurencji algorytmu,
        best_move = None                                 #  doswiadczalnie wybrane 1.3*siza-win_condition wydaje sie najlepsze dla zoptymalizowania
                                                         #  czasu oraz poziomu ruchow bota dla duzych wymiarow planszy.
        for move in available_moves:
            self.tags[move[0]][move[1]] = 'o'
            move_value = self.minimax(depth, -INFINITY, INFINITY, False)
            self.tags[move[0]][move[1]] = None
            if  move_value > best_value:
                best_value = move_value
                best_move = move

        self.tags[best_move[0]][best_move[1]] = 'o'

    def minimax(self, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
        """
        Minimax algorytm z mozliwoscia odcinania niepotrzebnych galezi(prunning).
        :param depth: Gelgokosc rekurencji
        :param alpha, beta: parametry umozliwiajace odcinanie niepotrzebnych galezi
        :param maximizing_player: Bool decydujacy ktory gracz ma ruch, bot czy gracz (maximizing, minimizing)
        :return: Najlepsza wartosc, w zaleznosci od typu gracza (maximizing, minimizing)
        """
        if self.check_if_win('x' if maximizing_player is True else 'o'):
            return -10 if maximizing_player else 10
        if self.full_board():
            return 1
        if depth == 0:
            return 0

        available_moves = self.check_for_moves()

        if maximizing_player:
            max_eval = -INFINITY
            for move in available_moves:
                self.tags[move[0]][move[1]] = 'o'
                evaluation = self.minimax(depth - 1, alpha, beta, False)
                self.tags[move[0]][move[1]] = None
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = INFINITY
            for move in available_moves:
                self.tags[move[0]][move[1]] = 'x'
                evaluation = self.minimax(depth - 1, alpha, beta, True)
                self.tags[move[0]][move[1]] = None
                min_eval = min(min_eval, evaluation)
                alpha = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval
