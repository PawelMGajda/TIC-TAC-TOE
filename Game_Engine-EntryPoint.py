from Mechanics import *


class GameEngine:
    """
    Klasa odpowiedzialna za wlaczenie glownej petli programu, gry.
    """
    def __init__(self):
        """
        Inicjalizacja obiektu
        """
        self.game_mechanics = None
        self.entry_display = EntryScreenDisplay()

    def run_end_screen(self, message: str) -> None:
        """
        Ekran koncowy gry.
        Aby wylaczyc nalezy kliknac na ekran gry.
        :param message: Wiadomosc z wynikiem gry.
        """
        end_screen = True
        while end_screen:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    end_screen = False
                    pg.time.delay(200)

            self.entry_display.display_message(250, message, BLUE, (400, 400))
            self.entry_display.display_message(255, message, WHITE, (400, 400))
            self.entry_display.display_message(102, 'Click to continue...', BLUE, (400, 500))
            self.entry_display.display_message(100, 'Click to continue...', WHITE, (400, 500))

            pg.display.update()

    def run_main_screen(self) -> int:
        """
        Wlacza ekran gry
        Wyswietla aktualny stan na planszy
        Sprawdza czy gra sie nie zakonczyla z powodu wygranej, przegranej lub remisu.
        :return "1" aby zapobiec zbyt wczesnemu wyswietlaniu sie przycisku START po zakonczeniu rozgrywki
        """
        run = True
        self.game_mechanics = GameScreenMechanics(self.entry_display.board_size, self.entry_display.win_cond)
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False

            self.game_mechanics.draw_components()
            if self.game_mechanics.player_move_in_progress:
                self.game_mechanics.move_player()
            else:
                self.entry_display.display_message(100, 'WAIT A SEC...', BLUE, (400, 400))
                pg.display.update()
                self.game_mechanics.move_bot()
            pg.display.update()
            self.game_mechanics.draw_components()

            if self.game_mechanics.check_if_win('o'):
                run = False
                self.run_end_screen('YOU DIE')
            elif self.game_mechanics.check_if_win('x'):
                run = False
                self.run_end_screen('YOU WIN')
            elif self.game_mechanics.full_board():
                run = False
                self.run_end_screen('DRAW')
        return 1

    def run_first_screen(self) -> None:
        """
        Wlacza poczatkowy ekran gry.
        Daje mozliwosc uzytkownikowi do zmiany wielkosci planszy oraz warunku wygranej za pomoca guzkikow, oraz mozliwosc rozpoczecia gry.
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        quit()
            self.entry_display.print_components(self.run_main_screen)
            pg.display.update()


# Entry point
if __name__ == '__main__':
    gE = GameEngine()
    gE.run_first_screen()
