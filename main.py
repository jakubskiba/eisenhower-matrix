import sys
import datetime
import todo_matrix
from curses_window import *


def ask_user(window, prompt):
    """
    Asks for user input

    Parameters
    ----------
    window : CoursesWindow
    prompt : string

    Returns
    -------
    string
    """

    window.put_on_screen(prompt)
    curses.echo()
    user_input = window.text_window.getstr().decode(encoding="utf-8")
    curses.noecho()
    return user_input


def print_menu(window, menu_options):
    """
    Prints menu and provide navigation

    Parameters
    ----------
    window : CoursesWindow
    menu_options : list of strings

    Returns
    -------
    int - if some option was selected
    None - if user quit menu
    """

    height, width = window.stdscr.getmaxyx()

    for option in menu_options:
        window.put_on_screen(option)

    selected = 0
    window.text_window.chgat(selected, 0, curses.A_REVERSE)
    window.update()

    while True:
        c = window.getch()
        if c == ord('q'):
            return None

        elif c == curses.KEY_UP or c == ord('k') or c == ord('w'):
            if selected > 0:
                window.text_window.chgat(selected, 0, curses.A_NORMAL)
                selected -= 1

        elif c == curses.KEY_DOWN or c == ord('j') or c == ord('s'):
            if selected < len(menu_options)-1:
                window.text_window.chgat(selected, 0, curses.A_NORMAL)
                selected += 1

        elif c == curses.KEY_ENTER or c == 10 or c == 14:
            return selected

        window.text_window.chgat(selected, 0, curses.A_REVERSE)
        window.update()


def add_item(matrix):
    """
    Ask user for data and add it to matrix

    Parameters
    ----------
    matrix : TodoMatrix
    """
    window = CoursesWindow('Eisenhower matrix: add item', 'Please provide data, validate with enter')
    title = ask_user(window, 'title')
    window.end_win()

    month = ''
    while not(month.isdigit() and int(month) >= 1 and int(month) <= 12):
        window = CoursesWindow('Eisenhower matrix: add item', '')
        month = ask_user(window, 'deadline month:')
        window.end_win()
    month = int(month)

    day = ''
    while not(day.isdigit() and int(day) >= 1 and int(day) <= 31):
        window = CoursesWindow('Eisenhower matrix: add item', '')
        day = ask_user(window, 'deadline day:')
        window.end_win()
    day = int(day)

    window = CoursesWindow('Is task important?', '')
    decision = print_menu(window, ['no', 'yes'])
    if decision:
        is_important = True
    else:
        is_important = False
    window.end_win()

    deadline = datetime.datetime(2017, month, day, 0, 0, 0)
    matrix.add_item(title, deadline, is_important)


def choose_quarter(matrix):
    """
    Ask user to choose matrix quarter

    Parameters
    ----------
    matrix : CoursesWindow

    Return
    ------
    tuple : TodoQuarter, string when user made a choice
    tuple : None, None when user exits menu
    """

    window = CoursesWindow('Eisenhower matrix: show quarter', 'choose quarter')

    quarter_menu = ['urgent & important', 'urgent & non important',
                    'non urgent and important', 'non urgent and non important']

    quarter = print_menu(window, quarter_menu)
    window.end_win()

    quarters = {0: 'IU', 1: 'IN', 2: 'NU', 3: 'NN'}

    if quarter is None:
        return (None, None)
    else:
        return (matrix.get_quarter(quarters[quarter]), quarter_menu[quarter])


def change_task_status(task):
    """
    Parameters
    ----------
    task : TodoItem
    """

    if task.is_done:
        task.unmark()
    else:
        task.mark()


def delete_task(quarter, task):
    """
    Deletes task from quarter
    Parameters
    ----------
    quarter : TodoQuarter
    task : TodoItem
    """

    index_to_delete = None
    for index in range(len(quarter.todo_items)):
        if quarter.todo_items[index] == task:
            index_to_delete = index

    window = CoursesWindow('Deleting task: ' + str(task) + '. Are you sure?', '')
    decision = int(print_menu(window, ['no', 'yes']))
    window.end_win()

    if index_to_delete is not None and decision:
        quarter.remove_item(index_to_delete)


