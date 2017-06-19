import todo_quarter
import datetime


class TodoMatrix:
    """
    Attributes
    ----------
    todo_quarters : dictionary 
        description : contains TodoQuarter objects
        key: string - status of todo_quarter
        value: TodoQuarter object
    """

    def __init__(self):
        self.todo_quarters = {}

        statuses = ['IU', 'IN', 'NU', 'NN']

        for status in statuses:
            self.todo_quarters[status] = todo_quarter.TodoQuarter()

    def get_quarter(self, status):
        """
        Returns a chosen TodoQuarter object
        """

        if status in ['IU', 'IN', 'NU', 'NN']:
            return self.todo_quarters[status]
        else:
            raise ValueError('No such status')

    def _check_datatime_type(self, obj):
        """
        Raises
        ------
        Type error when type is not datatime
        """

        if not type(obj) == datetime.datetime:
            raise TypeError('Type is not datatime')

    def _is_urgent(self, deadline):
        """
        Check is there at least 3 days to deadline

        Returns
        -------
        boolean
        """

        current_date = datetime.datetime.now()
        delta = deadline - current_date
        if delta.days > 3:
            return False
        else:
            return True

    def add_item(self, title, deadline, is_important=False):
        """
        Append a TodoQuarterItem object to attribute todo_items in the properly TodoQuarter object

        Raises
        ------
        TypeError : if an argument deadline is not an instance of class Datetime
        """

        self._check_datatime_type(deadline)

        is_urgent = self._is_urgent(deadline)

        if is_important and is_urgent:
            quarter = 'IU'
        elif is_important and not is_urgent:
            quarter = 'IN'
        elif not is_important and is_urgent:
            quarter = 'NU'
        elif not is_important and not is_urgent:
            quarter = 'NN'

        self.todo_quarters[quarter].add_item(title, deadline) 

    def add_items_from_file(self, file_name):
        """
        Reads data from file and add new objects

        Raises
        ------
        FileNotFoundError : if a file doesn't exist
        """

        with open(file_name, 'r') as f:
            for line in f:
                line = line.replace('\n', '').split('|')

                if len(line) != 3:
                    continue

                title = line[0]

                day = int(line[1].split('-')[0])
                month = int(line[1].split('-')[1])

                if line[2] == 'important':
                    is_important = True
                else:
                    is_important = False

                deadline = datetime.datetime(2017, month, day, 0, 0, 0)

                self.add_item(title, deadline, is_important)

    def _convert_todoitem_to_csv(self, item, important):
        """
        Generates csv line

        Returns
        -------
        string
        """

        line = ''
        line += item.title
        line += '|'
        line += str(item.deadline.day)
        line += '-'
        line += str(item.deadline.month)
        line += '|'
        line += important
        line += '\n'

        return line

    def _is_quarter_important(self, quarter):
        """
        Parameters
        ----------
        quarter : string

        Returns
        -------
        string
        """
        if 'I' in quarter:
            return 'important'
        else:
            return ''

    def save_items_to_file(self, file_name):
        """
        Saves items from each quarter to file

        Parameters
        ----------
        file_name : string, path to file
        """
        with open(file_name, 'w') as f:
            for quarter in self.todo_quarters:
                for item in self.todo_quarters[quarter].todo_items:
                    important = self._is_quarter_important(quarter)
                    line = self._convert_todoitem_to_csv(item, important)
                    f.write(line)

    def archive_items(self):
        """
        Removes all done todo items
        """

        for quarter in self.todo_quarters:
            self.todo_quarters[quarter].archive_items()

    def __repr__(self):

        representation = ''

        representation += 'Important & Urgent\n'
        representation += str(self.todo_quarters['IU'])

        representation += 'Important & Non urgent\n'
        representation += str(self.todo_quarters['IN'])

        representation += 'Non important & Urgent\n'
        representation += str(self.todo_quarters['NU'])

        representation += 'Non important & Non urgent\n'
        representation += str(self.todo_quarters['NN'])

        return representation
