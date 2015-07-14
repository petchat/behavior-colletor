__author__ = 'jiaying.lu'


class BlankConditionException(Exception):

    def __init__(self, err_msg):
        super(BlankConditionException, self).__init__()
        self.message = err_msg

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message