def view_task(quarter, task):
    """
    Provides menu for operation on task

    Parameters
    ----------
    quarter : TodoQuarter
    task : TodoItem
    """

    window = CoursesWindow('Task: ' + str(task), 'choose operation validate with enter, q to return')
    operations = ['change status', 'delete task', 'return to main menu']
    operation = print_menu(window, operations)
    window.end_win()
    if operation == 0:
        change_task_status(task)
    elif operation == 1:
        delete_task(quarter, task)


def show_quarter(*args):
    """
    Lists all task in specified quarter

    Parameters
    ----------
    args : tuple
        TodoQuarter, string
    """

    if args[0] is None:
        return None

    quarter_name = args[1]
    q = args[0]

    while True:
        window = CoursesWindow('Eisenhower matrix: show quarter ' + quarter_name,
                               'Press: q to return to main menu, enter to view task details')
        tasks = q.todo_items

        selected_task = ''
        selected_task = print_menu(window, [str(task) for task in tasks])

        window.end_win()

        # return when q was pressed
        if selected_task is None:
            break

        # return if there is no task in quarter
        try:
            task = tasks[selected_task]
        except IndexError:
            break

        view_task(q, task)


def archive_items(matrix):
    """
    Deletes all done tasks

    Parameters
    ----------
    matrix : TodoMatrix
    """

    window = CoursesWindow('All done items will be deleted. Are you sure?', '')
    decision = int(print_menu(window, ['no', 'yes']))
    window.end_win()
    if decision:
        matrix.archive_items()


def show_all_tasks(matrix):
    """
    Lists task from entire matrix sorted by deadline

    Parameters
    ----------
    matrix : TodoMatrix
    """

    all_tasks = todo_matrix.todo_quarter.TodoQuarter()

    for quarter in matrix.todo_quarters:
        all_tasks.todo_items += matrix.todo_quarters[quarter].todo_items

    all_tasks.sort_items()
    show_quarter(all_tasks, 'All tasks: ')


def show_whole_matrix(matrix):
    """
    Parameters
    ----------
    matrix : TodoMatrix
    """
    window = CoursesWindow('Eisenhower Matrix', 'press any key')
    window.put_on_screen(str(matrix))
    window.getch()
    window.end_win()


def open_file(matrix):
    """
    Loads data from file to matrix

    Asks user for file path if wasn't provided in system argument
    Creates file if non existing

    Parameters
    ----------
    matrix : TodoMatrix
    """

    try:
        sys.argv[1]
        file_path = sys.argv[1]
    except IndexError:
        window = CoursesWindow('Please enter database file path', '')
        file_path = ask_user(window, 'file path: ')
        window.end_win()

    try:
        matrix.add_items_from_file(file_path)
    except FileNotFoundError:
        window = CoursesWindow('File ' + file_path + 'non exists. Do you want to create it?', '')
        decision = int(print_menu(window, ['no', 'yes']))
        window.end_win()
        if decision:
            open(file_path, 'a').close()
            matrix.add_items_from_file(file_path)
        else:
            print('Goodbye')
            exit()

    return file_path


def main():
    matrix = todo_matrix.TodoMatrix()

    file_path = open_file(matrix)

    current_function = 0
    while current_function is not None:
        window = CoursesWindow('Eisenhower matrix', 'press q to quit, k or w to move up, j or s to move down')
        current_function = print_menu(window, ['add task',
                                               'show quarter', 'show all task chronologically', 'show whole matrix',
                                               'archive items'])
        window.end_win()
        if current_function == 0:
            add_item(matrix)

        elif current_function == 1:
            show_quarter(*choose_quarter(matrix))

        elif current_function == 2:
            show_all_tasks(matrix)

        elif current_function == 3:
            show_whole_matrix(matrix)

        elif current_function == 4:
            archive_items(matrix)

        elif current_function is None:
            window = CoursesWindow('Do you really want to quit?', 'All task will be automatically archived and saved')
            decision = print_menu(window, ['no', 'yes'])
            window.end_win()

            if not decision:
                current_function = 0

    matrix.archive_items()
    matrix.save_items_to_file(file_path)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        curses.endwin()
