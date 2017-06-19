import datetime


class TodoItem:
    """
    Single task

    Attributes
    ----------

    title : string
    deadline : datetime
    is_done : boolean


    """
    def __init__(self, title, deadline):
        """
        Parameters
        ----------
        title : string
        deadline : datetime
        """

        self.title = title
        self.deadline = deadline
        self.is_done = False

        self._check_arguments()

        self.deadline = self.deadline.replace(year=2017)

    def _check_arguments(self):
        """
        Raises
        ------
        Type error when type of argument is not correct
        """

        if not type(self.title) == str:
            raise TypeError('Title type incorrect')

        if not type(self.deadline) == datetime.datetime:
            raise TypeError('Deadline type incorrect')

        if not type(self.is_done) == bool:
            raise TypeError('is_done type incorrect')

    def mark(self):
        """
        Set task status to done
        """

        self.is_done = True

    def unmark(self):
        """
        Set task status to undone
        """

        self.is_done = False

    def get_cross_if_done(self):
        """
        Returns
        -------
        string
        """

        if self.is_done:
            return 'x'
        else:
            return ' '

    def __repr__(self):
        """
        Returns a formatted string with details about todo_item.

        Returns
        -------
        string
        """

        add_list = ['[', self.get_cross_if_done(), '] ',
                    self.deadline.day, '-', self.deadline.month, ' ',
                    self.title
                    ]

        representation = ''

        for item in add_list:
            representation += str(item)

        return representation
