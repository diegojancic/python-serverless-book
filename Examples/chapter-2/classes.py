
class User(object):

    def __init__(self, name):
        self._name = name

    def show_name(self):
        print("My name is: {}".format(self._name))


user = User(name="John")
user.show_name()
