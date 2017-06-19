import curses


class CoursesWindow:
    """
    Attributes
    ----------
    stdscr : curses window
    window : curses window
    text_window : curses window
    """
    def __init__(self, title, down_message):
        self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        self.stdscr.addstr(title, curses.A_REVERSE)
        self.stdscr.chgat(-1, curses.A_REVERSE)

        self.stdscr.addstr(curses.LINES-1, 0, down_message)

        self.window = curses.newwin(curses.LINES-2, curses.COLS, 1, 0)
        self.text_window = self.window.subwin(curses.LINES-6, curses.COLS-4, 3, 2)
        self.window.box()

        self.update()

    def getch(self):
        return self.window.getch()

    def update(self):
        """
        Refreshes all windows
        """
        self.stdscr.noutrefresh()
        self.window.noutrefresh()
        self.text_window.noutrefresh()
        curses.doupdate()

    def put_on_screen(self, message):
        """
        Prints message in window

        Parameters
        ----------
        message : string
        """

        self.text_window.addstr(message + '\n')
        self.update()

    def end_win(self):
        """
        Closes all windows
        """

        self.stdscr.clear()
        curses.endwin()

