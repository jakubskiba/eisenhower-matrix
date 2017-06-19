from operator import attrgetter
import todo_item


class TodoQuarter:
    """

    Attributes
    ----------
    todo_items : list
    """

    def __init__(self):
        """
        """
        self.todo_items = []

    def sort_items(self):
        """
        Sorts a todo_items list decreasing by attribute deadline.
        """

        self.todo_items = sorted(self.todo_items, key=attrgetter('deadline'))

    def add_item(self, title, deadline):
        """
        Appends TodoItem object to attribute todo_items sorted decreasing by deadline.

        Raises
        ------
        TypeError if an argument deadline is not an instance of Datetime class.
        """

        item_to_add = todo_item.TodoItem(title, deadline)

        self.todo_items.append(item_to_add)

        self.sort_items()

    def remove_item(self, index):
        """
        Removes TodoItem object from index of attribute todo_items.
        """

        self.todo_items.pop(index)

    def archive_items(self):
        """
        Removes all TodoItem objects with a parameter is_done set to True from attribute todo_items.
        """

        new_list = []

        for item in self.todo_items:
            if not item.is_done:
                new_list.append(item)

        self.todo_items = new_list

    def get_item(self, index):
        """
        Returns
        -------
        TodoItem

        Raises
        ------
        IndexError if an argument index is out of range attribute todo_items.
        """

        return self.todo_items[index]

    def __repr__(self):
        """
        Returns
        -------
        string : formatted string of todo_items sorted decreasing by deadline.
        """

        counter = 1
        representation = ''
        for item in self.todo_items:
            representation += str(counter)
            representation += '. '
            representation += str(item)
            representation += '\n'
            counter += 1

        return representation
