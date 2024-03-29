from Display import *


class Player(GameScreenDisplay):
    """
    Klasa odpowiedzialna za obsluge gracza
    """
    player_move_in_progress = True  # decyduje o tym czuja jest tura, TRUE - ruch ma gracz

    def player_handle_move(self) -> None:
        """
        Funckja sprawdza czy kursor myszy znajduje sie nad pustym polem gry, jesli tak rysuje obrazek X.
        Gdy gracz kliknie lewym przyciskiem myszy zatwierdzjac postawienie X w polu, dodaje element do tablicy.
        """
        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()

        for i in range(1, self.size + 1):
            x = i * self.gap_size + (i - 1) * self.box_size
            for j in range(1, self.size + 1):
                y = j * self.gap_size + (j - 1) * self.box_size
                if x < mouse_pos[0] < x + self.box_size and y < mouse_pos[1] < y + self.box_size and self.tags[i-1][j-1] is None:
                    displayWindow.blit(self.cross, (x, y))

                    if mouse_click[0] == 1:
                        self.tags[i-1][j-1] = 'x'
                        self.player_move_in_progress = False