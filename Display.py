import pygame as pg

#Rozmiar ekranu gry
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
MIGHTY_BLUE = (79, 153, 209)
GRAY = (204, 204, 204)
BLUE =(0, 0, 255)

# Ikony X oraz O
cross = pg.image.load('images/x.png')
circle = pg.image.load('images/o.png')

pg.init()


displayWindow = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#Nazwa gry
pg.display.set_caption('Tic-Tac-Toe')


class EntryScreenDisplay:
    """
    Ekran startowy, pokazujacy sie przy wlaczeniu gry oraz na zakonczenie rozgrywki
    """
    board_size = 3 # Wielkosc pola do gry, domyslnie 3x3
    win_cond = 3 # Warunek wygrania gry, domyslnie 3 w lini

    def increment_board(self) -> None:
        """
        Domyslnie zwiekszanie wielkosci pola gry zwieksza warunek wygranej
        """
        if self.board_size < 7:
            self.board_size += 1
            self.win_cond += 1

    def increment_win(self) -> None:
        if self.win_cond < 7 and self.win_cond < self.board_size:
            self.win_cond += 1

    def decrement_board(self) -> None:

        if self.board_size > 3:
            self.board_size += -1
            if self.win_cond > self.board_size:
                self.win_cond += -1

    def decrement_win(self) -> None:
        if self.win_cond > 3:
            self.win_cond += -1

    def display_message(self, size: int, message: str, color: tuple, position: tuple) -> None:
        """
        Wyswietla wiadomosc do uzytkownika o odpowiednim rozmiarze, w odpowiednim kolorze i na odpowiedniej pozycji.
        :param size : wielkosc tekstu
        :param message: string z tekstem do wyswietlenia
        :param color: kolor tekstu
        :param position: koordynaty x,y tekstu
        """
        text = pg.font.Font(None, size)
        text_surf = text.render(message, True, color)
        text_rect = text_surf.get_rect()
        text_rect.center = position
        displayWindow.blit(text_surf, text_rect)

    def maintain_button(self, position: tuple, width: int, height: int, rect_color: tuple, message: str,
                        mess_color: tuple, desired_action=None) -> None:
        """
        Wyswietla przycisk o podanych parametrach i o odpowiedniej funkcji.
        :param height: wysokosc przycisku
        :param width: szerokosc przycisku
        :param message: string z tekstem do wyswietlenia na przycisku
        :param mess_color: kolor tekstu wyswietlany na przycisku
        :param rect_color: kolor przycisku
        :param position: koordynaty x,y przycisku
        :param desired_action: funckja przycisku
        """
        mouse_pos = pg.mouse.get_pos()
        mouse_clicked = pg.mouse.get_pressed()

        if (position[0] - width / 2) < mouse_pos[0] < (position[0] + width / 2) and position[1] < mouse_pos[1] < (position[1] + height):
            if mouse_clicked[0] == 1 and desired_action is not None:
                pg.time.delay(200)
                if desired_action():  # prawda tylko podczas gdy gra sie skonczyla, zapobiega to zbyt wczesnemu pojawianiu sie przycisku START
                    return
        pg.draw.rect(displayWindow, rect_color, ((position[0] - (width / 2), position[1]), (width, height)))
        self.display_message(int(height / 2), message, mess_color, (position[0], position[1] + height / 2))

    def print_components(self, run_main):
        """
        Wyswietla komponenty na ekranie startowym
        :param run_main: Funckja powodujaca start gry
        """
        displayWindow.fill(MIGHTY_BLUE)
        self.display_message(120, 'Tic-Tac-Toe', BLACK, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.15))
        self.display_message(60, 'Win or Die', RED, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.25))
        self.display_message(40, 'Size of the board', GRAY, (WINDOW_WIDTH * 0.265, WINDOW_HEIGHT * 0.4))
        self.maintain_button((WINDOW_WIDTH * 0.14, WINDOW_HEIGHT*0.48), 50, 50, GRAY, "-", BLACK, self.decrement_board)
        self.maintain_button((WINDOW_WIDTH * 0.39, WINDOW_HEIGHT*0.48), 50, 50, GRAY, "+", BLACK, self.increment_board)
        self.maintain_button((WINDOW_WIDTH * 0.266, WINDOW_HEIGHT*0.445), 150, 100, WHITE, str(self.board_size), BLACK )
        self.display_message(40, 'Win condition', GRAY, (WINDOW_WIDTH * 0.26, WINDOW_HEIGHT * 0.66))
        self.maintain_button((WINDOW_WIDTH * 0.14, WINDOW_HEIGHT * 0.735), 50, 50, GRAY, "-", BLACK, self.decrement_win)
        self.maintain_button((WINDOW_WIDTH * 0.39, WINDOW_HEIGHT * 0.735), 50, 50, GRAY, "+", BLACK, self.increment_win)
        self.maintain_button((WINDOW_WIDTH * 0.266, WINDOW_HEIGHT * 0.7), 150, 100, WHITE, str(self.win_cond), BLACK)
        self.maintain_button((WINDOW_WIDTH * 0.75, WINDOW_HEIGHT * 0.5), 200, 150, WHITE, 'START', BLACK, run_main)


class GameScreenDisplay:
    """
    Ekran gry
    """
    def __init__(self, size, win_condition):
        self.size = size
        self.win_condition = win_condition
        self.box_size = WINDOW_WIDTH / (1.1 * self.size + 0.1)   # wielkosc pola gry
        self.gap_size = 0.1 * self.box_size  # przerwa pomiedzy polami gry
        self.tags = [[None for x in range(self.size)] for y in range(self.size)]  # pusta tablica tag`ów, znaków graczy {'x','o'}
        self.cross = self.resize_tags(cross, True)  # dopasowanie wielkosci X do rozmiaru planszy
        self.circle = self.resize_tags(circle, False)  # dopasowanie wielkosci O do rozmiaru planszy

    def resize_tags(self, image: pg.SurfaceType, is_cross: bool) -> pg.SurfaceType:
        """
        Funckja zmieniajaca rozmiar obrazkow X oraz O
        :param image: klasa pygame reprezentujaca obraz
        :param size: rozmiar planszy
        :param is_cross: ktory obraz przyjmuje X czy O
        :return: obraz o zmienionej wielkosci
        """
        if is_cross:
            x = 1.38
            y = 1.38
        else:
            x = 1.87
            y = 1.87

        image_rect = image.get_rect()
        image = pg.transform.scale(image, (int(x / self.size * image_rect.width), int(y / self.size * image_rect.height)))
        return image

    def draw_grid(self) -> None:
        """
        Rysuje siatke planszy gry, pola na ktorych beda wpisywane X oraz O
        """
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                pg.draw.rect(displayWindow, GRAY, [j*self.gap_size+(j-1)*self.box_size,
                                                   i*self.gap_size+(i-1)*self.box_size, self.box_size, self.box_size])

    def draw_tags(self) -> None:
        """
        Rysuje obrazki X oraz O w polach wybranych przez gracza oraz bota
        """
        for i in range(1, self.size + 1):
            x = i * self.gap_size + (i - 1) * self.box_size
            for j in range(1, self.size + 1):
                y = j * self.gap_size + (j - 1) * self.box_size
                if self.tags[i-1][j-1] == 'x':
                    displayWindow.blit(self.cross, (x, y))
                elif self.tags[i-1][j-1] == 'o':
                    displayWindow.blit(self.circle, (x, y))

    def draw_components(self) -> None:
        """
        Wyswietla wszystkie komponenty na ekran
        """
        displayWindow.fill(MIGHTY_BLUE)
        self.draw_grid()
        self.draw_tags()